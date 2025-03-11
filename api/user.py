from fastapi import APIRouter
from pydantic import BaseModel
from data.data import get_messages
from api.upload import model
router = APIRouter()

class User(BaseModel):
    message: str

@router.post("/user")
def chat(user: User):
    message = user.message
    context = model.search(message)
    print(context)
    return "test"

@router.get("/load_all")
def load():
    data = get_messages()
    return data