# Tài liệu — bộ công cụ kỹ thuật CompactFaces

> 🌐 Language / Ngôn ngữ: [English](README.md) | **Tiếng Việt**

**Người mới nên đọc [Bắt đầu](QUICKSTART.vi.md)** để chạy công cụ. GitHub có ví dụ CPU độc lập; model weights và ảnh gốc phân phối riêng.

| Mục tiêu | Tài liệu |
|---|---|
| Chạy ngay khi chưa có dataset | [Bắt đầu](QUICKSTART.vi.md) |
| Tìm/attach Dataset Version 1 trên Kaggle | [Các nền tảng](platforms.vi.md) |
| Hiểu thành phần mã nguồn | [Kiến trúc](architecture.vi.md) |
| Hiểu quy trình và năm slot | [Pipeline](pipeline.vi.md) · [Cấu trúc dataset](DATASET_STRUCTURE.vi.md) |
| Tải model cho ví dụ GPU | [Chuẩn bị model](MODEL_SETUP.vi.md) · [Nguồn model](MODEL_PROVENANCE.vi.md) |
| Tạo Volume và chạy GPU trên Modal | [Hướng dẫn Modal](MODAL_DEPLOYMENT.vi.md) |
| Kiểm SHA256 PNG và provenance thực tế | [Kiểm chứng](validation.vi.md) |
| Tạo/xem preview WebP | [Gallery](gallery.vi.md) |
| Hiểu giới hạn | [Khả năng tái lập](reproducibility.vi.md) · [Metadata hai nền tảng](platform-integrity.vi.md) |
| Xử lý lỗi | [Khắc phục sự cố](troubleshooting.vi.md) |
| Đọc giấy phép và phạm vi phân phối | [Chính sách phát hành](RELEASE_POLICY.vi.md) · [Giấy phép](../LICENSE-NOTES.vi.md) |
| Kiểm mã nguồn trước khi chia sẻ | [Checklist chất lượng](release-checklist.vi.md) |

**Case study:** 187 danh tính tổng hợp × 5 ảnh = 935 PNG 1024×1024 đã duyệt (120 Core, 67 Additional Optional). Test CPU chỉ đọc có thể chạy không cần ảnh gốc. Ví dụ GPU **không** tái tạo toàn bộ ảnh được tuyển chọn thủ công.

[README GitHub](../README.vi.md) · [Notebook Kaggle song ngữ](../notebooks/compactfaces_kaggle_cpu_validation.ipynb)
