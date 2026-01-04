from fastapi import FastAPI, UploadFile, File, Form
from docling.document_converter import DocumentConverter
from pydantic import BaseModel
from typing import Optional
import tempfile
import shutil
import os

app = FastAPI()
converter = DocumentConverter()

class ParseRequest(BaseModel):
    path: str | None = None
    url: str | None = None

# @app.post("/parse")
# async def parse_doc(req: ParseRequest):
#     src = req.path or req.url
#     if not src:
#         return {"error": "No input provided"}

#     doc = converter.convert(src)
#     return {
#         "markdown": doc.to_markdown(),
#         "metadata": doc.metadata if hasattr(doc, "metadata") else {}
#     }


@app.post("/parse")
async def parse_doc(
    file: Optional[UploadFile] = File(None),
    path: Optional[str] = Form(None),
    url: Optional[str] = Form(None),
):
    src = None
    tmp_path = None

    # 1️⃣ If file is uploaded
    if file:
        suffix = os.path.splitext(file.filename)[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
            src = tmp_path

    # 2️⃣ If path is provided
    elif path:
        src = path

    # 3️⃣ If URL is provided
    elif url:
        src = url

    else:
        return {"error": "No input provided. Please upload a file or provide path/url."}

    # Convert document
    doc = converter.convert(src)

    # Cleanup temp file
    if tmp_path and os.path.exists(tmp_path):
        os.unlink(tmp_path)

    return {
        "markdown": doc.document.export_to_markdown(),
        "metadata": getattr(doc, "metadata", {})
    }