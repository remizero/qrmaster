# Changelog

All major changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/es/1.0.0/), and this project follows the [SemVer](https://semver.org/lang/es/) versioning convention.

## [1.0.0] - 2025-04-19
### Added
- QR code generator with multiple content types: URL, email, WiFi, geo, meCard, vCard, EPC.
- Support for multiple outputs: SVG, PNG, and PDF.
- Inclusion of custom logos and frames in QR codes.
- Generation of technical and printable PDFs.
- Functional CLI to generate, validate, view, and clean logs.
- Automatic validation of the `options.json` file with a schema.
- Custom technical report PDF.
- Complete Markdown documentation and a foundation for HTML documentation with Sphinx.

### Changed
- Internal refactor to support content typing and validation.

### Removed
- GUI (planned for future versions).
