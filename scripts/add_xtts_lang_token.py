#!/usr/bin/env python3
"""Add a language token (e.g. `[mg]`) to an XTTS BPE vocab.json if it is missing.

XTTS-v2 prefixes every input with a `[<lang>]` token. The official vocab.json only
ships the 17 originally supported languages, so a new language such as Malagasy
(`mg`) must be appended for `language="mg"` to encode correctly instead of
falling back to `[UNK]`. The fine-tuning loader uses `strict=False`
(`TTS/tts/layers/xtts/trainer/gpt_trainer.py`), so the extra embedding row for the
new token is simply learned during fine-tuning.

Example:
    python scripts/add_xtts_lang_token.py --vocab ~/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2/vocab.json --lang mg
"""

import argparse
import json


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vocab", required=True, help="Path to the XTTS vocab.json (tokenizer file)")
    parser.add_argument("--lang", default="mg", help="Language code to add, e.g. mg (default: mg)")
    parser.add_argument("--out", default=None, help="Output path. Defaults to in-place update of --vocab")
    args = parser.parse_args()

    token = f"[{args.lang}]"
    with open(args.vocab, "r", encoding="utf-8") as f:
        data = json.load(f)

    vocab = data["model"]["vocab"]
    if token in vocab:
        print(f" [>] {token} already present with id={vocab[token]}, nothing to do.")
        return

    new_id = max(vocab.values()) + 1
    vocab[token] = new_id
    data.setdefault("added_tokens", []).append(
        {
            "id": new_id,
            "special": True,
            "content": token,
            "single_word": False,
            "lstrip": False,
            "rstrip": False,
            "normalized": False,
        }
    )

    out = args.out or args.vocab
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f" [>] added {token} with id={new_id} -> {out} (new vocab size: {new_id + 1})")


if __name__ == "__main__":
    main()
