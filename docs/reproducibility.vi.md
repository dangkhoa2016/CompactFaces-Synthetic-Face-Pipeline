# Khả năng tái lập và kiểm chứng độc lập CompactFaces 1.0.0

> 🌐 Language / Ngôn ngữ: [English](reproducibility.md) | **Tiếng Việt**

Tài liệu này phân biệt **kiểm lại file đã phát hành** với **tạo ảnh mới bằng AI**. Người dùng có thể chạy test CPU không cần tải dataset, nhưng xác minh toàn bộ đòi hỏi quyền truy cập các PNG gốc. Ví dụ Modal chỉ sinh **một SOURCE mới và một P2 mới**, không tái tạo lại 935 PNG đã tuyển chọn.

## 1. Chọn đúng mức kiểm chứng

| Mức | Mục tiêu | Yêu cầu | Bằng chứng kỳ vọng |
|---|---|---|---|
| A | Test mã nguồn và DEMO | Git, Python 3.10+, không cần ảnh/GPU | 2 bộ mẫu, 10 dòng metadata, DEMO_ONLY |
| B | Kiểm byte PNG ImageFolder | 935 PNG + metadata.csv | 187 bộ đủ 5 slot, SHA256 khớp đủ 935 |
| C | Kaggle FULL và provenance | Dataset Version 1, CPU, Pillow | 935 PNG, 935 preview, 935 generation metadata, 187 SOURCE lineage |
| D | Thử sinh ảnh GPU mới | Năm model đúng hash và sd-cli CUDA tương thích | SOURCE.png/P2.png **mới** và report.json |

Dataset có 120 bộ Core + 67 bộ Additional Optional. Mỗi bộ gồm SOURCE (trung tính), P1 (quay trái), P2 (quay phải), E1 (cười), E2 (khó chịu). Tổng cộng **187 × 5 = 935 PNG 1024×1024**.

**Integrity** nghĩa là byte file hiện tại giống SHA256 đã lưu; **provenance** nghĩa là metadata ở bước cuối khớp với bản ghi; **generation reproducibility** nghĩa là thử lại phương pháp tạo ảnh; **pixel-identical reproduction** đòi hỏi pixel giống chính xác. PASS mức B hoặc C **không** chứng minh mức D và không chứng minh khả năng tái tạo ảnh cùng byte.

## 2. Mức A — chạy ngay, không cần dataset

~~~bash
git clone https://github.com/dangkhoa2016/CompactFaces-Synthetic-Face-Pipeline.git
cd CompactFaces-Synthetic-Face-Pipeline
python3 --version
git rev-parse HEAD
python3 scripts/verify_dataset.py examples --expected-images 10 --expected-families 2
python3 scripts/validate_repository.py
python3 scripts/validate_notebooks.py
python3 scripts/audit_publication.py
python3 -m unittest -v scripts/test_modal_workflow.py
~~~

Kết quả ví dụ mong đợi: PASS: 2 identity families / 10 images. Validator notebook chạy DEMO song ngữ; verified_png_sha256_count = 0 trong DEMO là **đúng thiết kế**, không phải lỗi. Mức A **chưa đọc PNG gốc**. Scanner chỉ kiểm những mẫu token đã định nghĩa, không thay thế bước kiểm bảo mật.

## 3. Mức B — kiểm SHA256 ImageFolder thật

Khi có quyền, tải [dataset Hugging Face](https://huggingface.co/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset). Xác định thư mục thực sự có metadata.csv và các ảnh được tham chiếu bởi cột file_name (thường là data/train).

~~~bash
python3 scripts/verify_dataset.py /path/to/data/train \
  --expected-images 935 --expected-families 187 --verify-images
~~~

Nếu thành công, script báo PASS: 187 identity families / 935 images. Script kiểm đủ slot, danh tính và SHA256 byte của mỗi ảnh bằng cách đọc theo chunk. **Không** tự kiểm prompt/seed nhúng trong PNG, toàn bộ SOURCE lineage hoặc checksum model. Sai hash/thiếu file phải dừng và giữ nguyên dữ liệu; không chỉnh metadata cho khớp kết quả mong muốn.

## 4. Mức C — chạy FULL bằng notebook Kaggle CPU

1. Mở [notebook Kaggle CompactFaces](https://www.kaggle.com/code/dangkhoa2016/compactfaces-synthetic-face-cpu-validation), chọn Copy & Edit hoặc import file notebook từ GitHub.
2. Trong Input → Add Input → Datasets, tìm compactfaces-synthetic-face-dataset, xác nhận chủ sở hữu dangkhoa2016, chọn **Dataset Version 1**, nhấn Add.
3. Chọn Accelerator = None. File attach nằm dưới /kaggle/input; không cần tải lại từ Internet.
4. Sửa cell cấu hình:

~~~python
MODE = "full"
DATASET_DIR = ""
VERIFY_PNG_SHA256 = True
VERIFY_BUILDER = True
EXPORT_REPORT = True
~~~

Kaggle Dataset Version 1 cung cấp `metadata.csv` và **các thư mục Core, Additional, Builder** ở `/kaggle/input/compactfaces-synthetic-face-dataset/`. Notebook đọc trực tiếp dữ liệu sẵn có. Nếu nhiều root phù hợp, đặt DATASET_DIR chính xác theo Input. Khi EXPORT_REPORT bật, báo cáo lưu tại /kaggle/working/compactfaces_cpu_validation_report.json.

**Đọc kết quả đầy đủ:** mode FULL, verdict FULL_PASS, identities 187, records 935, verified_png_sha256_count 935, builder_jpeg_previews 935, generation_provenance_verified 935, source_lineage_verified 187; các checks metadata, png_sha256, builder và provenance phải PASS.

**Phạm vi báo cáo:** Notebook vẫn có hai trường kỹ thuật `builder_crc` và `zip_files` để tương thích với cấu trúc báo cáo. Với Kaggle Dataset Version 1 dạng thư mục, cả hai trường mang giá trị `SKIPPED_KAGGLE_EXTRACTED` vì phép kiểm cấp tệp lưu trữ không áp dụng. Đây là trạng thái **dự kiến**, không phải lỗi hoặc yêu cầu bổ sung dữ liệu, và không ngăn `FULL_PASS` khi ảnh, JPEG Builder và provenance đều đạt.

Notebook đối chiếu generation_metadata.jsonl (935 dòng), source_lineage.jsonl (187 dòng), generation_metadata_audit.json và thông số SDCpp trong PNG bằng Pillow. Các thông tin gồm SHA256, identity/slot, prompt, seed, steps ở **bước tạo/chỉnh cuối**. Nó không thể tái dựng mọi ảnh trung gian hoặc ứng viên bị loại.

## 5. Mức D — chạy ví dụ GPU mới trên Modal

Đầu tiên làm theo [chuẩn bị model](MODEL_SETUP.vi.md) và [hướng dẫn Modal](MODAL_DEPLOYMENT.vi.md). Cần tải đúng năm model, SHA256 đều PASS, sử dụng hai Volume riêng và kiểm lại file **trên Modal** bằng CPU trước khi bật GPU.

~~~bash
python3 scripts/model_assets.py --root "$HOME/compactfaces-models"
modal run modal_app.py::verify_models
# Kiểm phí/quota trước bước GPU có tính phí:
modal run modal_app.py::generate_pair
~~~

GPU runner ghim revision stable-diffusion.cpp, ghi hai prompt/seed, model hashes, output hashes và thời gian chạy. Cần kiểm file đầu ra và SHA256 thực tế; xem [Hướng dẫn Modal](MODAL_DEPLOYMENT.vi.md). Ví dụ GPU không chứng minh chất lượng của toàn bộ dataset.

Ngay cả khi có SOURCE/P2 mới và SHA256 hợp lệ, điều đó chỉ chứng minh **hai file đầu ra được tạo thành công**. Khả năng giữ danh tính và hướng quay phải được người dùng đánh giá bằng mắt riêng.

## 6. Vì sao không thể tái tạo chính xác 935 PNG?

Dataset cung cấp metadata của bước cuối và liên kết SOURCE để kiểm tra tệp, không bảo đảm tạo lại ảnh giống từng pixel. Cùng prompt và seed có thể sinh kết quả khác nhau trên model build hoặc runtime khác.

WebP 400/768px của gallery là ảnh preview nén mất dữ liệu, **không thay thế PNG gốc 1024×1024**. Ảnh tổng hợp có thể vô tình giống người thật; hash không phải bằng chứng tính duy nhất sinh trắc, consent hoặc quyền pháp lý.

## 7. Thu thập bằng chứng khi tự kiểm

Lưu Git commit, URL/phiên bản dataset, dạng input (thư mục Kaggle hoặc ImageFolder từ Hugging Face), lệnh thực tế, Python/Modal SDK, CPU/GPU, model SHA256, revision sd.cpp, prompt/seed, image hashes, thời lượng và mọi trạng thái SKIPPED/FAIL. Không công khai token, đường dẫn riêng, ảnh không có quyền phân phối hoặc dữ liệu cá nhân.

Chỉ diễn đạt đúng mức đạt được: “DEMO metadata PASS” cho A; “SHA256 935 PNG gốc đã đối chiếu” khi thật sự chạy B/C; “`builder_crc` và `zip_files` được bỏ qua vì không áp dụng cho dữ liệu dạng thư mục” cho bản Kaggle; “đã tạo SOURCE/P2 mới trên GPU” chỉ khi có bằng chứng chạy D. Không gộp các kết quả này thành khẳng định tái tạo chính xác toàn bộ.

[Khắc phục sự cố](troubleshooting.vi.md) · [Nguồn tải](platforms.vi.md) · [Nguồn model](MODEL_PROVENANCE.vi.md) · [Giấy phép](../LICENSE-NOTES.vi.md)

## Metadata của lần chạy notebook

Để có báo cáo FULL độc lập, cần giữ bản sửa đổi notebook, Kaggle Dataset Version 1, SHA256 của `metadata.csv`, thời gian chạy UTC, phiên bản Python/Pillow, cấu trúc input và các phép kiểm đã bật. `COMPACTFACES_GIT_SHA` là nhãn revision nguồn tùy chọn. Báo cáo ghi loại thiết bị CPU, không ghi định danh thiết bị duy nhất. Cần xác minh phiên bản Kaggle riêng, không tự suy từ tên thư mục và không công khai thông tin bí mật của máy. Kích thước IHDR của cả 935 PNG được so với yêu cầu 1024 × 1024; bước đọc header không thay thế SHA256.
