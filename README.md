# Coqui TTS

🗣️ **Coqui TTS** is a library for advanced Text-to-Speech generation.

🚀 Pretrained models in +1100 languages.
🛠️ Tools for training new models and fine-tuning existing models in any language.
🧹 Utilities for dataset analysis and curation.

[![Discord](https://img.shields.io/discord/1037326658807533628?color=%239B59B6&label=chat%20on%20discord)](https://discord.gg/5eXr5seRrv)
[![License](<https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg>)](https://opensource.org/licenses/MPL-2.0)
[![PyPI version](https://badge.fury.io/py/TTS.svg)](https://badge.fury.io/py/TTS)
[![Downloads](https://pepy.tech/badge/tts)](https://pepy.tech/project/tts)
[![DOI](https://zenodo.org/badge/265612440.svg)](https://zenodo.org/badge/latestdoi/265612440)
[![Docs](<https://readthedocs.org/projects/tts/badge/?version=latest&style=plastic>)](https://tts.readthedocs.io/en/latest/)

______________________________________________________________________

## 📣 News
- 📣 🥳 **XTTS-v2 now supports Malagasy (mg)** — 18 languages in total, with a fine-tuning recipe in [`recipes/xtts_mg`](recipes/xtts_mg).
- 📣 🥳 XTTSv2 is here with 16 languages and better performance across the board.
- 📣 🥳 XTTS fine-tuning code is out. Check the [example recipes](recipes/ljspeech).
- 📣 🥳 XTTS can now stream with <200ms latency.
- 📣 🥳 XTTS, our production TTS model that can speak 13 languages, is released ([blog post](https://coqui.ai/blog/tts/open_xtts), [demo](https://huggingface.co/spaces/coqui/xtts), [docs](https://tts.readthedocs.io/en/dev/models/xtts.html)).
- 📣 🐶 Bark is now available for inference with unconstrained voice cloning. [Docs](https://tts.readthedocs.io/en/dev/models/bark.html)
- 📣 You can use the [~1100 Fairseq MMS models](https://dl.fbaipublicfiles.com/mms/tts/all-tts-languages.html) with 🗣️TTS.
- 📣 🗣️TTS now supports 🐢Tortoise with faster inference. [Docs](https://tts.readthedocs.io/en/dev/models/tortoise.html)

## 💬 Where to ask questions
Please use our dedicated channels for questions and discussion. Help is much more valuable if it's shared publicly so that more people can benefit from it.

| Type                            | Platform                                  |
| ------------------------------- | ----------------------------------------- |
| 🚨 **Bug Reports**              | The issue tracker of this repository      |
| 🎁 **Feature Requests & Ideas** | The issue tracker of this repository      |
| 👩‍💻 **Usage Questions**          | Community discussions or [Discord]       |
| 🧠 **General Discussion**       | [Discord]                                 |

[discord]: https://discord.gg/5eXr5seRrv

## 🔗 Links and Resources
| Type                     | Link                                                            |
| ------------------------ | --------------------------------------------------------------- |
| 💼 **Documentation**     | [ReadTheDocs](https://tts.readthedocs.io/en/latest/)            |
| 💾 **Installation**      | See [Installation](#installation) below                         |
| 👩‍💻 **Contributing**      | [CONTRIBUTING.md](CONTRIBUTING.md)                              |
| 🚀 **Released Models**   | `tts --list_models`                                             |
| 📰 **Blog**              | [coqui.ai/blog](https://coqui.ai/blog/)                         |

## 🧠 Features
- High-performance deep learning models for Text2Speech tasks.
    - Text2Spec models (Tacotron, Tacotron2, Glow-TTS, SpeedySpeech).
    - Speaker Encoder to compute speaker embeddings efficiently.
    - Vocoder models (MelGAN, Multiband-MelGAN, GAN-TTS, ParallelWaveGAN, WaveGrad, WaveRNN).
- Fast and efficient model training.
- Detailed training logs on the terminal and TensorBoard.
- Support for multi-speaker TTS.
- Efficient, flexible, lightweight but feature complete `Trainer API`.
- Released and ready-to-use models.
- Tools to curate Text2Speech datasets.
- Utilities to use and test your models.
- Modular (but not too much) code base enabling easy implementation of new ideas.

## 🧩 Model Implementations
### Spectrogram models
- Tacotron: [paper](https://arxiv.org/abs/1703.10135)
- Tacotron2: [paper](https://arxiv.org/abs/1712.05884)
- Glow-TTS: [paper](https://arxiv.org/abs/2005.11129)
- Speedy-Speech: [paper](https://arxiv.org/abs/2008.03802)
- Align-TTS: [paper](https://arxiv.org/abs/2003.01950)
- FastPitch: [paper](https://arxiv.org/pdf/2006.06873.pdf)
- FastSpeech: [paper](https://arxiv.org/abs/1905.09263)
- FastSpeech2: [paper](https://arxiv.org/abs/2006.04558)
- SC-GlowTTS: [paper](https://arxiv.org/abs/2104.05557)
- Capacitron: [paper](https://arxiv.org/abs/1906.03402)
- OverFlow: [paper](https://arxiv.org/abs/2211.06892)
- Neural HMM TTS: [paper](https://arxiv.org/abs/2108.13320)
- Delightful TTS: [paper](https://arxiv.org/abs/2110.12612)

### End-to-End Models
- 🥳 XTTS: [blog](https://coqui.ai/blog/tts/open_xtts)
- VITS: [paper](https://arxiv.org/pdf/2106.06103)
- 🗣️ YourTTS: [paper](https://arxiv.org/abs/2112.02418)
- 🐢 Tortoise (original implementation by neonbjb)
- 🐶 Bark (original implementation by Suno)

### Attention Methods
- Guided Attention: [paper](https://arxiv.org/abs/1710.08969)
- Forward Backward Decoding: [paper](https://arxiv.org/abs/1907.09006)
- Graves Attention: [paper](https://arxiv.org/abs/1910.10288)
- Double Decoder Consistency: [blog](https://erogol.com/solving-attention-problems-of-tts-models-with-double-decoder-consistency/)
- Dynamic Convolutional Attention: [paper](https://arxiv.org/pdf/1910.10288.pdf)
- Alignment Network: [paper](https://arxiv.org/abs/2108.10447)

### Speaker Encoder
- GE2E: [paper](https://arxiv.org/abs/1710.10467)
- Angular Loss: [paper](https://arxiv.org/pdf/2003.11825.pdf)

### Vocoders
- MelGAN: [paper](https://arxiv.org/abs/1910.06711)
- MultiBandMelGAN: [paper](https://arxiv.org/abs/2005.05106)
- ParallelWaveGAN: [paper](https://arxiv.org/abs/1910.11480)
- GAN-TTS discriminators: [paper](https://arxiv.org/abs/1909.11646)
- WaveRNN (original implementation by fatchord)
- WaveGrad: [paper](https://arxiv.org/abs/2009.00713)
- HiFiGAN: [paper](https://arxiv.org/abs/2010.05646)
- UnivNet: [paper](https://arxiv.org/abs/2106.07889)

### Voice Conversion
- FreeVC: [paper](https://arxiv.org/abs/2210.15418)

You can also help us implement more models.

## 💾 Installation
🗣️TTS is tested on Ubuntu 18.04 with **python >= 3.9, < 3.12**.

If you are only interested in [synthesizing speech](https://tts.readthedocs.io/en/latest/inference.html) with the released 🗣️TTS models, installing from PyPI is the easiest option.

```bash
pip install TTS
```

If you plan to code or train models, get a local checkout of this repository and install it in editable mode:

```bash
pip install -e .[all,dev,notebooks]  # Select the relevant extras
```

On Ubuntu (Debian) you can also use the Makefile:

```bash
$ make system-deps  # intended to be used on Ubuntu (Debian). Let us know if you have a different OS.
$ make install
```

On Windows, community installation instructions are available [on Stack Overflow](https://stackoverflow.com/questions/66726331/how-can-i-run-mozilla-tts-coqui-tts-training-with-cuda-on-a-windows-system).

## 🐳 Docker Image
You can run TTS without installing it by building the Docker image from the `Dockerfile` in this repository:

```bash
docker build -t tts-cpu .
docker run --rm -it -p 5002:5002 --entrypoint /bin/bash tts-cpu
python3 TTS/server/server.py --list_models                      # list available models
python3 TTS/server/server.py --model_name tts_models/en/vctk/vits  # start a server
```

The TTS server is then available at `http://[::1]:5002/`. More details about Docker images (GPU support, ...) are in the [documentation](https://tts.readthedocs.io/en/latest/docker_images.html).

## 🔊 Synthesizing speech with 🗣️TTS

### 🐍 Python API

#### Running a multi-speaker and multi-lingual model

```python
import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🗣️TTS models
print(TTS().list_models())

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Run TTS
# ❗ Since this model is a multi-lingual voice cloning model, we must set the target speaker_wav and language
wav = tts.tts(text="Hello world!", speaker_wav="my/cloning/audio.wav", language="en")
# Text to speech to a file
tts.tts_to_file(text="Hello world!", speaker_wav="my/cloning/audio.wav", language="en", file_path="output.wav")
# Malagasy (mg) voice cloning with a 6-15s reference sample
tts.tts_to_file(text="Manaona struktura!", speaker_wav="my/cloning/audio_mg.wav", language="mg", file_path="output_mg.wav")
```

#### Running a single speaker model

```python
# Init TTS with the target model name
tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=False).to(device)

# Run TTS
tts.tts_to_file(text="Ich bin eine Testnachricht.", file_path=OUTPUT_PATH)

# Example voice cloning with YourTTS in English, French and Portuguese
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False).to(device)
tts.tts_to_file("This is voice cloning.", speaker_wav="my/cloning/audio.wav", language="en", file_path="output.wav")
tts.tts_to_file("C'est le clonage de la voix.", speaker_wav="my/cloning/audio.wav", language="fr-fr", file_path="output.wav")
tts.tts_to_file("Isso é clonagem de voz.", speaker_wav="my/cloning/audio.wav", language="pt-br", file_path="output.wav")
```

#### Example voice conversion

Converting the voice in `source_wav` to the voice of `target_wav`

```python
tts = TTS(model_name="voice_conversion_models/multilingual/vctk/freevc24", progress_bar=False).to("cuda")
tts.voice_conversion_to_file(source_wav="my/source.wav", target_wav="my/target.wav", file_path="output.wav")
```

#### Example voice cloning together with the voice conversion model
This way, you can clone voices by using any model in 🗣️TTS.

```python
tts = TTS("tts_models/de/thorsten/tacotron2-DDC")
tts.tts_with_vc_to_file(
    "Wie sage ich auf Italienisch, dass ich dich liebe?",
    speaker_wav="target/speaker.wav",
    file_path="output.wav"
)
```

#### Example text to speech using **Fairseq models in ~1100 languages** 🤿
For Fairseq models, use the following name format: `tts_models/<lang-iso_code>/fairseq/vits`.
You can find the language ISO codes [here](https://dl.fbaipublicfiles.com/mms/tts/all-tts-languages.html).

```python
# TTS with on the fly voice conversion
api = TTS("tts_models/deu/fairseq/vits")
api.tts_with_vc_to_file(
    "Wie sage ich auf Italienisch, dass ich dich liebe?",
    speaker_wav="target/speaker.wav",
    file_path="output.wav"
)
```

### 🌍 XTTS-v2 languages
XTTS-v2 supports 18 languages: English (en), Spanish (es), French (fr), German (de), Italian (it), Portuguese (pt), Polish (pl), Turkish (tr), Russian (ru), Dutch (nl), Czech (cs), Arabic (ar), Chinese (zh-cn), Japanese (ja), Hungarian (hu), Korean (ko), Hindi (hi) and **Malagasy (mg)**.
Check the supported languages at runtime with:

```console
$ tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 --list_language_idx
```

See [`recipes/xtts_mg`](recipes/xtts_mg) for fine-tuning XTTS-v2 on Malagasy data and the [model docs](https://tts.readthedocs.io/en/dev/models/xtts.html).

### Command-line `tts`

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
  $ tts --model_name "<language>/<dataset>/<model_name>"  --list_speaker_idxs
  ```

- Run the multi-speaker TTS model with the target speaker ID:

  ```
  $ tts --text "Text for TTS." --out_path output/path/speech.wav --model_name "<language>/<dataset>/<model_name>"  --speaker_idx <speaker_id>
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

## 📁 Directory Structure
```
|- notebooks/       (Jupyter Notebooks for model evaluation, parameter selection and data analysis.)
|- recipes/         (Training recipes, including recipes/xtts_mg for Malagasy XTTS-v2 fine-tuning.)
|- scripts/         (Dataset preparation and tokenizer utilities, e.g. scripts/prepare_mg_dataset.py.)
|- TTS
    |- bin/             (folder for all the executables.)
      |- train*.py                  (train your target model.)
      |- ...
    |- tts/             (text to speech models)
        |- layers/          (model layer definitions)
        |- models/          (model definitions)
        |- utils/           (model specific utilities.)
    |- encoder/         (Speaker Encoder models.)
        |- (same)
    |- vocoder/         (Vocoder models.)
        |- (same)
```

## 📜 License
🗣️TTS is released under the [MPL-2.0 license](https://opensource.org/licenses/MPL-2.0). See [LICENSE.txt](LICENSE.txt).

## 📖 Citation
If you use 🗣️TTS in your research, please cite it using [CITATION.cff](CITATION.cff).
