# Kiến trúc — bộ công cụ kiểm dataset độc lập

> 🌐 Language / Ngôn ngữ: [English](architecture.md) | **Tiếng Việt**

CompactFaces tách riêng **quá trình tạo dữ liệu**, **kiểm chứng chỉ đọc** và **trình bày trên website**. Người dùng có thể chạy validator mà không cần GPU hay tải bộ ảnh gốc.

## Sơ đồ hệ thống

~~~text
GPU tùy chọn (Mage-Flow-Turbo / Edit, Qwen, VAE)
       │ các ứng viên SOURCE / P1 / P2 / E1 / E2
       ▼
Tuyển chọn và kiểm chất lượng thủ công (không được tự động hóa trong repo)
       │ PNG 1024×1024 + metadata + SHA256
       ├──────────► ImageFolder (Hugging Face)
       ├──────────► Thư mục PNG + notebook CPU (Kaggle)
       └──────────► builder chỉ đọc ► WebP 400/768px ► website

Metadata / thư mục PNG ──► validator CPU ──► số lượng, slot, hash, lỗi
~~~

## Các thành phần chính

| Thành phần | Chức năng | Đầu vào → đầu ra |
|---|---|---|
| `scripts/verify_dataset.py` | Kiểm schema, năm slot, SHA256 ảnh tùy chọn | ImageFolder → báo cáo |
| `scripts/build_static_gallery.py` | Kiểm đầu vào rồi tạo WebP dẫn xuất | ImageFolder → website tĩnh |
| `notebooks/compactfaces_kaggle_cpu_validation.ipynb` | Hướng dẫn kiểm CPU trên Kaggle | dataset attach → báo cáo |
| `website_src/` | Giao diện, tìm kiếm, xem năm ảnh, soạn email liên hệ | catalog → trình duyệt |
| `scripts/reproduce_source_pose_example.sh` | Ví dụ inference GPU tùy chọn | model tương thích → hai PNG mẫu |

## Phạm vi trách nhiệm

- Validator **chỉ đọc**; SHA sai phải dừng, không âm thầm sửa hoặc sinh lại ảnh.
- GitHub **không chứa PNG gốc và model weights**; test cơ bản dùng metadata mẫu đi kèm.
- WebP là ảnh dẫn xuất nén mất dữ liệu, không thay thế PNG gốc.
- Contact chỉ soạn email bằng ứng dụng mail của người dùng; không tự upload hoặc bảo đảm gửi thành công.
- SHA256 xác nhận byte trùng nhau, **không** chứng minh tính duy nhất sinh trắc học, quyền sử dụng hoặc tạo ảnh trùng từng pixel.

[Bắt đầu](QUICKSTART.vi.md) · [Cấu trúc dataset](DATASET_STRUCTURE.vi.md) · [Model](MODEL_PROVENANCE.vi.md)
