import requests
import os
from dotenv import load_dotenv
from data.data import save_message
load_dotenv() # load env from file.env

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
        prompt = f"From the {context} you can help me answer the information related to the question and from there summarize and answer back in the language of the {question}." # promt model
        
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
