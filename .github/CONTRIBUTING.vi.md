# Đóng góp cho CompactFaces

> 🌐 Language / Ngôn ngữ: [English](CONTRIBUTING.md) | **Tiếng Việt**

Chào đón đóng góp cho mã nguồn, công cụ kiểm thử, bản dịch và tài liệu của repository. **Không commit PNG gốc của dataset, ảnh người thật, checkpoint model hoặc token.**

## Phát triển

Dùng Python 3.10+ cho test CPU; Node.js để kiểm tra cú pháp JavaScript. GPU chỉ cần khi chủ động chạy smoke test SOURCE/P2.

```bash
python3 scripts/verify_dataset.py examples --expected-images 10 --expected-families 2
python3 scripts/validate_repository.py
node --check website_src/app.js && node --check website_src/pages.js
bash -n scripts/reproduce_source_pose_example.sh
```

## Chính sách tài liệu và review

- Mỗi Markdown có cặp Anh/Việt: `file.md` và `file.vi.md`.
- Sửa hai bản cùng lúc và có link chuyển ngôn ngữ đúng.
- Code commit nên nhỏ, dưới khoảng 600 dòng thay đổi; cặp tài liệu song ngữ dài được phép lớn hơn.
- Nêu rõ lý do, kiểm thử, tác động lên provenance và điều kiện công bố.
- Không xem WebP preview là PNG nguồn 1024px; 935 PNG gốc không thuộc repository này.
- Xem [kiểm dữ liệu](../docs/validation.vi.md) và [điều kiện phát hành](../docs/release-checklist.vi.md).

Code/docs của repository có MIT; quyền phân phối ảnh không nằm trong MIT này. Xem [phạm vi license](../LICENSE-NOTES.vi.md).
