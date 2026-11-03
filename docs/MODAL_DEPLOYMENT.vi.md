# Triển khai ví dụ GPU CompactFaces trên Modal

> 🌐 Language / Ngôn ngữ: [English](MODAL_DEPLOYMENT.md) | **Tiếng Việt**

Hướng dẫn này chạy ví dụ tạo **một SOURCE mới và một P2 mới** trên Modal A10G, không tái tạo lại 935 ảnh đã phát hành. Build image, lưu trữ và GPU có thể **phát sinh chi phí**. Người dùng phải kiểm tính tương thích runtime và tự đánh giá chất lượng ảnh đầu ra.

## 1. Cấu trúc triển khai

~~~text
Máy cá nhân: 5 checkpoint + Modal CLI
     │ upload vào Volume riêng tư
     ▼
compactfaces-example-models-v1
     │ mount read-only
     ├──► CPU kiểm SHA256 của 5 model
     │       └── PASS mới chạy GPU
     ▼
Modal A10G + stable-diffusion.cpp CUDA build đã ghim revision
     │ sinh SOURCE và chỉnh P2
     ▼
compactfaces-example-results-v1
     └── từng run: SOURCE.png, P2.png, report.json
~~~

Yêu cầu: workspace Modal có quyền và quota GPU; Python 3.11+ để chạy CLI; mạng Internet để build/tải thành phần; đủ dung lượng để chứa năm checkpoint; tuân thủ giấy phép của từng model.

## 2. Cài Modal CLI và đăng nhập

~~~bash
python3 -m pip install "modal==1.6.3"
modal --version
modal setup
modal profile current
~~~

Lệnh setup có thể mở trình duyệt để xác thực. **Không đưa Modal token vào Git, tài liệu hoặc log công khai.** Kiểm tra đúng workspace trước khi tạo Volume hoặc chạy GPU. Tài liệu chính thức: [Modal CLI](https://modal.com/docs/cli/latest) và [Volume commands](https://modal.com/docs/cli/latest/volume).

## 3. Chuẩn bị đủ năm model trên máy

Làm theo [MODEL_SETUP.vi.md](MODEL_SETUP.vi.md) để chọn đúng model và phiên bản. Cấu trúc bắt buộc:

~~~text
~/compactfaces-models/
  turbo/Mage-Flow-Turbo-DiT-Q8_0.gguf
  edit/diffusion_pytorch_model.safetensors
  qwen/Qwen3VL-4B-Instruct-Q4_K_M.gguf
  qwen/mmproj-BF16.gguf
  vae/diffusion_pytorch_model.safetensors
~~~

~~~bash
cd CompactFaces-Synthetic-Face-Pipeline
python3 scripts/model_assets.py --root "$HOME/compactfaces-models" --json
~~~

**Điều kiện tiếp tục:** kết quả phải có verdict = PASS và cả năm model đều PASS. MISSING, MISMATCH và PRESENCE_ONLY **không được xem là đạt SHA256**. Hai Safetensors trùng tên là hai model khác nhau, không được ghi đè.

## 4. Tạo hai Volume mới độc lập

~~~bash
modal volume create compactfaces-example-models-v1
modal volume create compactfaces-example-results-v1
~~~

Hai lệnh trên tạo các Volume dành cho ví dụ này. Giữ chúng tách biệt với tài nguyên production. Nếu đặt tên khác, hãy cấu hình `COMPACTFACES_MODEL_VOLUME` và `COMPACTFACES_OUTPUT_VOLUME` trước khi chạy Modal App.

## 5. Upload từng file model vào Volume riêng tư

~~~bash
modal volume put compactfaces-example-models-v1 \
  "$HOME/compactfaces-models/turbo/Mage-Flow-Turbo-DiT-Q8_0.gguf" \
  turbo/Mage-Flow-Turbo-DiT-Q8_0.gguf
modal volume put compactfaces-example-models-v1 \
  "$HOME/compactfaces-models/edit/diffusion_pytorch_model.safetensors" \
  edit/diffusion_pytorch_model.safetensors
modal volume put compactfaces-example-models-v1 \
  "$HOME/compactfaces-models/qwen/Qwen3VL-4B-Instruct-Q4_K_M.gguf" \
  qwen/Qwen3VL-4B-Instruct-Q4_K_M.gguf
modal volume put compactfaces-example-models-v1 \
  "$HOME/compactfaces-models/qwen/mmproj-BF16.gguf" \
  qwen/mmproj-BF16.gguf
modal volume put compactfaces-example-models-v1 \
  "$HOME/compactfaces-models/vae/diffusion_pytorch_model.safetensors" \
  vae/diffusion_pytorch_model.safetensors
modal volume ls compactfaces-example-models-v1 /
~~~

Các checkpoint có thể lớn; việc upload và lưu trữ có thể tốn thời gian/chi phí. Không tự thêm tùy chọn --force hay xóa file, vì thao tác ghi đè cần quyết định riêng.

## 6. Kiểm model trực tiếp từ Modal bằng CPU

~~~bash
modal run modal_app.py::verify_models
~~~

Function dùng CPU và mount Volume model **chỉ đọc**, tính SHA256 của năm tệp. Kỳ vọng hiển thị MODEL_PREFLIGHT_PASS và JSON verdict PASS. CPU/storage vẫn có thể tính phí. Nếu báo MODEL_PREFLIGHT_FAILED thì dừng, kiểm tên, đường dẫn và file hash trên Volume; tuyệt đối không bỏ qua kiểm checksum.

## 7. Runtime CUDA được ghim theo revision cụ thể

Modal image dùng nvidia/cuda:12.8.1-devel-ubuntu22.04, clone stable-diffusion.cpp, checkout revision **77b72a2efed78f55de26892c7e909cee001e8b83**, cập nhật submodule rồi build với SD_CUDA=ON và CUDA architecture 86 cho A10G. Binary đích: /opt/sd-source/build/bin/sd-cli.

Cấu hình sử dụng revision inference engine được ghim và CUDA target A10G. Hãy kiểm tương thích trên phần cứng thực tế. Nếu build thất bại, lưu log và báo FAIL; không tự chuyển sang master mới nhất. Tham khảo [hướng dẫn build](https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/build.md) và [Mage-Flow](https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/mage_flow.md).

## 8. Chạy thử GPU A10G (bước có tính phí)

Kiểm tra quota/chi phí Modal và chủ động chạy:

~~~bash
modal run modal_app.py::generate_pair
~~~

Function kiểm lại cả năm SHA256, chạy hai lệnh sd-cli, tạo SOURCE.png và P2.png 1024×1024, kiểm header/kích thước PNG rồi commit output và report.json vào Volume riêng. Khi có lỗi thì dừng và báo lỗi, không tạo báo cáo PASS giả.

Lấy run ID thực tế từ kết quả, sau đó tải ảnh và report về:

~~~bash
modal volume ls compactfaces-example-results-v1 /
modal volume get compactfaces-example-results-v1 YOUR_RUN_ID/SOURCE.png ./SOURCE.png
modal volume get compactfaces-example-results-v1 YOUR_RUN_ID/P2.png ./P2.png
modal volume get compactfaces-example-results-v1 YOUR_RUN_ID/report.json ./report.json
~~~

Thay YOUR_RUN_ID bằng mã được in ra. Người dùng **phải tự xem ảnh** để đánh giá giữ danh tính và đúng hướng quay; checksum đúng không chứng minh chất lượng ảnh đạt.

## 9. Kiểm tra kết quả GPU

Sau khi chạy `modal_app.py::generate_pair`, kiểm thư mục kết quả có `SOURCE.png`, `P2.png` và `report.json`. Đối chiếu kích thước và SHA256, rồi đánh giá trực quan góc mặt và độ nhất quán danh tính. Hash khớp không chứng minh chất lượng hình ảnh.

Ví dụ hai ảnh này không tái tạo lại dataset đang phân phối.

## 10. Xử lý lỗi và ghi nhận kết quả

| Tình trạng | Hướng xử lý |
|---|---|
| Chưa đăng nhập đúng Modal | Chạy modal setup, xác nhận workspace |
| Không thấy Volume | Kiểm tên Volume và environment |
| MODEL_PREFLIGHT_FAILED | Kiểm file/hash thực tế; không bỏ qua |
| CMake/CUDA build lỗi | Giữ log, đánh dấu build chưa PASS |
| sd-cli không nhận tham số | So phiên bản binary với API/flag tương ứng |
| GPU hết VRAM hoặc timeout | Ghi lại lỗi, GPU và thời lượng thực tế |
| Có PNG nhưng pose/danh tính sai | Lưu bằng chứng, báo chưa đạt kiểm trực quan |

Nên lưu: Git commit, Modal SDK, loại GPU, revision sd.cpp, SHA256 của model/ảnh, seed, prompt, thời lượng, run ID, kết quả review và toàn bộ check SKIPPED. Không lưu token hoặc file model private trong Git.

**Ví dụ này không tạo endpoint công khai, không deploy dịch vụ chạy thường trực và không tự xóa dữ liệu Volume.** Người dùng tự kiểm soát phí GPU/storage và quyền phân phối model.

[Chuẩn bị model](MODEL_SETUP.vi.md) · [Nguồn model](MODEL_PROVENANCE.vi.md) · [Tái lập](reproducibility.vi.md)
