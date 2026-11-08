#!/usr/bin/env python3
"""Fine-tune XTTS-v2 on a Malagasy (mg) dataset prepared with scripts/prepare_mg_dataset.py.

Example:
    python recipes/xtts_mg/train_xtts_mg.py \
        --train-csv data/mg_dataset/metadata_train.csv \
        --eval-csv data/mg_dataset/metadata_val.csv \
        --output-path runs/xtts_mg \
        --language mg --epochs 10 --batch-size 4 --grad-accum 1 --max-audio-length 11
"""

import argparse

from TTS.demos.xtts_ft_demo.utils.gpt_train import train_gpt


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--train-csv", required=True, help="metadata_train.csv produced by scripts/prepare_mg_dataset.py")
    parser.add_argument("--eval-csv", required=True, help="metadata_val.csv produced by scripts/prepare_mg_dataset.py")
    parser.add_argument("--output-path", default="./runs/xtts_mg", help="Where checkpoints/logs are written (default: ./runs/xtts_mg)")
    parser.add_argument("--language", default="mg", help="Language code of the dataset (default: mg)")
    parser.add_argument("--epochs", type=int, default=10, help="Number of epochs (default: 10)")
    parser.add_argument("--batch-size", type=int, default=4, help="Batch size (default: 4)")
    parser.add_argument("--grad-accum", type=int, default=1, help="Gradient accumulation steps (default: 1)")
    parser.add_argument(
        "--max-audio-length",
        type=float,
        default=11.0,
        help="Max audio segment length in seconds kept during training (default: 11)",
    )
    args = parser.parse_args()

    # train_gpt expects max_wav_length in samples at 22050 Hz
    max_wav_length = int(args.max_audio_length * 22050)

    config_path, checkpoint, vocab_file, trainer_out_path, speaker_ref = train_gpt(
        args.language,
        args.epochs,
        args.batch_size,
        args.grad_accum,
        args.train_csv,
        args.eval_csv,
        output_path=args.output_path,
        max_audio_length=max_wav_length,
    )
    print(" [>] Fine-tuning finished!")
    print(f"     config:     {config_path}")
    print(f"     checkpoint: {checkpoint}")
    print(f"     vocab:      {vocab_file}")
    print(f"     runs:       {trainer_out_path}")
    print(f"     speaker ref (6-15s sample to reuse for cloning): {speaker_ref}")


if __name__ == "__main__":
    main()
