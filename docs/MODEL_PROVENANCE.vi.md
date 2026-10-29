# Nguồn gốc model và fingerprint tham chiếu

> 🌐 Language / Ngôn ngữ: [English](MODEL_PROVENANCE.md) | **Tiếng Việt**

Đây là **tài liệu tham chiếu duy nhất dành cho người đọc** về năm tệp model trong ví dụ GPU CompactFaces SOURCE → P2: vai trò, biến thể chính xác, nguồn tải và checksum đã ghi nhận. Để biết thư mục tải, lệnh kiểm SHA256 và cách chạy GPU, xem [Chuẩn bị model](MODEL_SETUP.vi.md). Việc kiểm dataset bằng CPU không cần trọng số model.

## Danh mục model

| Vai trò | Tệp và định dạng | Nguồn model / tham chiếu |
|---|---|---|
| Sinh SOURCE từ văn bản | `Mage-Flow-Turbo-DiT-Q8_0.gguf` · GGUF Q8_0 | [Mage-Flow-Turbo](https://huggingface.co/mage-flow-community/Mage-Flow-Turbo) · [Kaggle mirror](https://www.kaggle.com/models/dangkhoa2016/mage-flow-community-mage-flow-turbo) |
| Chỉnh góc mặt/biểu cảm | `diffusion_pytorch_model.safetensors` · Edit transformer | [Mage-Flow-Edit-Turbo](https://huggingface.co/mage-flow-community/Mage-Flow-Edit-Turbo) · [Kaggle mirror](https://www.kaggle.com/models/dangkhoa2016/mage-flow-community-mage-flow-edit-turbo) |
| Conditioning văn bản/thị giác | `Qwen3VL-4B-Instruct-Q4_K_M.gguf` · GGUF Q4_K_M | [Qwen3-VL GGUF trên Kaggle](https://www.kaggle.com/models/dangkhoa2016/qwen-qwen3-vl-4b-instruct-gguf) · [model gốc](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct) |
| Projector xử lý ảnh | `mmproj-BF16.gguf` · GGUF BF16 | [File projector ghim theo revision](https://huggingface.co/unsloth/Qwen3-VL-4B-Instruct-GGUF/blob/cc8371d67a57fc6ae05fc5a9c2df763914928539/mmproj-BF16.gguf) |
| Giải mã latent | `diffusion_pytorch_model.safetensors` · VAE Safetensors | [Mage-Flow-Turbo Kaggle mirror](https://www.kaggle.com/models/dangkhoa2016/mage-flow-community-mage-flow-turbo) · **PyTorch / vae-only / Version 1** |

**Edit và VAE là hai thành phần khác nhau**, dù cùng tên `diffusion_pytorch_model.safetensors`. Phải dùng đúng thư mục `edit/` và `vae/` trong [Chuẩn bị model](MODEL_SETUP.vi.md). Không suy ra hai file trùng byte chỉ từ tên model hoặc khi sử dụng quantization khác.

## SHA256 đã ghi nhận

Các fingerprint đầy đủ được đặt **bên ngoài bảng model** để bảng dễ đọc. Mở phần bên dưới khi cần sao chép. Giá trị chuẩn dùng cho công cụ kiểm file chỉ đọc nằm trong [`scripts/model_assets.py`](../scripts/model_assets.py); phần tham chiếu này phải khớp với script đó.

<details>
<summary>Xem năm giá trị SHA256 đầy đủ và đường dẫn tương đối</summary>

```text
4c3dafc143ee64121692b6b63563a4f5288bf6183c4870e1d65f1566519ba7f0  turbo/Mage-Flow-Turbo-DiT-Q8_0.gguf
29c3726ecd64afe149eef28af3e27b6b40de52646bfd16757a37da4b6fbcf288  edit/diffusion_pytorch_model.safetensors
66358cb18bb6b3b1b6675aa412c7a88ef01d228f481184d13668e5201c730a0a  qwen/Qwen3VL-4B-Instruct-Q4_K_M.gguf
364ef9a7502b7e9a834b9c013b953670f6ba2550b4a26fc043c317fa484eb53e  qwen/mmproj-BF16.gguf
34e076dc1e8a15321e1e07be5111d59cf16dd10b804b7c7e20b4de29013427e0  vae/diffusion_pytorch_model.safetensors
```

</details>

Đây là SHA256 tham chiếu cho đúng biến thể tệp được liệt kê, không phải hash chung của mọi revision upstream. Không thay fingerprint chỉ để chấp nhận tệp khác.

## Phạm vi thông tin nguồn gốc

Dataset phát hành có `generation_metadata.jsonl` (935 bản ghi ở bước sinh/chỉnh cuối), `source_lineage.jsonl` (187 bản ghi SOURCE), và `generation_metadata_audit.json`. Các PNG giữ thông số sinh ảnh có cấu trúc khi được ghi nhận. Đây là metadata của file phát hành và bước xử lý cuối, không bao gồm đầy đủ mọi ảnh trung gian.

Dự án sử dụng Mage-Flow-Turbo để tạo SOURCE tổng hợp và Mage-Flow-Edit-Turbo cho các biến thể góc mặt/biểu cảm. Ví dụ GPU tùy chọn chỉ tạo cặp SOURCE/P2 **mới**, **không** tái tạo trùng byte 935 ảnh đã phát hành. Cần tự kiểm output GPU và độ nhất quán khuôn mặt; checksum khớp không chứng minh chất lượng ảnh. Xem [Triển khai Modal](MODAL_DEPLOYMENT.vi.md) và [Khả năng tái lập](reproducibility.vi.md).

## Giấy phép và tài liệu tiếp theo

Mã nguồn thuộc dự án dùng [giấy phép MIT](../LICENSE). Giấy phép ảnh được trình bày trong [Ghi chú giấy phép](../LICENSE-NOTES.vi.md); trọng số model bên thứ ba chịu giấy phép riêng. Cần đọc trang nguồn model thực tế trước khi sử dụng. SHA256 khớp chỉ xác minh file theo fingerprint đã ghi nhận, **không** tự cấp quyền sử dụng hay phân phối model.

[Chuẩn bị và kiểm chứng model](MODEL_SETUP.vi.md) · [Chạy CUDA/Modal](MODAL_DEPLOYMENT.vi.md) · [Khả năng tái lập](reproducibility.vi.md)
