# Mã nguồn gallery danh tính tĩnh

> 🌐 Language / Ngôn ngữ: [English](README.md) | **Tiếng Việt**

`website_src/` là **frontend HTML/CSS/JavaScript song ngữ độc lập** trong dự án kỹ thuật CompactFaces, gồm Explore, About, Contact, tìm kiếm, bộ lọc, phân trang, deep link, điều khiển bàn phím/vuốt và popup năm ảnh. Không cần backend hay dịch vụ analytics.

Repository chỉ chứa **mã nguồn website**, không chứa ảnh đầu ra. Để hiển thị một bộ ảnh, người dùng cung cấp ImageFolder cục bộ có quyền sử dụng, `metadata.csv` và năm slot PNG. Builder tham chiếu xác minh SHA256 và tạo thumbnail WebP 400px cùng preview WebP 768px:

```bash
python3 -m pip install Pillow
python3 scripts/build_static_gallery.py   --train /path/to/compatible/data/train   --output /path/to/gallery
python3 -m http.server 8095 --bind 127.0.0.1 --directory /path/to/gallery
```

Chỉ thêm `--public` khi xuất website công khai; tùy chọn này bật URL dataset chuẩn, canonical tag cho từng trang, sitemap và cấu hình index/robots **trong thư mục đầu ra**, không sửa mã nguồn mẫu trong repository. Phải triển khai lại toàn bộ bản export (kể cả `robots.txt` và `sitemap.xml`) để công cụ tìm kiếm thấy cấu hình mới; chỉnh sửa mã nguồn không tự cập nhật website đang chạy. Vẫn phải kiểm tra website và các đường dẫn thực sự truy cập Public.

Builder hiện áp dụng **cấu trúc case study CompactFaces 1.0.0** (187 nhóm × 5 ảnh), dùng SHA256 và liên kết SOURCE để kiểm tra dữ liệu. Đây là ví dụ export tùy chọn; các kiểm thử CPU của repo hoạt động độc lập với `examples/`, không cần PNG.

## Ảnh và liên kết ngoài

- Website chỉ chứa **WebP dẫn xuất**; PNG 1024px gốc do chủ dữ liệu tự quản lý.
- `site-config.json` trong mã nguồn phục vụ **xem trước cục bộ**, chưa cấu hình URL tải dữ liệu. Dùng `--public` để tạo bản website có liên kết dataset và bật lập chỉ mục trong thư mục đầu ra. HTML nguồn có `noindex` cho chế độ xem trước.
- Liên kết Hugging Face và Kaggle được lấy từ cấu hình triển khai. Gallery cung cấp WebP xem trước, không phân phối trực tiếp PNG gốc.
- About giới thiệu bộ công cụ kỹ thuật. Contact chỉ soạn email `mailto:` kèm identity/slot, không gửi lên server, không upload ảnh cá nhân hay tự động gỡ dữ liệu.
- Git không chứa PNG nguồn, nhật ký tuyển chọn, thông tin xác thực hoặc trọng số model.

Có thể chạy website offline qua HTTP server cục bộ sau khi cung cấp catalog tương thích. CI kiểm mã nguồn không cần catalog hay dataset remote.
