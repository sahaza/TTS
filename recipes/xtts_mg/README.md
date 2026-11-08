# XTTS-v2 fine-tuning for Malagasy (`mg`)

This fork adds official Malagasy (`mg`) support to XTTS-v2:

- `mg` is in `XttsConfig.languages` (`TTS/tts/configs/xtts_config.py`),
- the XTTS tokenizer cleans Malagasy text (lowercase, numbers in Malagasy via
  `TTS/tts/layers/xtts/mg_num2words.py`, abbreviations, symbols, ordinals) in
  `TTS/tts/layers/xtts/tokenizer.py`,
- a generic `malagasy_cleaners` is available for other models
  (`text_cleaner: "malagasy_cleaners"`),
- espeak-ng already ships `mg`, so phonemizer-based models pick it up
  automatically through `DEF_LANG_TO_PHONEMIZER`.

## 1. Prepare the dataset

Metadata file (`metadata.csv` or `metadata.txt`), one sample per line:

```
audio_file.wav | Transcription en malgache | Nom_Du_Locuteur [| emotion]
```

```bash
python scripts/prepare_mg_dataset.py \
    --metadata data/metadata.csv \
    --wavs-dir data/raw_wavs \
    --out-dir data/mg_dataset \
    --language mg \
    --sample-rate 24000 \
    --max-segment 11 \
    --val-ratio 0.05
```

The script resamples everything to mono **24 kHz** (XTTS-v2 requirement), splits
segments longer than `--max-segment` at silence boundaries, and writes
`data/mg_dataset/wavs/*.wav`, `metadata_train.csv` and `metadata_val.csv`
(format `audio_file|text|speaker_name[|emotion_name]`, compatible with the
`coqui` dataset formatter used by the XTTS trainer).

## 2. Fine-tune XTTS-v2 on your Malagasy data

The training wrapper automatically downloads the XTTS-v2 base files and adds
the `[mg]` token to the tokenizer vocab if missing (the official vocab only
contains the 17 original languages):

```bash
python recipes/xtts_mg/train_xtts_mg.py \
    --train-csv data/mg_dataset/metadata_train.csv \
    --eval-csv data/mg_dataset/metadata_val.csv \
    --output-path runs/xtts_mg \
    --language mg \
    --epochs 10 --batch-size 4 --grad-accum 1 --max-audio-length 11
```

(Alternatively use the Gradio demo: `python TTS/demos/xtts_ft_demo/xtts_demo.py`,
language `mg` is now in the dropdowns.)

Checkpoints land in `runs/xtts_mg/run/training/` (look for the `best_model.pth`
inside `XTTS_trainer/...` run folder; `config.json`, `vocab.json`, `model.pth`,
`dvae.pth`, `mel_stats.pth` are the files to ship).

To add `[mg]` to an already-downloaded vocab manually:

```bash
python scripts/add_xtts_lang_token.py --vocab <model_dir>/vocab.json --lang mg
```

## 3. Generate speech with a custom Malagasy voice (6–15 s reference)

Python API — `speaker_wav` accepts a 6–15 s Malagasy sample; prosody knobs are
passed directly to the model:

```python
from TTS.api import TTS

tts = TTS(model_path="runs/xtts_mg/.../best_model.pth",
          config_path="runs/xtts_mg/.../config.json",
          vocab_path="runs/xtts_mg/.../vocab.json",
          gpu=True)

tts.tts_to_file(
    "Manaona struktura! Izany dia andrana amin'ny feo malagasy.",
    speaker_wav="data/ref_6a15s.wav",   # 6-15 seconds of Malagasy speech
    language="mg",
    file_path="out.wav",
    temperature=0.65,                   # lower = flatter/more stable, higher = more expressive
    repetition_penalty=5.0,             # raise if it stutters or loops
    length_penalty=1.0,
    top_k=50,
    top_p=0.85,
    max_new_tokens=400,                 # caps output length (audio tokens)
)
```

CLI equivalent:

```bash
tts --model_path runs/xtts_mg/.../best_model.pth \
    --config_path runs/xtts_mg/.../config.json \
    --vocab_path runs/xtts_mg/.../vocab.json \
    --speaker_wav data/ref_6a15s.wav \
    --language_idx mg \
    --text "Manaona struktura! Izany dia andrana amin'ny feo malagasy." \
    --out_path out.wav \
    --temperature 0.65 --repetition_penalty 5.0 --max_new_tokens 400
```

The same knobs can be set permanently in the model `config.json`
(`temperature`, `repetition_penalty`, `length_penalty`, `top_k`, `top_p`,
`max_new_tokens`, and for the reference window `gpt_cond_len`, `gpt_cond_chunk_len`,
`max_ref_len` — the default `max_ref_len` is now `15` s so 6–15 s references are
fully used).

## 4. Tips for tone/emotion variation

- Keep one clean 6–15 s reference per speaker; several references can be passed
  as a list (`speaker_wav=["a.wav", "b.wav"]`) and are averaged.
- `temperature` 0.4–0.6 → neutral, stable prosody; 0.7–0.9 → more expressive.
- `repetition_penalty` 3–10 → avoids loops/long silences; lower it if speech
  gets cut off.
- `max_new_tokens` bounds generation length (~1 token ≈ 40 ms of audio).
- For training-time emotion variation, add a 4th column to `metadata.csv`
  (`file.wav|text|speaker|emotion`) — it is forwarded as `emotion_name`.
