# Kiểm tra tệp dữ liệu giữa các nền tảng — CompactFaces 1.0.0

> 🌐 Language / Ngôn ngữ: [English](platform-integrity.md) | **Tiếng Việt**

CompactFaces sử dụng định danh `dangkhoa2016/compactfaces-synthetic-face-dataset` trên [Hugging Face](https://huggingface.co/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset) và [Kaggle](https://www.kaggle.com/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset). Đặc tả dataset gồm **187 danh tính tổng hợp, mỗi danh tính có năm ảnh tư thế/biểu cảm** (120 Core, 67 Additional Optional), tương ứng **935 PNG gốc** kích thước 1024 × 1024. JPEG Builder và WebP gallery chỉ là ảnh xem trước, không phải PNG gốc bổ sung.

## Đối chiếu các tệp thật sự đã tải

Hugging Face ImageFolder lưu `data/train/metadata.csv` và đường dẫn ảnh tương đối dưới `data/train/images/`. Kaggle lưu `metadata.csv` tại thư mục gốc cùng các thư mục `core_600png/images/` và `additional_optional_335png/images/`.

Tải CSV từ trang dataset chính thức của từng nền tảng, sau đó chạy:

```bash
sha256sum /path/to/hf/metadata.csv /path/to/kaggle/metadata.csv
python3 scripts/compare_platform_metadata.py /path/to/hf/metadata.csv /path/to/kaggle/metadata.csv
```

Lệnh thứ nhất tính SHA256 của toàn bộ từng CSV; hai hash giống nhau là bằng chứng hai CSV trùng byte. Lệnh thứ hai kiểm cấu trúc 187 danh tính/935 slot, cặp identity/slot, collection, liên kết SOURCE và đối chiếu **giá trị SHA256 PNG được ghi trong metadata**. Nó **không** so sánh giá trị mọi cột tùy ý (ví dụ review flags, prompt hay đường dẫn file); muốn kiểm hai CSV trùng toàn bộ cần đối chiếu hash CSV. **Cả hai phép kiểm này đều không đọc byte PNG từ cả hai máy chủ.**

## Kiểm byte PNG gốc

Nếu đã tải Hugging Face ImageFolder:

```bash
python3 scripts/verify_dataset.py /path/to/data/train --expected-images 935 --expected-families 187 --verify-images
```

Với cấu trúc thư mục Kaggle, attach dataset vào [notebook kiểm chứng CPU](https://www.kaggle.com/code/dangkhoa2016/compactfaces-synthetic-face-cpu-validation), đặt `MODE = "full"` và kiểm toàn bộ trạng thái trong báo cáo. Xem [Kiểm chứng](validation.vi.md).

Các phép kiểm chỉ đối chiếu tệp và metadata; không chứng minh tính duy nhất sinh trắc học, việc khuôn mặt không giống người thật hoặc khả năng tạo lại ảnh trùng pixel.

[Tải dữ liệu](platforms.vi.md) · [Cấu trúc dataset](DATASET_STRUCTURE.vi.md) · [Giới hạn tái lập](reproducibility.vi.md)
