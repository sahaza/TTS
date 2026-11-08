#!/usr/bin/env python3
"""Prepare a Malagasy (mg) fine-tuning dataset for XTTS-v2.

Reads a metadata file (`metadata.csv` or `metadata.txt`) with one sample per line:

    audio_file.wav | Transcription en malgache | Nom_Du_Locuteur [| emotion]

- resamples every audio file to mono 24 kHz (required by XTTS-v2),
- automatically splits segments longer than `--max-segment` seconds at silence
  boundaries (falling back to an even split when no pause is found),
- normalizes the transcriptions with the XTTS multilingual cleaner for `mg`,
- writes `wavs/*.wav` plus `metadata_train.csv` / `metadata_val.csv` (coqui
  formatter format: `audio_file|text|speaker_name[|emotion_name]`) into `--out-dir`.

Example:
    python scripts/prepare_mg_dataset.py \
        --metadata data/metadata.csv \
        --wavs-dir data/raw_wavs \
        --out-dir data/mg_dataset \
        --language mg
"""

import argparse
import csv
import os
import sys
import wave

try:
    import numpy as np
except ImportError:  # pragma: no cover - numpy is a TTS dependency
    np = None

try:
    import soundfile as sf
except ImportError:
    sf = None

XTTS_SAMPLE_RATE = 24000


def load_audio(path):
    """Load an audio file as (samples, sample_rate). Samples are floats in [-1, 1]."""
    if sf is not None:
        data, sr = sf.read(path, dtype="float32", always_2d=True)
        return data.mean(axis=1).tolist(), sr
    try:
        import librosa

        data, sr = librosa.load(path, sr=None, mono=True)
        return data.tolist(), sr
    except ImportError:
        pass
    with wave.open(path, "rb") as w:
        sr = w.getframerate()
        n_channels = w.getnchannels()
        sampwidth = w.getsampwidth()
        raw = w.readframes(w.getnframes())
    if sampwidth == 2:
        import array

        samples = array.array("h")
        samples.frombytes(raw)
        scale = 32768.0
    elif sampwidth == 4:
        import array

        samples = array.array("i")
        samples.frombytes(raw)
        scale = 2147483648.0
    else:
        raise ValueError(f"Unsupported sample width {sampwidth} for {path} (use 16/32-bit PCM wav, or install soundfile/librosa)")
    if n_channels > 1:
        samples = [samples[i] for i in range(0, len(samples), n_channels)]
    return [s / scale for s in samples], sr


def resample(samples, orig_sr, target_sr):
    """Linear-interpolation resampling to `target_sr`."""
    if orig_sr == target_sr:
        return samples
    if np is not None:
        n_new = int(len(samples) * target_sr / orig_sr)
        x_old = np.arange(len(samples), dtype=np.float64)
        x_new = np.linspace(0, len(samples) - 1, n_new)
        return np.interp(x_new, x_old, np.asarray(samples, dtype=np.float64)).tolist()
    duration = len(samples) / orig_sr
    n_new = int(duration * target_sr)
    out = []
    for i in range(n_new):
        pos = i * orig_sr / target_sr
        i0 = int(pos)
        frac = pos - i0
        i1 = min(i0 + 1, len(samples) - 1)
        out.append(samples[i0] * (1 - frac) + samples[i1] * frac)
    return out


def write_wav(path, samples, sr):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if sf is not None:
        sf.write(path, np.asarray(samples, dtype=np.float32), sr)
        return
    import array

    pcm = array.array("h", (int(max(-1.0, min(1.0, s)) * 32767) for s in samples))
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def find_split_points(samples, sr, max_sec, min_sec, pause_sec=0.25):
    """Return sample indices where to cut so that every chunk is <= max_sec.

    Cuts happen in the middle of low-energy (silence) windows; if no pause is
    found in the allowed zone, the segment is cut evenly.
    """
    n = len(samples)
    max_len = int(max_sec * sr)
    min_len = int(min_sec * sr)
    if n <= max_len:
        return [0, n]
    frame = int(0.025 * sr)
    hop = int(0.010 * sr)
    if frame <= 0 or n < frame:
        return [0, n]
    energies = []
    for start in range(0, n - frame + 1, hop):
        e = 0.0
        for s in samples[start : start + frame]:
            e += s * s
        energies.append(e)
    if not energies:
        return [0, n]
    peak = max(energies)
    threshold = 0.05 * peak
    pause_frames = int(pause_sec * sr / hop)

    cuts = [0]
    pos = 0
    while pos + max_len < n:
        # look for a silence window in [pos + min_len, pos + max_len]
        lo = (pos + min_len) // hop
        hi = min((pos + max_len) // hop, len(energies) - pause_frames)
        best = None
        i = lo
        while i < hi:
            if all(energies[i + k] < threshold for k in range(pause_frames)):
                best = i + pause_frames // 2  # keep the latest pause in the window
            i += 1
        if best is None:
            # no pause found: cut in the middle of the allowed window
            best = (2 * pos + max_len) // (2 * hop)
        cut = best * hop
        cuts.append(cut)
        pos = cut
    cuts.append(n)
    return cuts


def normalize_text(text, lang):
    """Normalize a transcription with the XTTS multilingual cleaner when available."""
    text = " ".join(text.split())
    try:
        from TTS.tts.layers.xtts.tokenizer import multilingual_cleaners

        return multilingual_cleaners(text, lang)
    except Exception:
        return text.lower()


def read_metadata(metadata_path):
    """Yield (audio_file, text, speaker_name, emotion_or_None) rows."""
    with open(metadata_path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if not line.strip():
                continue
            parts = [p.strip() for p in line.split("|")]
            first = parts[0].lower()
            if lineno == 1 and first in {"audio_file", "wav_filename", "file", "filename", "path"}:
                continue  # header row
            if len(parts) == 2:
                audio_file, text, speaker, emotion = parts[0], parts[1], "default", None
            elif len(parts) == 3:
                audio_file, text, speaker, emotion = parts[0], parts[1], parts[2], None
            else:
                audio_file = parts[0]
                text = "|".join(parts[1:-2])
                speaker = parts[-2]
                emotion = parts[-1]
            yield lineno, audio_file, text, speaker, emotion


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--metadata", required=True, help="Path to metadata.csv / metadata.txt (file.wav | text | speaker [| emotion])")
    parser.add_argument("--wavs-dir", required=True, help="Directory containing the source audio files")
    parser.add_argument("--out-dir", required=True, help="Output dataset directory (wavs/ + metadata_train.csv + metadata_val.csv)")
    parser.add_argument("--language", default="mg", help="Language code stamped on cleaned text (default: mg)")
    parser.add_argument("--sample-rate", type=int, default=XTTS_SAMPLE_RATE, help="Target sample rate in Hz (default: 24000, XTTS-v2)")
    parser.add_argument("--max-segment", type=float, default=11.0, help="Max segment duration in seconds before auto-split (default: 11)")
    parser.add_argument("--min-segment", type=float, default=0.5, help="Min segment duration in seconds (default: 0.5)")
    parser.add_argument("--val-ratio", type=float, default=0.05, help="Fraction of samples kept for validation (default: 0.05)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for the train/val split (default: 42)")
    args = parser.parse_args()

    import random

    random.seed(args.seed)
    os.makedirs(args.out_dir, exist_ok=True)

    rows = []
    skipped = 0
    for lineno, audio_file, text, speaker, emotion in read_metadata(args.metadata):
        src = audio_file if os.path.isabs(audio_file) else os.path.join(args.wavs_dir, audio_file)
        if not os.path.exists(src):
            print(f" [!] line {lineno}: audio not found, skipped -> {src}")
            skipped += 1
            continue
        samples, sr = load_audio(src)
        samples = resample(samples, sr, args.sample_rate)
        cuts = find_split_points(samples, args.sample_rate, args.max_segment, args.min_segment)
        base = os.path.splitext(os.path.basename(audio_file))[0]
        clean_text = normalize_text(text, args.language)
        for seg_idx in range(len(cuts) - 1):
            start, end = cuts[seg_idx], cuts[seg_idx + 1]
            if end - start < int(args.min_segment * args.sample_rate):
                continue
            seg = samples[start:end]
            rel_path = f"wavs/{speaker}_{base}_{seg_idx:05d}.wav"
            write_wav(os.path.join(args.out_dir, rel_path), seg, args.sample_rate)
            row = {"audio_file": rel_path, "text": clean_text, "speaker_name": speaker}
            if emotion:
                row["emotion_name"] = emotion
            rows.append(row)
        print(f" [+] {audio_file}: {len(cuts) - 1} segment(s), {len(samples) / args.sample_rate:.1f}s @ {args.sample_rate}Hz")

    if not rows:
        print(" [!] No usable samples were produced. Check --metadata and --wavs-dir.")
        sys.exit(1)

    random.shuffle(rows)
    n_val = max(1, int(len(rows) * args.val_ratio)) if len(rows) > 1 else 0
    val_rows, train_rows = rows[:n_val], rows[n_val:]

    has_emotion = any(r.get("emotion_name") for r in rows)
    if has_emotion:
        for r in rows:
            r["emotion_name"] = r.get("emotion_name") or "neutral"
    fieldnames = ["audio_file", "text", "speaker_name"] + (["emotion_name"] if has_emotion else [])
    for name, subset in [("metadata_train.csv", train_rows), ("metadata_val.csv", val_rows)]:
        path = os.path.join(args.out_dir, name)
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="|", extrasaction="ignore")
            writer.writeheader()
            writer.writerows(subset)
        print(f" [>] wrote {path} ({len(subset)} samples)")

    speakers = sorted({r["speaker_name"] for r in rows})
    print(f" [>] done: {len(rows)} samples, {skipped} skipped, speakers: {speakers}")
    print(f" [>] dataset root for training: {os.path.abspath(args.out_dir)}")


if __name__ == "__main__":
    main()
