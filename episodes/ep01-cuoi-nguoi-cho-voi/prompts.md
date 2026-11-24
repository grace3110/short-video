# Tập 1 — Prompt cho Flow (Bước 3–5)

Quy trình gợi ý: tạo **nhân vật nền trắng** (dễ tách nền ở Bước 4) + **background riêng** (không có nhân vật), rồi ghép & làm hoạt hình. Hoặc dùng prompt "Shot" bên dưới để Flow tạo thẳng cảnh hoàn chỉnh rồi chuyển thành video.

Style chung: `cute 3D Pixar-like cartoon style, vibrant colors, vertical 9:16`

## A. Nhân vật (nền trắng — để tách nền)

**A1. Vịt Bảnh trên xe máy, cười chê**
```
A young white cartoon duck with an orange beak, black sunglasses, a shiny black leather jacket, a red neck scarf and a slicked-up hair tuft, riding a shiny new red scooter, pointing and laughing mockingly, cute 3D Pixar-like style, full body, side view, plain pure white background
```

**A2. Vịt Bảnh ướt sũng, xe chết máy**
```
The same young white cartoon duck, completely soaked, feathers dripping, sunglasses crooked, leather jacket wet, panicking while kicking the starter of a red scooter, cute 3D Pixar-like style, full body, plain pure white background
```

**A3. Vịt Bảnh ngượng ngùng ôm xe máy**
```
The same young white cartoon duck, wet, cheeks blushing red with embarrassment, sheepish smile, hugging a red scooter, sitting, cute 3D Pixar-like style, full body, plain pure white background
```

**A4. Bác Trâu kéo xe gỗ**
```
A gentle old cartoon water buffalo with dark grey fur and curved horns, wearing a Vietnamese conical hat (non la), a brown ao ba ba shirt and a checkered khan ran scarf, chewing a straw, calmly pulling a small wooden cart loaded with hay, kind smile, cute 3D Pixar-like style, full body, side view, plain pure white background
```

**A5. Bác Trâu cận mặt mỉm cười**
```
Close-up portrait of the same gentle old cartoon water buffalo in a conical hat, chewing a straw, warm knowing smile, slightly squinting eyes, cute 3D Pixar-like style, plain pure white background
```

## B. Background (không có nhân vật)

**B1. Đường làng nắng**
```
A sunny Vietnamese countryside dirt road between green rice fields, bamboo trees and coconut palms, blue sky with fluffy clouds, no characters, cute 3D Pixar-like style, vertical 9:16
```

**B2. Đường làng mưa ngập**
```
The same Vietnamese countryside road completely flooded with muddy water, heavy rain, dark stormy sky, rice fields under water, no characters, cute 3D Pixar-like style, vertical 9:16
```

**B3. Sau mưa, cầu vồng**
```
The same flooded Vietnamese countryside road after rain, light drizzle, sun breaking through clouds, a bright rainbow over the rice fields, no characters, cute 3D Pixar-like style, vertical 9:16
```

## C. Prompt chuyển động (image → video trong Flow, mỗi shot 2–3s)

| Shot | Ảnh khởi đầu | Prompt chuyển động |
|---|---|---|
| 1 | A1 + A4 trên B1 | `The duck on the red scooter speeds in from the left, brakes next to the buffalo pulling the cart, points at the cart and laughs loudly. Static camera.` |
| 2 | A5 trên B1 | `The buffalo slowly chews the straw and smiles calmly; a puff of grey exhaust smoke blows across his face. Slow push-in.` |
| 3 | B2 | `The sky turns dark, heavy rain pours down, the road floods quickly, lightning flash. Static wide shot.` |
| 4 | A2 trên B2 | `The soaked duck repeatedly kicks the scooter starter, the engine sputters and dies, water splashes, sunglasses slide down his beak. Medium shot.` |
| 5 | A4 trên B2 | `The buffalo wades steadily through knee-deep floodwater pulling the floating wooden cart toward the camera, water rippling, determined kind face. Low angle tracking.` |
| 6 | A3 ngồi trên xe gỗ, A4 kéo, trên B3 | `The buffalo pulls the wooden cart through the water carrying the embarrassed duck hugging his scooter, the rainbow shines, camera slowly pulls back to a wide shot.` |

> Mẹo giữ nhân vật đồng nhất: tạo A1 và A4 trước, sau đó dùng chúng làm ảnh tham chiếu (Ingredients / reference) cho các ảnh còn lại.
