# MarkIt

Convert URLs and files to Markdown using Microsoft's MarkItDown library.

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
