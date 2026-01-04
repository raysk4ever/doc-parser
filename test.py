from docling.document_converter import DocumentConverter

converter = DocumentConverter(
    # enable_ocr=False,
    # enable_picture_description=False,
    # enable_table_structure=False
)
doc = converter.convert("Ravi_Resume.pdf")

markdown = doc.document.export_to_markdown()

with open("resume.md", "w") as f:
    f.write(markdown)
    
