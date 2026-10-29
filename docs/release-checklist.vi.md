# Sử dụng và kiểm chứng CompactFaces

> 🌐 Language / Ngôn ngữ: [English](release-checklist.md) | **Tiếng Việt**

Các lệnh này giúp người dùng kiểm tra bộ công cụ hoặc dataset đã tải.

## Kiểm bộ công cụ mã nguồn

```bash
python3 scripts/validate_repository.py
python3 scripts/validate_notebooks.py
python3 scripts/verify_dataset.py examples --expected-images 10 --expected-families 2
python3 -m unittest -v scripts.test_dataset_validator scripts.test_gallery_cache
```

Các ví dụ chỉ dùng dữ liệu giả lập. **Chúng không xác minh 935 PNG gốc đang được phân phối.** Test cache WebP cần Pillow.

## Kiểm dữ liệu đã tải

Làm theo [hướng dẫn kiểm chứng dataset](validation.vi.md) cho ImageFolder cục bộ, hoặc attach dataset Kaggle vào [notebook CPU](https://www.kaggle.com/code/dangkhoa2016/compactfaces-synthetic-face-cpu-validation) và đặt `MODE = "full"`. Kiểm số lượng thật, hash, từng trạng thái và phép kiểm bị bỏ qua. Khi so hai bản tải từ Hugging Face/Kaggle, dùng [hướng dẫn đối chiếu](platform-integrity.vi.md).

Về giấy phép, xem [MIT](../LICENSE), [điều khoản dữ liệu ảnh](../LICENSE-NOTES.vi.md) và giấy phép model gốc. Không đưa token, ảnh cá nhân nhạy cảm hoặc dữ liệu nhận dạng vào báo lỗi.

[Bắt đầu](QUICKSTART.vi.md) · [Khắc phục sự cố](troubleshooting.vi.md)
