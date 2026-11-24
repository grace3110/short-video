#!/usr/bin/env python3
"""Bước 6 — Ghép âm thanh vào video tập 1.

    python3 episodes/ep01-cuoi-nguoi-cho-voi/mix_audio.py

Vào : video/ep01_cutout.mp4, audio/music.mp3, audio/trau_*.mp3, audio/vit_*.mp3 (nếu có), audio/sfx/*.wav
Ra  : video/ep01_final.mp4
"""
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = HERE / "audio"

# (file, thời điểm bắt đầu giây, âm lượng, bộ lọc thêm)
CUES = [
    ("sfx/engine_rev.wav", 0.00, 0.55, ""),
    ("vit_1.mp3",          0.40, 1.60, ""),               # "Ha ha! Bác ơi…"
    ("sfx/brake.wav",      0.62, 0.25, ""),
    ("sfx/whoosh.wav",     1.90, 0.35, ""),
    ("trau_1.mp3",         2.10, 1.70, ""),               # "Ừ… từ từ mà đi cháu."
    ("sfx/engine_rev.wav", 2.85, 0.35, ""),               # Vịt phóng đi
    ("sfx/cough.wav",      4.35, 0.45, ""),
    ("sfx/thunder.wav",    4.72, 1.00, ""),
    ("sfx/thunder.wav",    5.02, 0.60, ""),
    ("sfx/rain.wav",       4.20, 0.40, "afade=t=in:d=0.8,afade=t=out:st=9.8:d=1.0"),
    ("sfx/start_fail.wav", 6.00, 1.10, ""),
    ("vit_2.mp3",          6.30, 1.60, ""),               # "Ơ… ơ… nổ đi mà!"
    ("sfx/whoosh.wav",     8.92, 0.30, ""),
    ("sfx/wade.wav",       9.00, 0.70, ""),
    ("trau_2.mp3",         9.30, 1.70, "atempo=1.15"),    # "Lên đây bác chở…"
    ("sfx/whoosh.wav",    11.92, 0.30, ""),
    ("sfx/wade.wav",      12.00, 0.35, ""),
    ("sfx/ting.wav",      12.38, 0.45, ""),
]
# Nhạc: vui nhộn → TẮT PHỤT lúc trời đổ mưa (4.6s) → vào lại ấm áp khi Bác Trâu tới (9.2s) → fade cuối
MUSIC_VOL = "if(lt(t,4.6),0.42,if(lt(t,9.2),0,0.36*min(1,(t-9.2)/0.8)))"


def main():
    inputs, filters, labels = ["-i", str(HERE / "video/ep01_cutout.mp4")], [], []
    inputs += ["-i", str(A / "music.mp3")]
    filters.append(f"[1:a]volume='{MUSIC_VOL}':eval=frame,afade=t=out:st=14.2:d=0.8[m]")
    labels.append("[m]")
    idx = 2
    for f, start, vol, extra in CUES:
        p = A / f
        if not p.exists():
            print(f"(bỏ qua {f} — chưa có file)")
            continue
        inputs += ["-i", str(p)]
        ms = int(start * 1000)
        chain = f"[{idx}:a]aformat=sample_rates=44100:channel_layouts=stereo,"
        chain += (extra + "," if extra else "") + f"volume={vol},adelay={ms}|{ms}[a{idx}]"
        filters.append(chain)
        labels.append(f"[a{idx}]")
        idx += 1
    filters.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest,"
                   "atrim=0:15,alimiter=limit=0.9,loudnorm=I=-14:TP=-1.5:LRA=11[out]")
    out = HERE / "video/ep01_final.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filters),
           "-map", "0:v", "-map", "[out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
           "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    print("✓", out)


if __name__ == "__main__":
    main()
