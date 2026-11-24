#!/usr/bin/env python3
"""Bước 6 — Tạo tiếng động (SFX) bằng code, không cần tải gì: ra audio/sfx/*.wav (44.1kHz mono)."""
import wave
from pathlib import Path

import numpy as np

SR = 44100
OUT = Path(__file__).resolve().parent / "audio/sfx"
rng = np.random.default_rng(3)


def save(name, x):
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.9
    OUT.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUT / f"{name}.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def t(d):
    return np.arange(int(SR * d)) / SR


def lowpass(x, a):  # bộ lọc 1 cực đơn giản
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc += a * (v - acc); y[i] = acc
    return y


def env(n, att, rel):
    e = np.ones(n); a, r = int(att * SR), int(rel * SR)
    e[:a] = np.linspace(0, 1, a); e[-r:] *= np.linspace(1, 0, r)
    return e


# xe máy rồ ga "brừm brừm": sóng răng cưa tần số thấp, ga tăng dần
d = 1.6; tt = t(d)
f = 70 + 90 * np.clip(tt / 1.2, 0, 1) ** 0.6 + 12 * np.sin(2 * np.pi * 6 * tt)
ph = 2 * np.pi * np.cumsum(f) / SR
eng = ((ph / (2 * np.pi)) % 1 * 2 - 1) + 0.5 * np.sign(np.sin(ph * 0.5))
eng = lowpass(eng + 0.3 * rng.standard_normal(len(tt)), 0.15) * env(len(tt), 0.05, 0.4)
save("engine_rev", eng)

# phanh "kíttt"
tt = t(0.45)
sq = np.sin(2 * np.pi * (2400 + 300 * np.sin(2 * np.pi * 30 * tt)) * tt) * env(len(tt), 0.01, 0.2)
save("brake", sq + 0.2 * rng.standard_normal(len(tt)) * env(len(tt), 0.01, 0.2))

# ho "khụ khụ"
cough = np.zeros(int(SR * 0.7))
for st in (0.0, 0.33):
    n = int(SR * 0.18); s = int(SR * st)
    burst = lowpass(rng.standard_normal(n), 0.25) * np.exp(-np.linspace(0, 6, n))
    cough[s:s + n] += burst
save("cough", cough)

# sấm "đùng": tiếng nổ + rền dài
tt = t(2.2)
crack = rng.standard_normal(len(tt)) * np.exp(-tt * 18)
rumble = lowpass(rng.standard_normal(len(tt)), 0.008) * 25 * (np.exp(-tt * 1.6)) * (1 + 0.5 * np.sin(2 * np.pi * 3 * tt))
save("thunder", crack * 0.6 + rumble)

# mưa rào: nhiễu trắng lọc + giọt lách tách
tt = t(11.0)
rain = lowpass(rng.standard_normal(len(tt)), 0.35) * 0.5
for _ in range(1800):
    p = rng.integers(0, len(tt) - 400)
    rain[p:p + 400] += rng.standard_normal(400) * np.exp(-np.linspace(0, 12, 400)) * 0.8
save("rain", rain)

# đề máy "tạch tạch… phụt" (lặp 6 lần ~0.45s)
d = 2.8; x = np.zeros(int(SR * d))
for k in range(6):
    s = int(SR * k * 0.4545)
    n = int(SR * 0.08)
    x[s:s + n] += rng.standard_normal(n) * np.exp(-np.linspace(0, 8, n))           # tạch
    s2 = s + int(SR * 0.1); n2 = int(SR * 0.22)
    tt2 = np.arange(n2) / SR
    puff = lowpass(rng.standard_normal(n2), 0.06) * 6 * np.exp(-tt2 * 14)          # phụt
    puff += 0.6 * np.sin(2 * np.pi * 55 * tt2) * np.exp(-tt2 * 12)
    x[s2:s2 + n2] += puff
save("start_fail", x)

# lội nước "ì oạp": các cú té nước trầm
d = 3.0; x = np.zeros(int(SR * d))
for k in range(5):
    s = int(SR * (0.15 + k * 0.6)); n = int(SR * 0.35)
    tt2 = np.arange(n) / SR
    sweep = np.sin(2 * np.pi * (300 - 500 * tt2) * tt2) * np.exp(-tt2 * 9)
    x[s:s + n] += lowpass(rng.standard_normal(n), 0.2) * np.exp(-tt2 * 10) + 0.5 * sweep
save("wade", x)

# "ting" kết: chuông 2 nốt
tt = t(1.6)
ting = sum(a * np.sin(2 * np.pi * f_ * tt) * np.exp(-tt * dcy) for f_, a, dcy in
           [(1568, 1, 3), (3136, 0.4, 5), (2093, 0.6, 3.5)])
ting[: int(SR * 0.12)] *= 0.0
ting2 = sum(a * np.sin(2 * np.pi * f_ * tt) * np.exp(-tt * dcy) for f_, a, dcy in [(2093, 1, 3), (4186, 0.3, 5)])
save("ting", np.concatenate([ting2[: int(SR * 0.12)], ting[int(SR * 0.12):]]))

# "vút" chuyển cảnh
tt = t(0.35)
save("whoosh", lowpass(rng.standard_normal(len(tt)), 0.1) * np.sin(np.pi * tt / 0.35) ** 2)
print("✓", OUT)
