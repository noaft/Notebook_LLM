from fastapi import APIRouter
from pydantic import BaseModel
from data.data import get_messages
from api.upload import model
from model.LLM import LLM
import os

router = APIRouter()
LLM_model = LLM()

class User(BaseModel):
    message: str
    file_name: str

@router.post("/user")
def chat(user: User):
    message = user.message
    context = model.search(message)
    respone = LLM_model.get_respone(context, message) # get respone
    print(respone)
    return respone

@router.get("/load_all")
def load():
    data = get_messages()
    return data

@router.get("/load_file")
def load_file():
    file_name = os.listdir("./tmp")
    return file_name