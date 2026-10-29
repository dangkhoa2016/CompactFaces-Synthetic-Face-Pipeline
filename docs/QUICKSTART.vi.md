# Bắt đầu — ưu tiên CPU

> 🌐 Language / Ngôn ngữ: [English](QUICKSTART.md) | **Tiếng Việt**

**Yêu cầu:** Git và Python 3.10+. Các lệnh CPU đầu không cần dataset, GPU, tải model hoặc thư viện Python ngoài.

## 1. Clone và kiểm ví dụ đi kèm

~~~bash
git clone https://github.com/dangkhoa2016/CompactFaces-Synthetic-Face-Pipeline.git
cd CompactFaces-Synthetic-Face-Pipeline
python3 scripts/verify_dataset.py examples --expected-images 10 --expected-families 2
python3 scripts/validate_repository.py
python3 scripts/validate_notebooks.py
~~~

Kỳ vọng: kiểm mã nguồn thành công và báo cáo notebook **DEMO_ONLY**. Bước này **không** kiểm 935 PNG gốc. Có thể kiểm cú pháp riêng: `python3 -m py_compile scripts/*.py`; `node --check website_src/app.js`; `bash -n scripts/reproduce_source_pose_example.sh`.

## 2. Kiểm đủ bộ dataset

Để kiểm toàn bộ dữ liệu, [thêm CompactFaces Dataset Version 1 trên Kaggle](platforms.vi.md), đặt `MODE = "full"` trong notebook CPU rồi chạy toàn bộ. Kaggle cung cấp trực tiếp ảnh PNG và metadata; **không cần tải hay giải nén ZIP**.

Nếu đã tải ImageFolder từ Hugging Face và có quyền truy cập, bạn cũng có thể kiểm các file cục bộ:

~~~bash
python3 scripts/verify_dataset.py /path/to/data/train --expected-images 935 --expected-families 187 --verify-images
~~~

Muốn xác minh toàn bộ byte ảnh phải có ảnh thật. Dùng [hướng dẫn kiểm chứng](validation.vi.md) cho ImageFolder hoặc Kaggle hiện tại. Không gọi DEMO_ONLY là FULL_PASS.

## 3. Gallery và ví dụ GPU tùy chọn

~~~bash
python3 -m pip install Pillow
python3 scripts/build_static_gallery.py --train /path/to/data/train --output ./compactfaces_gallery
python3 -m http.server 8095 --bind 127.0.0.1 --directory ./compactfaces_gallery
~~~

Gallery tạo preview WebP nén mất dữ liệu, không sửa PNG nguồn. Muốn chạy ví dụ sinh ảnh SOURCE/P2 mới, đọc [chuẩn bị model](MODEL_SETUP.vi.md). Không kỳ vọng tái tạo trùng byte bộ ảnh đã công bố.

**Muốn tự tạo ảnh trên Modal?** Sau khi chạy test CPU, xem [Model setup](MODEL_SETUP.vi.md) và [Hướng dẫn triển khai Modal](MODAL_DEPLOYMENT.vi.md). Không cần GPU để chạy các phép kiểm dữ liệu ở trên.

[Các nền tảng](platforms.vi.md) · [Khắc phục sự cố](troubleshooting.vi.md)
