# Bước 5 (cách 1) — Làm hoạt hình trong Google Flow (Veo)

Khung đầu cho từng shot nằm ở `images/keyframes/shot1.jpg … shot6.jpg`
(nhân vật đã ghép sẵn vào bối cảnh, không chữ). Tải 6 ảnh này về máy trước.

## Dán đoạn này vào Claude in Chrome (hoặc tự làm theo)

```text
Mở https://flow.google.com/, vào project "Cười người chớ vội - Tập 1".
Với mỗi shot dưới đây: chọn chế độ "Frames to Video", tải ảnh khung đầu tương ứng, khung dọc 9:16,
dán prompt, tạo video 8 giây. Tạo xong shot nào thì tải video về, đặt tên shot1.mp4 … shot6.mp4.
Không tạo lời thoại bằng giọng nói (thoại sẽ thêm ở bước âm thanh).

shot1.jpg → The cocky white duck on the red scooter laughs loudly, points his wing at the old water buffalo pulling the hay cart, his body bounces with laughter; the buffalo keeps walking calmly. Static camera, cute 3D Pixar style, no text.

shot2.jpg → The old water buffalo in the conical hat slowly chews the straw and gives a warm knowing smile; a puff of grey exhaust smoke drifts across his face from the right. Slow push-in, cute 3D Pixar style, no text.

shot3.jpg → The sunny sky quickly turns dark and stormy, heavy rain pours down, a lightning flash, the dirt road floods with muddy water. Static wide shot, cute 3D Pixar style, no characters, no text.

shot4.jpg → The soaked duck panics and repeatedly kicks the scooter starter, the engine sputters and puffs smoke but dies, muddy water splashes, his sunglasses slide down his beak. Heavy rain. Medium shot, cute 3D Pixar style, no text.

shot5.jpg → The old water buffalo wades steadily through the floodwater toward the camera pulling the floating wooden cart, water rippling around his legs, calm kind smile. Rain. Low-angle tracking shot, cute 3D Pixar style, no text.

shot6.jpg → The buffalo pulls the wooden cart through shallow water carrying the embarrassed blushing duck hugging his red scooter; the rain stops, sunlight breaks through, the rainbow glows. Camera slowly pulls back to a wide shot, cute 3D Pixar style, no text.
```

## Ghép lại
Kịch bản 15s nhưng Veo cho mỗi shot 8s → cắt mỗi shot lấy đoạn đẹp nhất:
shot1 2s · shot2 2s · shot3 2s · shot4 3s · shot5 3s · shot6 3s.
Upload 6 file `shot*.mp4` vào `video/flow/` trên GitHub, Claude sẽ cắt ghép + thêm phụ đề.
