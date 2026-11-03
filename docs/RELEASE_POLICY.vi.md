# Phân định dữ liệu phân phối và giấy phép

> 🌐 Language / Ngôn ngữ: [English](RELEASE_POLICY.md) | **Tiếng Việt**

## Phân biệt từng loại tài sản

| Tài sản | Nội dung | Điều khoản / trách nhiệm |
|---|---|---|
| [GitHub pipeline](https://github.com/dangkhoa2016/CompactFaces-Synthetic-Face-Pipeline) | mã nguồn, ví dụ, tài liệu, notebook | [MIT](../LICENSE) cho code/docs do repo sở hữu |
| [Dataset Hugging Face](https://huggingface.co/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset) | PNG gốc, metadata | [CC BY-NC 4.0](../LICENSE-NOTES.vi.md) với tài sản có quyền cấp phép |
| [Kaggle Dataset Version 1](https://www.kaggle.com/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset) | dataset và file hỗ trợ | giấy phép dataset, không phải MIT của GitHub |
| [Gallery](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/) | WebP dẫn xuất | vẫn chịu điều kiện phân phối ảnh |
| Model upstream | trọng số và runtime ở nền tảng ngoài | giấy phép và điều khoản riêng |

Repository **không** chứa ảnh gốc, trọng số model hoặc thông tin xác thực. Người dùng có thể chạy các công cụ độc lập không cần dataset đầy đủ.

## Trước khi chia sẻ kết quả

1. Kiểm file thật với [công cụ xác minh](validation.vi.md).
2. Đọc giấy phép dataset và model upstream; MIT của code **không** tự cấp quyền sử dụng ảnh/model.
3. Không tuyên bố có thể tái tạo mọi pixel, các danh tính khác biệt sinh trắc hoặc chắc chắn không giống người thật.
4. Chỉ công bố ảnh/preview khi đủ quyền đối với chính tài sản đó.

[README](../README.vi.md) · [Khả năng tái lập](reproducibility.vi.md)
