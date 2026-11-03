# CompactFaces 1.0.0 — Phân phối dataset

> 🌐 Language / Ngôn ngữ: [English](RELEASE_SYNC.md) | **Tiếng Việt**

## Thành phần dữ liệu

CompactFaces gồm 187 danh tính tổng hợp: **120 Core (600 PNG)** và **67 Additional Optional (335 PNG)**. Mỗi nhóm có SOURCE, P1, P2, E1 và E2. Ảnh gốc là PNG 1024 × 1024. Kaggle Builder có ảnh JPEG xem trước; công cụ gallery có thể tạo WebP thumbnail 400px và preview 768px. Những ảnh dẫn xuất này không phải PNG gốc bổ sung.

## Địa chỉ chính thức

- [Dataset Hugging Face](https://huggingface.co/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset) — PNG ImageFolder và metadata.
- [Dataset Kaggle](https://www.kaggle.com/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset) — thư mục PNG, metadata và tài nguyên Builder.
- [Notebook CPU Kaggle](https://www.kaggle.com/code/dangkhoa2016/compactfaces-synthetic-face-cpu-validation) — kiểm SHA256 tệp và provenance.
- [Gallery CompactFaces](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/) — ảnh WebP xem trước.
- [Bộ công cụ GitHub](https://github.com/dangkhoa2016/CompactFaces-Synthetic-Face-Pipeline) — mã nguồn, script và tài liệu.

## Kiểm chứng

Các nền tảng có thể khác bố cục thư mục và cách đánh số phiên bản. Cần tải tệp thực tế rồi làm theo [Kiểm tra giữa các nền tảng](platform-integrity.vi.md) và [Kiểm chứng](validation.vi.md) để so metadata và SHA256 PNG. Không kết luận dữ liệu trên hai máy chủ trùng byte chỉ vì cùng tên hoặc một câu mô tả.

Giấy phép phần mềm GitHub không thay thế giấy phép riêng của ảnh và model. Xem [Chính sách phân phối](RELEASE_POLICY.vi.md).
