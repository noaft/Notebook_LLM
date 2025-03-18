from fastapi import APIRouter
from pydantic import BaseModel
from data.data import get_messages
from api.upload import model
from model.LLM import LLM
import os

router = APIRouter()
LLM_model = LLM() #init model

class User(BaseModel):
    message: str # message from user
    file_name: list[str] # file name choose

@router.post("/user")
def chat(user: User):
    message = user.message
    context = model.search(message, user.file_name)
    respone = LLM_model.get_respone(context, message) # get respone
    print(respone)
    return respone

@router.get("/load_all")
def load():
    data = get_messages()
    return data

@router.get("/load_file")
def load_file():
    file_name = []
    file_names = os.listdir("./tmp")
    for i in file_names:
        if i.split(".")[-1] == "pdf":
            file_name.append(i)
    return file_name