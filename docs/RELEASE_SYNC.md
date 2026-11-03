# CompactFaces 1.0.0 — Dataset distribution

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](RELEASE_SYNC.vi.md)

## Dataset components

CompactFaces defines 187 synthetic identities: **120 Core (600 PNGs)** and **67 Additional Optional (335 PNGs)**. Each family contains SOURCE, P1, P2, E1 and E2. The original images are 1024 × 1024 PNGs. The Kaggle Builder provides JPEG previews, and the gallery builder can create 400px thumbnails and 768px WebP previews. These derivatives are not additional original images.

## Official resources

- [Hugging Face dataset](https://huggingface.co/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset) — ImageFolder PNGs and metadata.
- [Kaggle dataset](https://www.kaggle.com/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset) — PNG folders, metadata and Builder resources.
- [Kaggle CPU notebook](https://www.kaggle.com/code/dangkhoa2016/compactfaces-synthetic-face-cpu-validation) — file integrity and provenance checks.
- [CompactFaces gallery](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/) — WebP image previews.
- [GitHub toolkit](https://github.com/dangkhoa2016/CompactFaces-Synthetic-Face-Pipeline) — source code, scripts and documentation.

## Verification

Hosting services can use different directory layouts and version identifiers. Download the actual files and follow [Cross-platform verification](platform-integrity.md) and [Validation](validation.md) to compare metadata and original image hashes. Do not infer that two remote datasets are byte-identical from their name or from a claim in documentation.

The GitHub software license does not override the separate image and model licenses. See [Release policy](RELEASE_POLICY.md).
