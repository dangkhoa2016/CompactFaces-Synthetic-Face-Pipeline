# Tạo và sử dụng gallery WebP tĩnh

> 🌐 Language / Ngôn ngữ: [English](gallery.md) | **Tiếng Việt**

**Website mẫu:** [Gallery CompactFaces](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/). Website hiển thị WebP preview; PNG gốc 1024×1024 được lưu ở kênh riêng.

## Yêu cầu và cách build

Cần ImageFolder năm slot có `metadata.csv`, Python 3.10+ và Pillow:

~~~bash
python3 -m pip install Pillow
python3 scripts/build_static_gallery.py --train /path/to/data/train   --output ./compactfaces_gallery --workers 4
python3 -m http.server 8095 --bind 127.0.0.1 --directory ./compactfaces_gallery
~~~

Để tạo bản xuất **sẵn cấu hình Public**, thêm `--public` vào lệnh build. Tùy chọn này ghi link chuẩn Hugging Face/Kaggle, bật cấu hình index/robots công khai và không sửa `website_src/`. **Lệnh không triển khai website và không xác minh quyền truy cập thực tế trên mạng.** Lệnh mặc định dành cho xem trước cục bộ.

Mở http://127.0.0.1:8095/ bằng trình duyệt. Không mở file HTML trực tiếp vì gallery fetch JSON catalog qua HTTP.

## Website đầu ra có gì?

- Thumbnail WebP 400px và preview 768px cho từng ảnh (không chứa PNG nguồn).
- Tìm kiếm danh tính, lọc Core/Additional, xem năm slot, sáng/tối và ngôn ngữ Anh/Việt.
- Trang About/Contact chạy trên trình duyệt. Yêu cầu gỡ ảnh **chỉ chuẩn bị bản nháp email**; phải có ứng dụng mail để thực sự gửi.
- Cấu hình `site-config.json`; kiểm URL bên ngoài và tùy chọn lập chỉ mục trước khi công bố.

Builder kiểm SHA256 của từng PNG trước khi xử lý. WebP cũ **chỉ được tái sử dụng** nếu cache đi kèm khớp SHA256 PNG nguồn, phiên bản Pillow, tham số mã hóa và SHA256 của WebP thực tế. Cache thiếu hoặc lỗi sẽ kích hoạt tạo lại; `--force` luôn tạo mới. Báo cáo build tách số WebP tạo mới và số cache hit đã kiểm chứng.

WebP là ảnh dẫn xuất nén mất dữ liệu. Chỉ upload khi có quyền phân phối; builder không sửa PNG gốc. Mẫu xem trước cục bộ có `noindex`; bản xuất với `--public` sẽ bật lập chỉ mục và dùng liên kết dataset chính thức.

[Kiến trúc](architecture.vi.md) · [Giấy phép](../LICENSE-NOTES.vi.md)
