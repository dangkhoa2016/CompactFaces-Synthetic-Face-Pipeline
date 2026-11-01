# CompactFaces — Bộ dữ liệu khuôn mặt tổng hợp và công cụ kỹ thuật

[![CI](https://github.com/dangkhoa2016/CompactFaces-Synthetic-Face-Pipeline/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/dangkhoa2016/CompactFaces-Synthetic-Face-Pipeline/actions/workflows/ci.yml)
![Phiên bản dataset](https://img.shields.io/badge/dataset-v1.0.0-orange)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
[![Code license: MIT](https://img.shields.io/badge/code%20license-MIT-green)](LICENSE)

> 🌐 Language / Ngôn ngữ: [English](README.md) | **Tiếng Việt**

**CompactFaces** là *dự án minh họa kỹ thuật có thể kiểm chứng* về bộ ảnh chân dung tổng hợp. Mỗi danh tính gồm một ảnh SOURCE trung tính, hai ảnh thay đổi tư thế (P1/P2) và hai ảnh thay đổi biểu cảm (E1/E2). Repository cung cấp công cụ kiểm chứng CPU, notebook Kaggle, bộ tạo gallery tĩnh, tài liệu song ngữ và ví dụ GPU tùy chọn.

**Ứng dụng:** tìm hiểu quy trình kiểm toàn vẹn dữ liệu và nguồn gốc ảnh, khám phá tập ảnh thay đổi tư thế/biểu cảm có kiểm soát và thử nghiệm pipeline xử lý dữ liệu. Đây **không phải** benchmark nhận dạng sinh trắc hoặc bằng chứng về độ nhất quán khuôn mặt bằng thị giác.

**Có thể clone và chạy công cụ CPU mà không cần tải bộ ảnh CompactFaces.** Dữ liệu phát hành và trọng số model nằm ở nguồn riêng; GitHub chỉ chứa mã nguồn và tài liệu.

## Thông tin chính

| Dataset 1.0.0 | Phạm vi |
|---|---|
| **187 danh tính tổng hợp** | 120 Core + 67 Additional Optional |
| **935 PNG gốc** | 1024 × 1024; một ảnh SOURCE và bốn biến thể tư thế/biểu cảm mỗi danh tính |
| **SOURCE · P1 · P2 · E1 · E2** | Nhìn thẳng/trung tính · quay trái · quay phải · cười · khó chịu |
| **935 bản ghi nguồn gốc của bước cuối** | Prompt, seed và cấu hình sinh/chỉnh ảnh dạng máy đọc được |
| **187 bản ghi SOURCE lineage** | Liên kết kiểm tra tính nhất quán SOURCE; không phải hướng dẫn tái tạo toàn bộ dataset |
| **935 JPEG xem trước của Builder** | Dùng kiểm bản xem trước, không thay thế PNG gốc |

Validator kiểm **cấu trúc bộ năm ảnh, tính toàn vẹn file, SHA256 và tính nhất quán metadata**. Nó **không chứng minh** tính duy nhất sinh trắc học, độ tương đồng khuôn mặt bằng thị giác hay việc mọi quyền sử dụng đã được xác minh độc lập.

## Ảnh minh họa năm biến thể — CORE:0002

| SOURCE · Trung tính | P1 · Quay trái | P2 · Quay phải | E1 · Mỉm cười | E2 · Khó chịu |
| :---: | :---: | :---: | :---: | :---: |
| ![Ảnh khuôn mặt tổng hợp SOURCE](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/assets/thumb/images/core/identity_0002_SOURCE.webp) | ![Ảnh khuôn mặt tổng hợp P1](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/assets/thumb/images/core/identity_0002_P1.webp) | ![Ảnh khuôn mặt tổng hợp P2](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/assets/thumb/images/core/identity_0002_P2.webp) | ![Ảnh khuôn mặt tổng hợp E1](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/assets/thumb/images/core/identity_0002_E1.webp) | ![Ảnh khuôn mặt tổng hợp E2](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/assets/thumb/images/core/identity_0002_E2.webp) |

Bộ ảnh WebP 400px của **cùng một danh tính tổng hợp**, lấy từ gallery công khai. Ảnh chỉ để xem nhanh, không xác minh SHA256 của PNG gốc, chất lượng thị giác hoặc tính nhất quán danh tính. [Mở gallery tương tác](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/).

**Ví dụ trực quan năm ảnh:** [Xem SOURCE, P1, P2, E1 và E2 trên gallery](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/) (WebP xem trước, không thay thế kiểm toàn vẹn) · [Kaggle CPU Integrity Lab](https://www.kaggle.com/code/dangkhoa2016/compactfaces-synthetic-face-cpu-validation) · [Mã nguồn notebook](notebooks/compactfaces_kaggle_cpu_validation.ipynb) · [Kaggle Dataset Version 1](https://www.kaggle.com/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset) · [Hugging Face ImageFolder](https://huggingface.co/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset).

Để tự kiểm tra dữ liệu đã tải, xem [hướng dẫn xác minh ImageFolder](docs/validation.vi.md) hoặc [đối chiếu hai nền tảng](docs/platform-integrity.vi.md). Không suy diễn tính toàn vẹn ảnh chỉ từ phần mô tả dataset hoặc checksum viết trên một trang web.

## Bắt đầu nhanh — không cần tải dataset ảnh hoặc dùng GPU

Cài **Git và Python 3.10+**, clone repository rồi chạy bộ mẫu 10 dòng. Các lệnh CPU này không cần dataset ảnh hoặc GPU:

```bash
git clone https://github.com/dangkhoa2016/CompactFaces-Synthetic-Face-Pipeline.git
cd CompactFaces-Synthetic-Face-Pipeline
python3 scripts/verify_dataset.py examples --expected-images 10 --expected-families 2
python3 scripts/validate_repository.py
python3 scripts/validate_notebooks.py
```

Công cụ kiểm notebook sẽ chạy DEMO độc lập ở cả hai ngôn ngữ. **`DEMO_ONLY` là kết quả dự kiến**: chỉ kiểm metadata minh họa, chưa xác minh byte của PNG phát hành. Các lệnh đầu tiên chỉ dùng thư viện chuẩn Python. Đọc [hướng dẫn bắt đầu](docs/QUICKSTART.vi.md) để chạy thêm phép kiểm Pillow, JavaScript và hồi quy.

## Kiểm chứng 935 ảnh đã phát hành trên Kaggle

1. Mở [CPU Integrity Lab](https://www.kaggle.com/code/dangkhoa2016/compactfaces-synthetic-face-cpu-validation), chọn **Copy & Edit**.
2. Thêm dataset **`dangkhoa2016/compactfaces-synthetic-face-dataset`**, **Version 1**, qua **Input → Add Input → Datasets**.
3. Chọn **Accelerator = None**, đặt `MODE = "full"`, `DATASET_DIR = ""`, rồi chạy toàn bộ cell.
4. Kiểm `FULL_PASS` và báo cáo JSON: **SHA256 của 935 PNG**, **kích thước IHDR của 935 PNG**, **935 JPEG Builder được giải mã**, **935 bản ghi provenance nhúng** và **187 SOURCE lineage**.

**Đối chiếu nội dung bản phát hành:** FULL kiểm thêm SHA256 của `metadata.csv` với fingerprint chính thức của Version 1. Phép kiểm xác nhận byte metadata dự kiến, **không** chứng nhận số phiên bản Kaggle đang lưu trữ hoặc Git commit nguồn.

**Giới hạn:** `FULL_PASS` chỉ xác minh tính toàn vẹn của tệp và tính nhất quán metadata; **không** đánh giá tính duy nhất sinh trắc, chất lượng thị giác hay độ giống nhau của năm khuôn mặt. Bài test FULL trong CI dùng dữ liệu giả lập, không chứng nhận dataset Version 1 hiện được Kaggle phục vụ đã được kiểm độc lập.

**Lưu ý:** Notebook mặc định `MODE = "auto"`, nên sẽ chạy `DEMO_ONLY` nếu chưa attach dataset. Muốn xác minh dữ liệu phát hành, phải đặt `MODE = "full"` để thiếu input sẽ báo lỗi rõ ràng.

Kaggle cung cấp dữ liệu dưới dạng *thư mục đã giải nén*. Vì vậy kiểm SHA256/CRC của ZIP nguyên vẹn được ghi `SKIPPED_KAGGLE_EXTRACTED`, không tự nhận PASS. Nếu không thể truy cập dữ liệu, chế độ FULL chủ động báo lỗi, không âm thầm chuyển thành DEMO. Notebook **chỉ đọc dữ liệu đầu vào**, tùy chọn chỉ ghi báo cáo tổng hợp vào `/kaggle/working/`.

Nếu đã có bản sao ImageFolder từ Hugging Face và có quyền sử dụng:

```bash
python3 scripts/verify_dataset.py /path/to/data/train --expected-images 935 --expected-families 187 --verify-images
```

Lệnh cục bộ này kiểm cấu trúc năm slot và SHA256 PNG; muốn kiểm Builder và provenance nhúng thì dùng notebook Kaggle. Xem [kiểm chứng](docs/validation.vi.md), [đối chiếu hai nền tảng](docs/platform-integrity.vi.md) và [khả năng tái lập](docs/reproducibility.vi.md).

## Công cụ trong repository

| Đường dẫn | Chức năng |
|---|---|
| `scripts/verify_dataset.py` | Kiểm metadata, cấu trúc bộ năm ảnh và SHA256 trên CPU |
| `notebooks/compactfaces_kaggle_cpu_validation.ipynb` | Một notebook, phần giải thích EN/VI tách riêng và Python dùng chung; DEMO / FULL / PARTIAL |
| `scripts/test_notebook_full_fixture.py` | Fixture hồi quy tổng hợp và tình huống dữ liệu lỗi, chạy offline |
| `scripts/build_static_gallery.py` | Tạo WebP 400px/768px và catalog tĩnh từ ImageFolder được phép sử dụng |
| `website_src/` | Gallery song ngữ responsive, lọc Core/Additional, xem năm ảnh tư thế/biểu cảm |
| `modal_app.py` và `scripts/reproduce_source_pose_example.sh` | Ví dụ sinh/chỉnh SOURCE/P2 mới; cần chuẩn bị model và GPU |
| `scripts/model_assets.py` | Kiểm SHA256 của năm checkpoint model; không nhúng trọng số |

**Ví dụ GPU tùy chọn:** [Chuẩn bị model](docs/MODEL_SETUP.vi.md) → [Hướng dẫn Modal](docs/MODAL_DEPLOYMENT.vi.md). Ví dụ tạo cặp SOURCE/P2 **mới** bằng checkpoint tương thích, không tái tạo bộ dataset 935 ảnh được phân phối. Cần tự kiểm tra chất lượng ảnh đầu ra.

Để tạo preview cục bộ từ ImageFolder **được phép sử dụng**, đọc [hướng dẫn Gallery](docs/gallery.vi.md). WebP là ảnh nén mất dữ liệu; công cụ không commit hoặc chỉnh sửa PNG gốc.

## Tài liệu

[Mục lục tài liệu](docs/README.vi.md) · [Bắt đầu](docs/QUICKSTART.vi.md) · [Dataset và nền tảng](docs/platforms.vi.md) · [Kiến trúc](docs/architecture.vi.md) · [Kiểm chứng](docs/validation.vi.md) · [Khả năng tái lập](docs/reproducibility.vi.md) · [Nguồn gốc model](docs/MODEL_PROVENANCE.vi.md) · [Chính sách phát hành](docs/RELEASE_POLICY.vi.md) · [Đối chiếu hai nền tảng](docs/platform-integrity.vi.md)

## Nguồn gốc dữ liệu, giới hạn và giấy phép

CompactFaces cung cấp ảnh khuôn mặt tổng hợp và metadata để kiểm tra dataset. Hash giúp xác minh nội dung tệp nhưng không bảo đảm tạo lại ảnh giống từng pixel hoặc không vô tình giống người thật.

**Phân định giấy phép:** mã nguồn và tài liệu do repository sở hữu sử dụng [MIT](LICENSE). Ảnh dataset, WebP gallery phái sinh và metadata đủ điều kiện được cấp phép riêng theo [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) trong phạm vi người cấp phép có quyền. Trọng số model và dữ liệu đầu vào của người dùng có điều khoản riêng. MIT cho mã nguồn không đồng nghĩa cấp quyền thương mại đối với ảnh. Xem [phạm vi giấy phép](LICENSE-NOTES.vi.md).

Liên hệ khi cần xem xét quyền riêng tư, ảnh hoặc đề nghị gỡ ảnh: **[i.am@dangkhoa.dev](mailto:i.am@dangkhoa.dev)**.

**Tác giả:** Đăng Khoa.
