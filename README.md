# Anima TrainFlow (Linux port)

Gradio web UI for training [Anima](https://huggingface.co/circlestone-labs/Anima)
LoRA adapters: dataset smart-crop (U²-Net), auto-tagging (WD EVA02-Large v3),
one-click kohya sd-scripts runs with live log + sample preview.

Ported from the Windows portable bundle
[ThetaCursed/Anima-TrainFlow-Portable](https://huggingface.co/datasets/ThetaCursed/Anima-TrainFlow-Portable)
(MIT). Original UI/trainer by ThetaCursed; this fork only adapts it for Linux.

## Changes vs the Windows portable

- `python_embeded/python.exe` → any system/venv python (edit `PORTABLE_PYTHON` in `app.py`)
- Default model paths → ComfyUI models layout (`diffusion_models/anima/`, `text_encoders/`, `vae/`)
- `ui.launch()` → `server_name="0.0.0.0"`, port `8877` (LAN-accessible web app)
- Removed Windows-only `bitsandbytes_windows/*.dll` loaders and `start_trainer.bat`

## Requirements

- Python 3.10+ with torch (CUDA), plus: `gradio onnxruntime opencv-python psutil toml pandas accelerate`
- Anima base DiT + Qwen3-0.6B text encoder + Qwen-Image VAE (point the UI fields at your local copies)
- kohya deps for sd-scripts: see `training/sd-scripts/requirements.txt`

## Run

```bash
python app.py   # serves http://0.0.0.0:8877
```

## Models (download separately)

See `models/README.md` — the two ONNX files (U²-Net ~176 MB, WD tagger ~1.26 GB)
are excluded from this repo to keep it light.

## License

MIT (inherited from the upstream portable bundle). `training/sd-scripts` keeps
its own license (Apache-2.0-style, kohya-ss).
