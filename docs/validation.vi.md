# Kiểm chứng ảnh và metadata của dataset

> 🌐 Language / Ngôn ngữ: [English](validation.md) | **Tiếng Việt**

Công cụ phân biệt **kiểm thử mã nguồn mẫu** và **kiểm đủ PNG gốc**. Không nhầm DEMO_ONLY hoặc schema PASS với xác minh toàn bộ 935 PNG.

## A. Kiểm CPU khi chưa tải dataset

~~~bash
python3 scripts/verify_dataset.py examples --expected-images 10 --expected-families 2
python3 scripts/validate_repository.py
python3 scripts/validate_notebooks.py
~~~

Chỉ kiểm metadata mẫu và DEMO của notebook; chưa hash PNG gốc.

## B. Kiểm ImageFolder đã tải

~~~bash
python3 scripts/verify_dataset.py /path/to/data/train --expected-images 935 --expected-families 187 --verify-images
~~~

Cần `metadata.csv` và ảnh được tham chiếu. Validator cục bộ kiểm cú pháp danh tính, đủ năm slot, collection Core/Additional, đường dẫn và SHA256 không trùng, và liên kết `source_sha256` của mỗi nhóm. Khi dùng `--verify-images`, công cụ còn đối chiếu SHA256 của byte PNG. Công cụ này **không giải mã PNG, kiểm kích thước hay xác minh provenance nhúng**; dùng notebook Kaggle FULL cho các phép kiểm bổ sung. Bỏ cờ thì **chưa kiểm byte ảnh**.

Chạy test hồi quy với dữ liệu sai: `python3 -m unittest -v scripts.test_dataset_validator scripts.test_gallery_cache` (test cache cần Pillow).

## C. Notebook CPU trên Kaggle

1. [Mở notebook](https://www.kaggle.com/code/dangkhoa2016/compactfaces-synthetic-face-cpu-validation).
2. Làm theo [Input → Add Input → Datasets](platforms.vi.md), chọn CompactFaces Dataset Version 1 của dangkhoa2016.
3. Đặt `MODE = "full"`, accelerator `None`, rồi Run all.
4. Đọc `verified_png_sha256_count`, `input_layout`, trạng thái từng phép kiểm và `verdict`.

Notebook FULL đọc **trực tiếp ảnh PNG và metadata trong các thư mục Kaggle Dataset Version 1**, không cần chuẩn bị ZIP. Notebook kiểm SHA256 của 935 PNG, kiểm tên và giải mã 935 JPEG Builder, đối chiếu 935 bản ghi provenance, 187 SOURCE lineage và thông số SDCpp nhúng trong PNG bằng Pillow. FULL_PASS cần đủ file provenance; thiếu file sẽ báo lỗi và dừng.

Kiểm thử Builder đối chiếu tên của đủ 935 JPEG với identity/slot, giải mã đầy đủ từng JPEG và đối chiếu **SHA256/đường dẫn PNG gốc ghi trong catalog**. Công cụ không hash từng JPEG để so với một manifest checksum JPEG độc lập; JPEG hợp lệ nhưng khác nội dung hình ảnh vẫn có thể vượt qua bước này. SOURCE lineage phải có 187 danh tính duy nhất, khớp hoàn toàn metadata. Các phép kiểm không chứng minh JPEG và PNG giống nhau về mặt thị giác. **`FULL_PASS` chỉ xác nhận toàn vẹn tệp và tính nhất quán metadata**; không tự đánh giá chất lượng hình ảnh, độ giống khuôn mặt giữa các góc nhìn hoặc tính duy nhất sinh trắc học. Test FULL trên CI dùng fixture giả lập, không phải dữ liệu Kaggle đang được phục vụ.

**Khi có lỗi:** giữ nguyên file, kiểm đường dẫn/slot trùng/hash và tải lại nguồn hợp lệ. Không tự sinh lại hoặc ghi đè PNG đã duyệt chỉ để test báo xanh.

[Cấu trúc](DATASET_STRUCTURE.vi.md) · [Khắc phục sự cố](troubleshooting.vi.md)

## Kích thước PNG và bằng chứng máy đọc được

Notebook CPU kiểm chữ ký PNG và chiều rộng/cao trong IHDR của **cả 935 ảnh gốc**, yêu cầu 1024 × 1024, kể cả khi tắt tùy chọn SHA256. Kiểm header này không tương đương giải mã đầy đủ toàn bộ ảnh. Để đạt `FULL_PASS`, cả 935 SHA256 của ảnh gốc, JPEG Builder, metadata nhúng và SOURCE lineage vẫn phải đạt. Bước preview còn kiểm kích thước năm ảnh thuộc danh tính được chọn.

JSON report có thêm `verified_png_dimensions_count`, `metadata_csv_sha256`, phiên bản Python và Pillow, thời gian chạy UTC, kiến trúc CPU và các lựa chọn kiểm chứng. Có thể cung cấp `source_git_commit` qua biến môi trường `COMPACTFACES_GIT_SHA`; nếu không có thì giữ null. Báo cáo chỉ ghi loại thiết bị CPU, không ghi định danh thiết bị. Notebook không xác minh độc lập chủ sở hữu hoặc phiên bản dataset: hãy kiểm tra qua bảng Input hoặc API của Kaggle.
