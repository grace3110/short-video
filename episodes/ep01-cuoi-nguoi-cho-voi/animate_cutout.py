#!/usr/bin/env python3
"""Bước 5 (cách 2) — Dựng hoạt hình kiểu cắt giấy cho Tập 1 từ ảnh đã tách nền.

    python3 episodes/ep01-cuoi-nguoi-cho-voi/animate_cutout.py [--preview | --keyframes]

Ra: video/ep01_cutout.mp4 (1080x1920, 30fps, 15s, chưa có âm thanh — âm thanh là Bước 6).
"""
import math
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
RAW, CUT, OUT = HERE / "images/raw", HERE / "images/cutout", HERE / "video"
W, H, FPS, DUR = 1080, 1920, 30, 15.0
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
random.seed(7)


# ---------- tiện ích ----------
def ease(t):  # ease-in-out
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def ease_out_back(t, s=1.6):
    t = max(0.0, min(1.0, t)) - 1
    return t * t * ((s + 1) * t + s) + 1


def lerp(a, b, t):
    return a + (b - a) * t


def load_bg(name):
    im = Image.open(next(RAW.glob(name + ".*"))).convert("RGB")
    # cover 9:16, phóng 6% để cắt bỏ watermark ở góc
    s = max(W / im.width, H / im.height) * 1.06
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((l, t, l + W, t + H))


def load_cut(name, height):
    im = Image.open(CUT / f"{name}.png").convert("RGBA")
    s = height / im.height
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)


def zoomed(img, z, cx=0.5, cy=0.5):
    """Máy quay phóng to z lần quanh điểm (cx, cy)."""
    if abs(z - 1) < 1e-3:
        return img.copy()
    cw, ch = W / z, H / z
    l = min(max(cx * W - cw / 2, 0), W - cw)
    t = min(max(cy * H - ch / 2, 0), H - ch)
    return img.resize((W, H), Image.BILINEAR, box=(l, t, l + cw, t + ch))


def paste(canvas, sprite, x, y, scale=1.0, angle=0.0):
    """Dán sprite với (x, y) là điểm giữa-đáy."""
    sp = sprite
    if scale != 1.0:
        sp = sp.resize((max(1, round(sp.width * scale)), max(1, round(sp.height * scale))), Image.BILINEAR)
    if angle:
        sp = sp.rotate(angle, resample=Image.BICUBIC, expand=True)
    canvas.alpha_composite(sp, (round(x - sp.width / 2), round(y - sp.height)))


def shadow(canvas, x, y, w, alpha=90):
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse((x - w / 2, y - w * 0.07, x + w / 2, y + w * 0.07), fill=(0, 0, 0, alpha))
    canvas.alpha_composite(layer.filter(ImageFilter.GaussianBlur(14)))


def water(canvas, y, t, alpha=150):
    """Mặt nước lũ có gợn sóng từ y xuống đáy."""
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pts = [(x, y + 10 * math.sin(x / 70 + t * 5)) for x in range(0, W + 20, 20)]
    d.polygon(pts + [(W, H), (0, H)], fill=(120, 92, 60, alpha))
    for k in range(6):
        yy = y + 40 + k * 45
        off = (t * 60 + k * 97) % 200
        for x0 in range(-200, W, 200):
            d.arc((x0 + off, yy, x0 + off + 120, yy + 18), 200, 340, fill=(220, 200, 170, 120), width=3)
    canvas.alpha_composite(layer)


RAIN = [(random.uniform(0, W), random.uniform(0, H), random.uniform(0.7, 1.3)) for _ in range(260)]


def rain(canvas, t, density=1.0, alpha=120):
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    n = int(len(RAIN) * density)
    for x, y, sp in RAIN[:n]:
        yy = (y + t * 2600 * sp) % (H + 100) - 50
        xx = (x - t * 500 * sp) % W
        d.line((xx, yy, xx - 12 * sp, yy + 55 * sp), fill=(220, 230, 255, alpha), width=3)
    canvas.alpha_composite(layer)


NO_TEXT = "--keyframes" in sys.argv


def text(canvas, s, y, size=64, fill=(255, 255, 255), stroke=(0, 0, 0), sw=7, appear=1.0, box=False, cx=None):
    if appear <= 0 or NO_TEXT:
        return
    font = ImageFont.truetype(FONT, size)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    lines = s.split("\n")
    lh = size * 1.25
    widths = [d.textlength(l, font=font) for l in lines]
    if box:
        bw, bh = max(widths) + 80, lh * len(lines) + 50
        d.rounded_rectangle(((W - bw) / 2, y - 25, (W + bw) / 2, y - 25 + bh), 36, fill=(255, 255, 255, 235),
                            outline=(30, 30, 30, 255), width=6)
    for i, l in enumerate(lines):
        x0 = (W - widths[i]) / 2 if cx is None else cx - widths[i] / 2
        d.text((x0, y + i * lh), l, font=font, fill=fill, stroke_width=sw, stroke_fill=stroke)
    if appear < 1:  # bật lên
        s_ = ease_out_back(appear)
        bb = layer.getbbox()
        if bb:
            crop = layer.crop(bb)
            nw, nh = max(1, int(crop.width * s_)), max(1, int(crop.height * s_))
            layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
            cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
            layer.alpha_composite(crop.resize((nw, nh), Image.BILINEAR), (int(cx - nw / 2), int(cy - nh / 2)))
    canvas.alpha_composite(layer)


def speech(canvas, who, line, t0, t, y=170):
    """Phụ đề thoại dạng bong bóng, ở 1/3 trên để không đè nhân vật."""
    a = (t - t0) / 0.25
    if a <= 0:
        return
    text(canvas, line, y, size=58, fill=(25, 25, 25), stroke=(255, 255, 255), sw=0, appear=min(a, 1), box=True)
    text(canvas, who, y - 95, size=44, fill=(255, 214, 70), sw=6, appear=min(a, 1))


def smoke(canvas, t, x0, y0):
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for k in range(7):
        p = t - k * 0.06
        if p <= 0:
            continue
        r = 60 + p * 260
        x, y = x0 - p * 900 + k * 20, y0 - p * 120 + math.sin(k) * 40
        a = int(max(0, 170 * (1 - p / 1.4)))
        d.ellipse((x - r, y - r, x + r, y + r), fill=(150, 150, 150, a))
    canvas.alpha_composite(layer.filter(ImageFilter.GaussianBlur(18)))


# ---------- tài nguyên ----------
B1, B2, B3 = load_bg("B1"), load_bg("B2"), load_bg("B3")
B1_BLUR = B1.filter(ImageFilter.GaussianBlur(10))
B2 = ImageEnhance.Brightness(B2).enhance(0.85)
DUCK_RIDE = load_cut("A1", 900)
DUCK_WET = load_cut("A2", 1000)
DUCK_SHY = load_cut("A3", 900)
BUF_CART = load_cut("A4", 520)
BUF_FACE = load_cut("A5", 1750)


# ---------- các shot ----------
def shot1(t):  # 0–2s CHÊ: Vịt phóng vào, phanh, chỉ tay cười
    c = B1.convert("RGBA")
    c = zoomed(c, 1.04 + 0.02 * t).convert("RGBA")
    bx = 330 - 25 * t  # Trâu kéo xe đi chậm
    shadow(c, bx, 1440, 520)
    paste(c, BUF_CART, bx, 1450, angle=1.2 * math.sin(t * 9))
    p = ease_out_back(t / 0.7, 1.2)
    dx = lerp(1500, 720, p)
    tilt = -6 * math.exp(-((t - 0.75) ** 2) / 0.02)  # chúi đầu khi phanh
    laugh = 6 * abs(math.sin(t * 14)) if t > 0.8 else 0
    shadow(c, dx, 1830, 600)
    paste(c, DUCK_RIDE, dx, 1840 - laugh, angle=tilt)
    speech(c, "VỊT BẢNH", "Ha ha! Bác ơi,\nthời nào rồi còn kéo xe bò!", 0.35, t)
    return c


def shot2(t):  # 2–4s CHÊ: Cận Bác Trâu, Vịt phóng đi, khói phụt
    c = zoomed(B1_BLUR, 1.05).convert("RGBA")
    z = 1 + 0.06 * ease(t / 2)
    chew = 6 * math.sin(t * 12)
    face = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    paste(face, BUF_FACE, W / 2 + 20, H + 40 + chew)
    c.alpha_composite(face)
    c = zoomed(c, z, 0.5, 0.45).convert("RGBA")
    if t > 0.9:
        smoke(c, t - 0.9, W + 150, 1050)
    speech(c, "BÁC TRÂU", "Ừ… từ từ mà đi cháu.", 0.15, t)
    return c


def shot3(t):  # 4–6s BẤT NGỜ: trời tối, mưa, sấm
    k = ease(t / 0.8)
    c = Image.blend(B1, B2, k).convert("RGBA")
    c = zoomed(c, 1.08 - 0.04 * ease(t / 2)).convert("RGBA")
    rain(c, t, density=k)
    if 0.75 < t < 0.9 or 1.0 < t < 1.08:  # chớp
        c.alpha_composite(Image.new("RGBA", c.size, (255, 255, 255, 190)))
    text(c, "30 phút sau…", 820, size=96, fill=(255, 255, 255), sw=9, appear=(t - 0.3) / 0.3)
    return c


def shot4(t):  # 6–9s BẤT NGỜ: Vịt ướt, xe chết máy
    c = zoomed(B2, 1.12, 0.5, 0.7).convert("RGBA")
    kick = (t * 2.2) % 1  # mỗi ~0.45s đạp một cái
    jolt = 22 * math.exp(-kick * 10)
    shake = random.uniform(-6, 6) if kick < 0.2 else 0
    paste(c, DUCK_WET, W / 2 + shake, 1820 + jolt * 0.4, angle=jolt * 0.15)
    water(c, 1640, t)
    rain(c, t + 2, density=1.0)
    # khói "phụt" từ ống xả sau mỗi cú đạp: 3 cụm khói xám bốc lên, bay sang phải, tan dần
    layer = Image.new("RGBA", c.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    age = kick / 2.2  # giây kể từ cú đạp gần nhất
    for prev in (0, 1):  # cụm khói của cú đạp này và cú trước (còn đang tan)
        a_ = age + prev / 2.2
        if a_ > 0.9:
            continue
        for j in range(6):  # 6 cụm khói nhỏ, mỗi cụm xuất hiện trễ hơn một chút
            aj = a_ - j * 0.04
            if aj <= 0:
                continue
            r = 30 + aj * 150 + (j % 3) * 8
            x = 790 + aj * 160 + [0, 30, -20, 45, 10, -35][j]
            y = 1540 - aj * 330 - [0, 25, 40, 10, 55, 30][j]
            al = int(230 * max(0, 1 - aj / 0.85))
            d.ellipse((x - r, y - r, x + r, y + r), fill=(200, 200, 205, al))
            d.ellipse((x - r * 0.55, y - r * 0.7, x + r * 0.35, y + r * 0.2), fill=(245, 245, 248, al))
    c.alpha_composite(layer.filter(ImageFilter.GaussianBlur(14)))
    if age < 0.3:
        text(c, "PHỤT!", 1100, size=80, fill=(255, 255, 255), stroke=(50, 50, 50), sw=8, appear=age / 0.12, cx=860)
    speech(c, "VỊT BẢNH", "Ơ… ơ… nổ đi mà!", 0.3, t)
    return c


def shot5(t):  # 9–12s LẬT KÈO: Bác Trâu lội nước tới
    c = zoomed(B2, 1.06, 0.5, 0.6).convert("RGBA")
    p = ease(t / 2.4)
    x, s = lerp(1250, 560, p), lerp(0.9, 1.75, p)
    bob = 12 * math.sin(t * 7)
    paste(c, BUF_CART, x, 1760 + bob, scale=s, angle=1.5 * math.sin(t * 7))
    water(c, 1600, t, alpha=170)
    rain(c, t + 5, density=0.55)
    speech(c, "BÁC TRÂU", "Lên đây bác chở.\nXe bác bốn chân,\nkhông sợ ngập!", 0.4, t, y=150)
    return c


def shot6(t):  # 12–15s LẬT KÈO: chở Vịt về, cầu vồng, chữ kết
    z = 1.18 - 0.16 * ease(t / 2.6)
    c = B3.convert("RGBA")
    group = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gx = 520 - 60 * t
    bob = 8 * math.sin(t * 6)
    s = 1.35
    bw, bh = BUF_CART.width * s, BUF_CART.height * s
    paste(group, BUF_CART, gx, 1700 + bob, scale=s)
    # Vịt ôm xe máy ngồi trên thùng xe gỗ (phía phải của sprite)
    paste(group, DUCK_SHY, gx - bw / 2 + bw * 0.72, 1700 + bob - bh * 0.32, scale=0.42 * s, angle=2 * math.sin(t * 6 + 1))
    c.alpha_composite(group)
    water(c, 1610, t, alpha=120)
    c = zoomed(c, z, 0.5, 0.62).convert("RGBA")
    rain(c, t + 9, density=0.15, alpha=80)
    text(c, "Cười người chớ vội…", 250, size=92, fill=(255, 236, 120), sw=10, appear=(t - 0.4) / 0.35)
    text(c, "hôm trước cười người,\nhôm sau người cười", 400, size=54, sw=7, appear=(t - 1.0) / 0.35)
    if t > 2.6:  # fade đen cuối
        c.alpha_composite(Image.new("RGBA", c.size, (0, 0, 0, int(255 * min(1, (t - 2.6) / 0.4)))))
    return c


SHOTS = [(0, 2, shot1), (2, 4, shot2), (4, 6, shot3), (6, 9, shot4), (9, 12, shot5), (12, 15, shot6)]


def frame_at(t):
    for i, (a, b, fn) in enumerate(SHOTS):
        if a <= t < b or (i == len(SHOTS) - 1 and t >= a):
            img = fn(t - a)
            # chuyển cảnh: chớp trắng nhẹ 0.1s đầu mỗi shot (trừ shot đầu và shot 3 đã có hiệu ứng)
            if i not in (0, 2) and t - a < 0.1:
                img.alpha_composite(Image.new("RGBA", img.size, (255, 255, 255, int(160 * (1 - (t - a) / 0.1)))))
            return img.convert("RGB")


def main():
    OUT.mkdir(exist_ok=True)
    if NO_TEXT:  # khung đầu cho Flow "Frames to Video" (không chữ, không mưa chớp)
        kdir = HERE / "images/keyframes"
        kdir.mkdir(exist_ok=True)
        for i, (a, b, fn) in enumerate(SHOTS, 1):
            t = {1: 0.9, 2: 0.3, 3: 0.0, 4: 0.5, 5: 1.2, 6: 0.0}[i]
            fn(t).convert("RGB").save(kdir / f"shot{i}.jpg", quality=92)
        print("✓", kdir)
        return
    if "--preview" in sys.argv:  # ảnh tĩnh giữa mỗi shot
        for a, b, fn in SHOTS:
            frame_at((a + b) / 2 + 0.3).save(OUT / f"preview_{a:02d}s.jpg", quality=85)
        return
    out = OUT / "ep01_cutout.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "21", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)],
                          stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        ff.stdin.write(frame_at(i / FPS).tobytes())
        if i % 60 == 0:
            print(f"{i}/{n}", flush=True)
    ff.stdin.close()
    ff.wait()
    print("✓", out)


if __name__ == "__main__":
    main()
