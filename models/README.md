# Models (download separately)

The app expects these files under `models/`:

## u2net — smart crop saliency model
- `models/u2net/u2net.onnx` (~176 MB)
- Source: https://github.com/xuebinqin/U-2-Net (ONNX export; also bundled with rembg releases)

## WD EVA02-Large Tagger v3 — auto-tagging
- `models/wd-eva02-large-tagger-v3/model.onnx` (~1.26 GB)
- Plus `config.json`, `selected_tags.csv`, `sw_jax_cv_config.json` (tracked in this repo)
- Source: SmilingWolf/wd-eva02-large-tagger-v3 on Hugging Face
  https://huggingface.co/SmilingWolf/wd-eva02-large-tagger-v3

```bash
# example
huggingface-cli download SmilingWolf/wd-eva02-large-tagger-v3 model.onnx --local-dir models/wd-eva02-large-tagger-v3
```

Anima base DiT / Qwen3-0.6B text encoder / Qwen-Image VAE are NOT included —
point the UI at your local copies (defaults target a ComfyUI layout under
/home/jeffrey/comfyui/ComfyUI/models/).
