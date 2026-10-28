# Cấu trúc dataset CompactFaces 1.0.0

> 🌐 Language / Ngôn ngữ: [English](DATASET_STRUCTURE.md) | **Tiếng Việt**

Dataset tham chiếu gồm **187 bộ danh tính tổng hợp và 935 PNG 1024×1024 đã duyệt**. Mỗi bộ có đúng **năm ảnh**:

| Slot | Nội dung |
|---|---|
| `SOURCE` | Chân dung tham chiếu nhìn thẳng, trung tính |
| `P1` | Quay sang trái |
| `P2` | Quay sang phải |
| `E1` | Biểu cảm mỉm cười |
| `E2` | Biểu cảm khó chịu |

**Core:** 120 bộ / 600 PNG. **Additional Optional:** 67 bộ / 335 PNG. Tổng 187 bộ đã bao gồm Additional Optional.

## Metadata

ImageFolder trên Hugging Face dùng `data/train/metadata.csv`; Kaggle Dataset Version 1 có `metadata.csv` ở thư mục gốc, bên cạnh `core_600png/images/` và `additional_optional_335png/images/`. Metadata có các trường `file_name`, `identity_key`, `collection`, `slot`, `sha256`, `source_sha256`. Các trường `archive_name` / `archive_file_name` ghi ánh xạ phân phối ban đầu, **không có nghĩa là phải chuẩn bị ZIP trên Kaggle**.

- Mỗi `identity_key` phải xuất hiện năm lần, đủ năm slot không trùng.
- Năm dòng của một bộ phải cùng collection và tham chiếu SHA256 của SOURCE.
- `sha256` dùng để kiểm **byte PNG thực tế**, không phải preview hoặc độ giống gương mặt.
- Metadata tạo ảnh và SOURCE lineage được phân phối với dataset; test CPU mẫu trên GitHub không cần tải toàn bộ chúng.

## Sử dụng đúng

Khi chia train/validation/test, hãy chia theo `identity_key` để tránh cùng danh tính rơi vào nhiều tập. Xem [cách kiểm chứng](validation.vi.md) trước khi sử dụng dữ liệu. Ảnh AI không bảo đảm tất cả danh tính khác nhau về sinh trắc, không nhận dạng được hoặc không tình cờ giống người thật.

[Nguồn tải](platforms.vi.md) · [Giấy phép](../LICENSE-NOTES.vi.md)
