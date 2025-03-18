from fastapi import APIRouter, File, UploadFile
import os
import PyPDF2
from model.document import PDFEmbeddingFAISS

router = APIRouter()
model = PDFEmbeddingFAISS()

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_path = f'./tmp/{file.filename}'

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
    model.save_multil(file.filename, texts)

    return {"filename": file.filename, "content_type": file.content_type}

def read_content(pdf_path, chunk=50, chunk_k=25):
    reader = PyPDF2.PdfReader(pdf_path)  # read PDF
    texts = []
    
    for page in reader.pages:
        text = page.extract_text()  
        words = text.split()  # split
        num_words = len(words)
        
        i = 0
        while i < num_words:
            chunk_text = " ".join(words[i:i+chunk])  # combine to word
            texts.append(chunk_text)
            i += chunk_k  
            
            if i + chunk > num_words:
                break  # break if end

    return texts