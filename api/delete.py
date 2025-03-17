from fastapi import APIRouter

router = APIRouter()

@router.post("/delete")
def delete(filename: str):
    pass