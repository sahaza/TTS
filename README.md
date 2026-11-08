# Full TTS

**Full TTS** is a library for advanced Text-to-Speech generation.

- Pretrained models in +1100 languages.
- Tools for training new models and fine-tuning existing models in any language.
- Utilities for dataset analysis and curation.

______________________________________________________________________

## News
- **XTTS-v2 now supports Malagasy (mg)** — 18 languages in total, with a fine-tuning recipe in [`recipes/xtts_mg`](recipes/xtts_mg).
- XTTS-v2 is out with 16 languages, voice cloning from a 3-second clip and streaming under 200 ms.
- Bark and Tortoise are available for unconstrained voice cloning, plus ~1100 Fairseq MMS models.

## Features
- High-performance deep learning models for Text2Speech (Tacotron, Glow-TTS, VITS, XTTS, YourTTS, Bark, Tortoise, ...).
- Speaker encoder for speaker embeddings, vocoders (MelGAN, HiFiGAN, UnivNet, WaveRNN, ...), voice conversion (FreeVC).
- Multi-speaker and multi-lingual models, fast training with detailed terminal/TensorBoard logs.
- A lightweight but feature-complete `Trainer API`, ready-to-use released models and dataset curation tools.

## Installation
Full TTS requires **Python >= 3.9, < 3.12** and, for phonemizer-based models, the `espeak-ng` system package.

**Inference only** — install from PyPI:

```bash
pip install Full-TTS
```

**Development / training** — get a local checkout of this repository, then:

```bash
pip install -e .[all,dev,notebooks]   # pick the extras you need
```

On Ubuntu/Debian, system dependencies (espeak-ng, libsndfile, ...) can be installed with the Makefile:

```bash
make system-deps   # Ubuntu/Debian only
make install
```

**Docker** — build and run the server image from the `Dockerfile` in this repository:

```bash
docker build -t full-tts .
docker run --rm -it -p 5002:5002 full-tts
python3 TTS/server/server.py --model_name tts_models/multilingual/multi-dataset/xtts_v2
```

The server is then available at `http://[::1]:5002/` (see the [Docker docs](https://tts.readthedocs.io/en/latest/docker_images.html)).

## Quickstart

### Python API — multi-lingual voice cloning with XTTS-v2

```python
import torch
from TTS.api import TTS

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

tts.tts_to_file(text="Hello world!", speaker_wav="my/cloning/audio.wav", language="en", file_path="output.wav")
# Malagasy (mg) voice cloning with a 6-15s reference sample
tts.tts_to_file(text="Manaona struktura!", speaker_wav="my/cloning/audio_mg.wav", language="mg", file_path="output_mg.wav")
```

### Python API — single-speaker model

```python
tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=False)
tts.tts_to_file(text="Ich bin eine Testnachricht.", file_path="output.wav")
```

### Command line

```bash
tts --text "Hello world!" --model_name tts_models/multilingual/multi-dataset/xtts_v2     --speaker_wav my/cloning/audio.wav --language_idx en --out_path output.wav
```

The full CLI reference is below. List all available models with `tts --list_models`.

### XTTS-v2 languages
XTTS-v2 supports 18 languages: en, es, fr, de, it, pt, pl, tr, ru, nl, cs, ar, zh-cn, ja, hu, ko, hi and **mg (Malagasy)**.
Check them at runtime with `tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 --list_language_idx`.
Fine-tune XTTS-v2 on your own (e.g. Malagasy) data with [`recipes/xtts_mg`](recipes/xtts_mg); see the [XTTS docs](https://tts.readthedocs.io/en/dev/models/xtts.html).

### Command-line `tts` reference

<!-- begin-tts-readme -->

Synthesize speech on command line.

You can either use your trained model or choose a model from the provided list.

If you don't specify any models, then it uses LJSpeech based English model.

#### Single Speaker Models

- List provided models:

  ```
  $ tts --list_models
  ```

- Get model info (for both tts_models and vocoder_models):

  - Query by type/name:
    The model_info_by_name uses the name as it from the --list_models.
    ```
    $ tts --model_info_by_name "<model_type>/<language>/<dataset>/<model_name>"
    ```
    For example:
    ```
    $ tts --model_info_by_name tts_models/tr/common-voice/glow-tts
    $ tts --model_info_by_name vocoder_models/en/ljspeech/hifigan_v2
    ```
  - Query by type/idx:
    The model_query_idx uses the corresponding idx from --list_models.

    ```
    $ tts --model_info_by_idx "<model_type>/<model_query_idx>"
    ```

    For example:

    ```
    $ tts --model_info_by_idx tts_models/3
    ```

  - Query info for model info by full name:
    ```
    $ tts --model_info_by_name "<model_type>/<language>/<dataset>/<model_name>"
    ```

- Run TTS with default models:

  ```
  $ tts --text "Text for TTS" --out_path output/path/speech.wav
  ```

- Run TTS and pipe out the generated TTS wav file data:

  ```
  $ tts --text "Text for TTS" --pipe_out --out_path output/path/speech.wav | aplay
  ```

- Run a TTS model with its default vocoder model:

  ```
  $ tts --text "Text for TTS" --model_name "<model_type>/<language>/<dataset>/<model_name>" --out_path output/path/speech.wav
  ```

  For example:

  ```
  $ tts --text "Text for TTS" --model_name "tts_models/en/ljspeech/glow-tts" --out_path output/path/speech.wav
  ```

- Run with specific TTS and vocoder models from the list:

  ```
  $ tts --text "Text for TTS" --model_name "<model_type>/<language>/<dataset>/<model_name>" --vocoder_name "<model_type>/<language>/<dataset>/<model_name>" --out_path output/path/speech.wav
  ```

  For example:

  ```
  $ tts --text "Text for TTS" --model_name "tts_models/en/ljspeech/glow-tts" --vocoder_name "vocoder_models/en/ljspeech/univnet" --out_path output/path/speech.wav
  ```

- Run your own TTS model (Using Griffin-Lim Vocoder):

  ```
  $ tts --text "Text for TTS" --model_path path/to/model.pth --config_path path/to/config.json --out_path output/path/speech.wav
  ```

- Run your own TTS and Vocoder models:

  ```
  $ tts --text "Text for TTS" --model_path path/to/model.pth --config_path path/to/config.json --out_path output/path/speech.wav
      --vocoder_path path/to/vocoder.pth --vocoder_config_path path/to/vocoder_config.json
  ```

#### Multi-speaker Models

- List the available speakers and choose a <speaker_id> among them:

  ```
  $ tts --model_name "<language>/<dataset>/<model_name>" --list_speaker_idxs
  ```

- Run the multi-speaker TTS model with the target speaker ID:

  ```
  $ tts --text "Text for TTS." --out_path output/path/speech.wav --model_name "<language>/<dataset>/<model_name>" --speaker_idx <speaker_id>
  ```

- Run your own multi-speaker TTS model:

  ```
  $ tts --text "Text for TTS" --out_path output/path/speech.wav --model_path path/to/model.pth --config_path path/to/config.json --speakers_file_path path/to/speaker.json --speaker_idx <speaker_id>
  ```

### Voice Conversion Models

```
$ tts --out_path output/path/speech.wav --model_name "<language>/<dataset>/<model_name>" --source_wav <path/to/speaker/wav> --target_wav <path/to/reference/wav>
```

<!-- end-tts-readme -->

## Links and resources
| Resource | Link |
| -------- | ---- |
| Documentation | [ReadTheDocs](https://tts.readthedocs.io/en/latest/) |
| Contributing | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Questions & discussion | [Discord](https://discord.gg/5eXr5seRrv) |
| Released models | `tts --list_models` |

## Directory structure
```
|- notebooks/   Jupyter notebooks for evaluation and data analysis
|- recipes/     training recipes (incl. recipes/xtts_mg for Malagasy XTTS-v2)
|- scripts/     dataset/tokenizer utilities (e.g. scripts/prepare_mg_dataset.py)
|- TTS/         the Python package (bin/, tts/, encoder/, vocoder/, server/, ...)
|- tests/       test suite
```

## License
Full TTS is released under the [MPL-2.0 license](https://opensource.org/licenses/MPL-2.0). See [LICENSE.txt](LICENSE.txt).

## Citation
If you use Full TTS in your research, please cite it using [CITATION.cff](CITATION.cff).
