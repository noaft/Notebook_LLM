from fastapi import APIRouter, File, UploadFile
import os
import PyPDF2
from model.document import PDFEmbeddingFAISS

router = APIRouter()
model = PDFEmbeddingFAISS()

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_path = './tmp/data.pdf'

    # Ensure the directory exists
    os.makedirs('./tmp', exist_ok=True)

    # Remove existing file
    if os.path.isfile(file_path):
        os.remove(file_path)

    # Save the uploaded file
    with open(file_path, 'wb') as f:
        f.write(await file.read())

    # Process the PDF
    texts = read_content(file_path)  
    model.save_multil(texts)

    return {"filename": file.filename, "content_type": file.content_type}

def read_content(pdf_path, chunk=200, chunk_k=100):
    reader = PyPDF2.PdfReader(pdf_path)  # Open PDF
    texts = []
    for page in reader.pages:
        text = page.extract_text()  # Extract text
        text_len = len(text) 
        i = 0 
        while i < text_len:
            chunk_text = text[i:i+chunk].strip()
            texts.append(chunk_text)
            if chunk_text:  # Only process non-empty text
                i += chunk_k

    return texts
