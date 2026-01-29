import tempfile
import os
import logging
import validators
from urllib.parse import urlparse
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from markitdown import MarkItDown

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MarkIt", description="Convert URLs and files to Markdown")
templates = Jinja2Templates(directory="templates")
md = MarkItDown()

MAX_FILE_SIZE = 10 * 1024 * 1024


def validate_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    if not validators.url(url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    parsed = urlparse(url)
    hostname = parsed.netloc.split(":")[0]

    if not validators.domain(hostname):
        raise HTTPException(status_code=400, detail="Invalid URL: must be a valid FQDN")

    return url


def convert_url_to_markdown(url: str) -> str:
    url = validate_url(url)
    try:
        result = md.convert(url)
        return result.text_content
    except Exception as e:
        logger.exception("Failed to convert URL: %s", url)
        raise HTTPException(status_code=500, detail=f"Failed to convert URL: {str(e)}")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/convert", response_class=PlainTextResponse)
async def convert_url(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="URL parameter is required")
    content = convert_url_to_markdown(url)
    return PlainTextResponse(content=content, media_type="text/markdown")


@app.get("/convert/{url:path}", response_class=PlainTextResponse)
async def convert_url_path(url: str):
    content = convert_url_to_markdown(url)
    return PlainTextResponse(content=content, media_type="text/markdown")


@app.post("/convert", response_class=PlainTextResponse)
async def convert_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB")

    temp_path = None
    try:
        suffix = os.path.splitext(file.filename)[1] if file.filename else ""
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_path = temp_file.name
            temp_file.write(content)

        result = md.convert(temp_path)
        return PlainTextResponse(content=result.text_content, media_type="text/markdown")
    except Exception as e:
        logger.exception("Failed to convert file: %s", file.filename)
        raise HTTPException(status_code=500, detail=f"Failed to convert file: {str(e)}")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
