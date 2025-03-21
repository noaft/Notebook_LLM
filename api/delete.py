from fastapi import APIRouter
import os
from pydantic import BaseModel

router = APIRouter()

@router.post("/delete_one")
def delete(filename: str):
    extensions = [".pdf", ".json", ".bin"]
    filename_all = filename.split[".pdf"]
    for e in extensions:
        os.remove(f"./tmp/{filename_all}" + e)

    return "Success delete file"

class data(BaseModel):
    filenames: list[str]

@router.post("/delete")
def delete(data: data):
    for filename in data.filenames:
        extensions = [".pdf", ".json", ".bin"]
        filename_all = filename.split(".pdf")[0]
        for e in extensions:
            os.remove(f"./tmp/{filename_all}" + e)

    return "Success delete file"