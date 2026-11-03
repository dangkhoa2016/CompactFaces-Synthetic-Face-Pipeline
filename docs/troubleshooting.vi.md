# Khắc phục sự cố và câu hỏi thường gặp

> 🌐 Language / Ngôn ngữ: [English](troubleshooting.md) | **Tiếng Việt**

| Hiện tượng | Cách xử lý |
|---|---|
| Test CPU chạy được nhưng chưa kiểm 935 ảnh | Đúng thiết kế: repo chỉ có mười dòng metadata mẫu. Tải dataset khi có quyền hoặc chạy Kaggle FULL. |
| Không tìm thấy dataset trên Kaggle | Vào **Input → Add Input → Datasets**, tìm **compactfaces-synthetic-face-dataset**, xác nhận dangkhoa2016, chọn Version 1 và kiểm quyền truy cập. |
| Notebook báo DEMO_ONLY | Chưa nhận dataset. Đặt `MODE = "full"` để bắt buộc có input và thấy lỗi chỉ rõ file còn thiếu. |
| Không tìm thấy ảnh sau khi thêm dataset | Mở mục Input, kiểm tra `metadata.csv` cùng `core_600png/images/` và `additional_optional_335png/images/`; notebook đọc dữ liệu trong thư mục trực tiếp. |
| FULL báo nhiều dataset root | Đặt `DATASET_DIR` bằng thư mục /kaggle/input/... chính xác trong thanh Input. |
| Sai SHA256 hoặc thiếu góc mặt | Dừng, kiểm byte ảnh, metadata và slot. Không ghi đè ảnh được tuyển chọn. |
| GPU không tải được model | Kiểm đúng biến thể, SHA256, vai trò file Safetensors và bản `sd-cli` tương thích theo [chuẩn bị model](MODEL_SETUP.vi.md). |
| Gallery trống ảnh | Chạy qua HTTP bằng `python3 -m http.server`, kiểm catalog đã xuất và relative path. |
| Nút Contact không gửi email | Nút chỉ soạn email; cần cài ứng dụng mail hoặc tự gửi nội dung. |
| GitHub Action không có step/kết quả | Kiểm quyền runner/billing và commit cụ thể; không có job không có nghĩa là test PASS. |

Liên hệ quyền riêng tư hoặc yêu cầu gỡ ảnh: **i.am@dangkhoa.dev**, kèm mã identity/slot cụ thể. Không đưa token, ảnh cá nhân hoặc file nhạy cảm lên issue công khai.

**Lỗi Modal:** xem [Triển khai GPU Modal](MODAL_DEPLOYMENT.vi.md) để phân biệt sai SHA256, build CUDA lỗi và runtime inference lỗi.

[Bắt đầu](QUICKSTART.vi.md) · [Kiểm chứng](validation.vi.md)
