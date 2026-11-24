#!/usr/bin/env python3
"""Bước 4 — Tách nền trắng cho ảnh nhân vật (A1–A5).

Cách dùng:
    python3 tools/remove_bg.py <thư_mục_ảnh_vào> <thư_mục_ảnh_ra>

Mặc định: chỉ xóa vùng nền trắng NỐI LIỀN với mép ảnh (flood fill),
nên phần trắng bên trong nhân vật (lông vịt trắng, mắt...) được giữ lại.
Thêm --ai để dùng rembg (mô hình AI) nếu đã cài: pip install "rembg[cpu]".
Ảnh bối cảnh (B1–B3) không cần tách nền, script tự bỏ qua file tên bắt đầu bằng "B".
"""
import argparse
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def white_key(img: Image.Image, tol: int, feather: float) -> Image.Image:
    rgb = np.asarray(img.convert("RGB")).astype(np.int16)
    h, w, _ = rgb.shape
    # "gần trắng": mọi kênh >= 255 - tol và màu ít bão hòa
    near_white = (rgb.min(axis=2) >= 255 - tol) & ((rgb.max(axis=2) - rgb.min(axis=2)) <= tol)

    bg = np.zeros((h, w), dtype=bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if near_white[y, x] and not bg[y, x]:
                bg[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if near_white[y, x] and not bg[y, x]:
                bg[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < h and 0 <= nx < w and near_white[ny, nx] and not bg[ny, nx]:
                bg[ny, nx] = True; q.append((ny, nx))

    alpha = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8))
    if feather > 0:  # làm mềm viền, tránh răng cưa / viền trắng
        alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(feather))
    out = img.convert("RGBA")
    out.putalpha(alpha)
    return out


def ai_remove(img: Image.Image) -> Image.Image:
    from rembg import remove  # type: ignore
    return remove(img)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("dst")
    p.add_argument("--tol", type=int, default=18, help="độ lệch cho phép so với màu trắng (0-60)")
    p.add_argument("--feather", type=float, default=0.8, help="độ mềm viền (px)")
    p.add_argument("--ai", action="store_true", help="dùng rembg thay cho tách nền trắng")
    a = p.parse_args()

    src, dst = Path(a.src), Path(a.dst)
    dst.mkdir(parents=True, exist_ok=True)
    files = sorted(f for f in src.iterdir() if f.suffix.lower() in EXTS and not f.name.upper().startswith("B"))
    if not files:
        print(f"Không tìm thấy ảnh nhân vật trong {src}")
        return 1
    for f in files:
        img = Image.open(f)
        out = ai_remove(img) if a.ai else white_key(img, a.tol, a.feather)
        bbox = out.getchannel("A").getbbox()
        if bbox:  # cắt sát nhân vật, chừa lề 16px
            l, t, r, b = bbox
            out = out.crop((max(l - 16, 0), max(t - 16, 0), min(r + 16, out.width), min(b + 16, out.height)))
        target = dst / (f.stem + ".png")
        out.save(target)
        print(f"✓ {f.name} -> {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
