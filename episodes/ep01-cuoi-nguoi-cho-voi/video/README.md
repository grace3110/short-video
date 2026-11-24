# Video tập 1

- `ep01_final.mp4` — **bản đủ âm thanh** (Bước 6): nhạc nền + giọng Bác Trâu + tiếng động. Giọng Vịt Bảnh: chưa có (xem dưới).
- `ep01_cutout.mp4` — Bước 5 cách 2: hoạt hình cắt giấy (`../animate_cutout.py`), chưa âm thanh.
- `flow/` — Bước 5 cách 1: các shot làm bằng Flow/Veo (xem `../flow-veo-guide.md`).

## Âm thanh (`../audio/`)
| File | Nguồn |
|---|---|
| `music.mp3` | vidIQ AI music (25 credit), nhạc cartoon vui nhộn 15s |
| `trau_1.mp3`, `trau_2.mp3` | vidIQ voiceover, giọng "Trieu Duong" (nam miền Nam, trầm) |
| `vit_1.mp3`, `vit_2.mp3` | **chưa có** — giọng gợi ý: "Ninh Đôn" (nam trẻ). Bỏ file vào `audio/` rồi chạy lại `mix_audio.py` |
| `sfx/*.wav` | tự tạo bằng `../make_sfx.py` (xe, phanh, sấm, mưa, đề máy, lội nước, ting) |

Dựng lại: `python3 episodes/ep01-cuoi-nguoi-cho-voi/animate_cutout.py && python3 episodes/ep01-cuoi-nguoi-cho-voi/mix_audio.py`
