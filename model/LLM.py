import requests
import os
from dotenv import load_dotenv
from data.data import save_message
load_dotenv() # load env from file.env
from model.prompts import PromptTemplates

class LLM:
    def __init__(self, model_name = "meta-llama/llama-3.3-70b-instruct:free"):
        API_KEY =  os.getenv("API_KEY") # get env
        self.model = model_name # set model
        self.url =  "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        } # header to push url

    def get_respone(self, context, question):
        prompt = self.get_prompt(context, question)
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 195
        }

        response = requests.post(self.url, headers=self.headers, json=data) # post to api
        result = response.json()
        
        data = result['choices'][0]['message']['content']
        save_message(question, data)
        return data


    def get_prompt(self, context: str, question: str) -> str:
        prompt_type = PromptTemplates.detect_prompt_type(question)
        return PromptTemplates.get_prompt(prompt_type, document_content=context, question=question)
    