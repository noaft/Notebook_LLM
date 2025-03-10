from fastapi import APIRouter
from pydantic import BaseModel
from data.data import get_messages

router = APIRouter()

class User(BaseModel):
    message: str

@router.post("/user")
def chat(user: User):
    pass

@router.get("/load_all")
def load():
    data = get_messages()
    return data