# ==========================================
# FOLDER BROWSER + LORA-REVIEW IMPORT (Sophia, 2026-09-18)
# ==========================================
import urllib.request
import urllib.error
import os
from pathlib import Path
import json
import shutil
import subprocess

BROWSE_ROOTS = [
    "/home/jeffrey",                      # GX10 home (run datasets, exports)
    "/home/jeffrey/anima-trainflow/training/output",
]
BROWSE_BLOCK = {"/home/jeffrey/.venv", "/home/jeffrey/comfyui/ComfyUI",
                "/home/jeffrey/lora_archive", "/home/jeffrey/.cache"}
IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

LORA_REVIEW_API = os.environ.get("LORA_REVIEW_API", "http://192.168.50.113:8300")

def _safe_dir(p: Path):
    rp = p.resolve()
    if not rp.is_dir():
        return None
    for b in BROWSE_BLOCK:
        try:
            if rp == Path(b) or b in rp.parents:
                return None
        except (ValueError, OSError):
            pass
    return rp

def _count_images(p: Path) -> int:
    try:
        return sum(1 for f in p.iterdir() if f.is_file() and f.suffix.lower() in IMG_EXTS)
    except OSError:
        return 0

def browse_dir(current: str):
    """List subdirs + image counts + existing captions of `current`."""
    base = _safe_dir(Path(current or "/home/jeffrey"))
    if base is None:
        return "❌ Invalid or blocked path", "", gr.update(choices=[], value=None)
    entries = []
    try:
        for d in sorted(base.iterdir(), key=lambda x: x.name.lower()):
            if d.is_dir() and not d.name.startswith("."):
                n = _count_images(d)
                txt = sum(1 for f in d.iterdir() if f.is_file() and f.suffix == ".txt")
                mark = f" 🏷️{txt}" if txt else ""
                entries.append(f"📁 {d.name}/  [{n} img{mark}]")
    except OSError as e:
        return f"❌ {e}", "", gr.update(choices=[], value=None)
    n_here = _count_images(base)
    log = f"📂 {base}  — {n_here} images here" + (f", {len(entries)} subfolders" if entries else "")
    return log, str(base), gr.update(choices=entries or ["(no subfolders)"], value=None)

def browse_pick(current_log: str, base_path: str, picked: str):
    if not picked or picked.startswith("("):
        return current_log, base_path
    name = picked.split("📁 ", 1)[1].split("/")[0].strip()
    return current_log, str(Path(base_path) / name)

def open_picked_dataset(base_path: str, current_log: str):
    """Set dataset_path to base_path if it holds images."""
    n = _count_images(Path(base_path))
    if n == 0:
        return current_log + "\n⚠️ No images in " + base_path, gr.update()
    return current_log + f"\n✅ Dataset set: {base_path} ({n} images)", gr.update(value=base_path)

def list_lora_review_datasets():
    try:
        with urllib.request.urlopen(f"{LORA_REVIEW_API}/api/datasets", timeout=8) as r:
            ds = json.load(r)["datasets"]
    except Exception as e:
        return gr.update(choices=[f"(error: {e})"], value=None), ""
    items = []
    for d in ds:
        c = d.get("counts", {})
        flag = " ✅trained" if d.get("trained") else ""
        items.append(f"{d['name']}  [{c.get('keep',0)} keep / {c.get('delete',0)} del{flag}]")
    return gr.update(choices=items, value=None), f"{len(items)} datasets on lora-review ({LORA_REVIEW_API})"

def import_lora_review_dataset(picked: str, current_log: str):
    if not picked or picked.startswith("("):
        return current_log, gr.update()
    name = picked.split("  [")[0].strip()
    log = current_log
    try:
        req = urllib.request.Request(
            f"{LORA_REVIEW_API}/api/datasets/{name}/export?mode=keep",
            method="POST")
        with urllib.request.urlopen(req, timeout=300) as r:
            total = int(r.headers.get("Content-Length", 0))
            tmp = Path("/tmp") / f"lr_export_{name}.tar.gz"
            with open(tmp, "wb") as f:
                while True:
                    chunk = r.read(1 << 20)
                    if not chunk: break
                    f.write(chunk)
        log += f"\n⬇️ Exported {name}: {tmp.stat().st_size/1e6:.1f} MB"
        dest = Path("/home/jeffrey/lora_datasets_imported") / name
        if dest.exists(): shutil.rmtree(dest)
        dest.mkdir(parents=True)
        subprocess.run(["tar", "xzf", str(tmp), "-C", str(dest)], check=True)
        tmp.unlink()
        n = _count_images(dest)
        txt = sum(1 for f in dest.iterdir() if f.is_file() and f.suffix == ".txt")
        log += f"\n📦 Imported to {dest}: {n} images, {txt} captions"
        return log + f"\n✅ Ready — dataset path filled in.", gr.update(value=str(dest))
    except Exception as e:
        return log + f"\n❌ Import failed: {e}", gr.update()
