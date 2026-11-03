# Quy trình tạo bộ năm ảnh tư thế và biểu cảm

> 🌐 Language / Ngôn ngữ: [English](pipeline.md) | **Tiếng Việt**

Bộ dữ liệu bắt đầu từ tạo ảnh bằng văn bản, tiếp theo là chỉnh sửa ảnh và tuyển chọn thủ công. **Repository công khai cung cấp validator và ví dụ GPU hai ảnh, không phải chương trình tạo tự động đủ 935 ảnh.**

| Bước | Đầu vào | Đầu ra | Cần kiểm tra |
|---|---|---|---|
| SOURCE | Prompt, seed, Mage-Flow-Turbo | chân dung trung tính | một người trưởng thành, bố cục rõ |
| P1/P2 | SOURCE đã chọn, Mage-Flow-Edit-Turbo | ảnh quay trái/phải | hướng quay và giữ danh tính |
| E1/E2 | SOURCE, model chỉnh sửa | ảnh cười/khó chịu | biểu cảm và giữ danh tính |
| Tuyển chọn | ảnh ứng viên | một ảnh được chọn mỗi slot | lỗi thị giác, trùng lặp, nhất quán |
| Phân phối | PNG và metadata | ImageFolder trên Hugging Face; thư mục PNG trên Kaggle | 187 bộ, 935 PNG, 5 slot, SHA256 |
| Website | ImageFolder đã kiểm | WebP 400/768px | trải nghiệm xem, không sao chép PNG gốc |

## Thử công cụ

- **Không cần GPU:** `python3 scripts/verify_dataset.py examples --expected-images 10 --expected-families 2`.
- **Có ảnh được phép sử dụng:** đọc [Kiểm chứng](validation.vi.md) hoặc [attach dataset Kaggle](platforms.vi.md).
- **GPU tùy chọn:** chuẩn bị năm thành phần model cùng `sd-cli` tương thích theo [Hướng dẫn model](MODEL_PROVENANCE.vi.md), rồi chạy `bash scripts/reproduce_source_pose_example.sh`.

SHA256 không chứng nhận danh tính sinh học, chắc chắn không giống người thật hoặc model upstream có cùng byte. [Đọc giới hạn tái lập](reproducibility.vi.md).
