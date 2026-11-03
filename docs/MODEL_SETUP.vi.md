# Chuẩn bị model cho ví dụ GPU tùy chọn

> 🌐 Language / Ngôn ngữ: [English](MODEL_SETUP.md) | **Tiếng Việt**

Tài liệu này hướng dẫn chuẩn bị và kiểm chứng năm tệp model cục bộ cho ví dụ GPU **SOURCE → P2**. Notebook Kaggle kiểm dữ liệu bằng CPU **không cần model, CUDA, Modal hoặc tải trọng số**. Repository GitHub không phân phối model weights.

**Trước khi tải:** xem [danh mục model và các liên kết nguồn](MODEL_PROVENANCE.vi.md#danh-mục-model) để chọn đúng năm thành phần. Tài liệu hướng dẫn này không lặp lại bảng nguồn hoặc các chuỗi SHA256 dài 64 ký tự.

## 1. Chuẩn bị thư mục cục bộ

Tạo thư mục rồi đặt từng tệp model đã tải hợp lệ vào đúng vị trí:

```bash
mkdir -p "$HOME/compactfaces-models"/{turbo,edit,qwen,vae}
```

```text
~/compactfaces-models/
├── turbo/Mage-Flow-Turbo-DiT-Q8_0.gguf
├── edit/diffusion_pytorch_model.safetensors
├── qwen/Qwen3VL-4B-Instruct-Q4_K_M.gguf
├── qwen/mmproj-BF16.gguf
└── vae/diffusion_pytorch_model.safetensors
```

**Quan trọng:** Edit transformer và VAE là **hai tệp khác nhau** nhưng cùng tên `diffusion_pytorch_model.safetensors`. Không ghi đè một tệp lên tệp kia. Cần chọn đúng quantization GGUF và biến thể `vae-only` trong [Nguồn gốc model](MODEL_PROVENANCE.vi.md).

## 2. Tải từ nguồn đã ghi rõ

Mở liên kết của từng thành phần trong [danh mục model](MODEL_PROVENANCE.vi.md#danh-mục-model). Đọc điều kiện giấy phép và quyền truy cập; chọn chính xác định dạng GGUF/Safetensors và biến thể được ghi. Dùng giao diện hoặc CLI chính thức của nền tảng, không mặc định model trùng tên hay khác revision là trùng byte.

Năm SHA256 đầy đủ được giữ tại [phần checksum có thể mở rộng](MODEL_PROVENANCE.vi.md#sha256-đã-ghi-nhận). Giá trị dùng để kiểm chứng thực tế nằm trong `scripts/model_assets.py`. Các fingerprint này mô tả **tệp đã ghi nhận**, không chứng nhận tất cả revision upstream.

## 3. Kiểm chứng năm tệp trên CPU

Chạy tại thư mục gốc của repository GitHub:

```bash
python3 scripts/model_assets.py --root "$HOME/compactfaces-models"
python3 scripts/model_assets.py --root "$HOME/compactfaces-models" --json
```

Công cụ chỉ đọc từng phần của tệp, tính SHA256, so khớp năm fingerprint đã ghi nhận và trả `PASS`, `MISSING` hoặc `MISMATCH`. **Chỉ khi cả năm SHA256 khớp mới có verdict `PASS`, exit code 0**. Thiếu file hoặc sai hash trả exit code 2.

Tùy chọn `--presence-only` chỉ kiểm tra đường dẫn, **không xác nhận SHA256**. Không sửa hash kỳ vọng chỉ để biến file sai thành PASS.

## 4. Chạy ví dụ GPU tùy chọn

Sau khi kiểm cục bộ PASS, làm theo [hướng dẫn triển khai Modal](MODAL_DEPLOYMENT.vi.md): upload vào Volume Private, kiểm lại SHA256 trên CPU và gọi GPU có tính phí bằng thao tác riêng.

Hoặc nếu đã có binary `sd-cli` tương thích với NVIDIA/CUDA:

```bash
export SD_CLI=/path/to/compatible/sd-cli
export MODEL_DIR="$HOME/compactfaces-models"
export OUTPUT_DIR=./compactfaces_example
bash scripts/reproduce_source_pose_example.sh
```

Ví dụ tạo một SOURCE và một P2 mới, không tái tạo trùng byte 935 ảnh đã phát hành. Cần kiểm tính tương thích runtime và chất lượng ảnh riêng, độc lập với SHA256.

## Xử lý lỗi thường gặp

| Hiện tượng | Cần kiểm tra |
|---|---|
| `MISSING` | Đường dẫn tương đối, chữ hoa/thường, tên tệp và tải xuống hoàn chỉnh |
| `MISMATCH` | Quantization, biến thể file, revision và byte thực tế |
| Nhầm Edit thành VAE | Giữ hai tệp Safetensors trong hai thư mục tương ứng |
| Bị từ chối tải | Xem giấy phép, xin quyền truy cập hợp lệ |
| CUDA lỗi dù SHA256 PASS | Kiểm tra `sd-cli`, GPU, bản CUDA và tương thích model |

Xem [Nguồn gốc model](MODEL_PROVENANCE.vi.md) để kiểm tra fingerprint, liên kết tải, giấy phép và giới hạn tái lập; xem [Khả năng tái lập](reproducibility.vi.md) để hiểu điều ví dụ này không chứng minh.
