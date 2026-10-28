# Tải và sử dụng dữ liệu CompactFaces

> 🌐 Language / Ngôn ngữ: [English](platforms.md) | **Tiếng Việt**

Mã nguồn GitHub, ảnh gốc và website gallery là **các tài nguyên riêng biệt**. Test CPU cơ bản không cần tài khoản hay tải dataset.

## Các địa chỉ chính thức

| Tài nguyên | Liên kết | Nội dung |
|---|---|---|
| GitHub | [Mã nguồn pipeline](https://github.com/dangkhoa2016/CompactFaces-Synthetic-Face-Pipeline) | script, metadata mẫu, tài liệu, notebook |
| Hugging Face | [ImageFolder CompactFaces](https://huggingface.co/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset) | PNG gốc và metadata |
| Kaggle | [Dataset CompactFaces](https://www.kaggle.com/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset) | Version 1: 187 danh tính, 935 PNG và metadata |
| Notebook Kaggle | [Notebook kiểm CPU](https://www.kaggle.com/code/dangkhoa2016/compactfaces-synthetic-face-cpu-validation) | giao diện kiểm chứng |
| Website | [Gallery](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/) | WebP preview, không phải PNG gốc |

## Cách attach dataset trên Kaggle

1. Mở **notebook CPU** ở trên, chọn **Copy & Edit**, hoặc import notebook của repository.
2. Bên phải chọn **Input → Add Input** (hoặc **Add Data**) → **Datasets**.
3. Tìm **compactfaces-synthetic-face-dataset**, xác nhận tác giả **dangkhoa2016**, chọn **Version 1**, rồi **Add**.
4. Chọn **Accelerator: None**. Sau khi thêm dataset, Kaggle cung cấp `metadata.csv` và các thư mục `core_600png/images/`, `additional_optional_335png/images/`, `collection_builder_187/WEB_COLLECTION_BUILDER/previews/` tại `/kaggle/input/compactfaces-synthetic-face-dataset/`. **Bạn không cần chuẩn bị hoặc giải nén ZIP**; notebook đọc trực tiếp các tệp đã có.
5. Đặt `MODE = "full"` để bắt buộc kiểm dữ liệu thật rồi chạy toàn bộ. Để `DATASET_DIR = ""` cho tự dò, hoặc nhập path notebook tìm được nếu có nhiều dataset.
6. Đọc `FULL_PASS` và số PNG đã kiểm SHA256. `DEMO_ONLY` chỉ kiểm metadata mẫu, không kiểm PNG thật.

## Kiểm trên máy tính riêng

Với ImageFolder tương thích có `metadata.csv`:

~~~bash
python3 scripts/verify_dataset.py /path/to/data/train --expected-images 935 --expected-families 187 --verify-images
~~~

Ví dụ ImageFolder trong dataset card chung dùng layout `data/train/` của Hugging Face và **không thể chạy nguyên trạng với các thư mục đã giải nén trên Kaggle**. Với Kaggle Dataset Version 1, hãy dùng notebook FULL ở trên: notebook tự ánh xạ thư mục thực, đọc PNG/metadata và ghi rõ những phép kiểm cấp ZIP không áp dụng là SKIPPED. Xem [Kiểm chứng](validation.vi.md) và [Giấy phép](../LICENSE-NOTES.vi.md).
