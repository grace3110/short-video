# Ảnh tập 1

## Bước 3 → bỏ ảnh từ Flow vào `raw/`
Đặt tên đúng mã: `A1.png … A5.png` (nhân vật, nền trắng) và `B1.png … B3.png` (bối cảnh).

## Bước 4 — Tách nền (đã làm ✓)
Khuyên dùng chế độ AI (xóa luôn bóng đổ dưới chân):
```bash
pip install "rembg[cpu]"
python3 tools/remove_bg.py --ai episodes/ep01-cuoi-nguoi-cho-voi/images/raw episodes/ep01-cuoi-nguoi-cho-voi/images/cutout
```
Chế độ nhanh không cần AI (bỏ `--ai`) chỉ xóa nền trắng, còn sót bóng xám.
- Kết quả: `cutout/A1.png …` nền trong suốt, đã cắt sát nhân vật. Ảnh `B*` được bỏ qua (bối cảnh giữ nguyên).
- Còn sót viền trắng → tăng `--tol 30`. Ăn mất phần lông trắng của Vịt → giảm `--tol 10`.
- Nền không phải trắng tinh → dùng AI: `pip install "rembg[cpu]"` rồi thêm `--ai`.
- Không muốn chạy lệnh: dùng remove.bg, Canva "Xóa nền" hoặc CapCut "Xóa nền" cũng được, lưu PNG vào `cutout/`.
