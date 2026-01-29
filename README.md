# MarkIt

A simple web interface and API for converting URLs and files to Markdown.

Powered by [MarkItDown](https://github.com/microsoft/markitdown) from Microsoft.

## Supported Formats

- PDF
- Word, PowerPoint, Excel
- HTML
- Images (with EXIF metadata)
- Audio (with speech transcription)
- CSV, JSON, XML
- ZIP files
- YouTube URLs
- EPubs

## Setup

```bash
uv sync
```

## Run

```bash
uv run uvicorn main:app --reload
```

Open http://localhost:8000

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Landing page |
| GET | `/health` | Health check |
| GET | `/convert?url=<url>` | Convert URL to markdown |
| GET | `/convert/{url:path}` | Convert URL (path-style) |

## Docker

```bash
docker build -t markit .
docker run -p 8000:8000 markit
```

## Examples

```bash
curl "http://localhost:8000/convert?url=https://example.com"
```

## License

MIT
