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
        prompt = f"You are an advanced AI assistant with deep knowledge across various domains. Based on the given context:  \
            {context}  \
            Analyze the information, extract key points, and generate a concise and accurate response. Answer in the language of the question:  \
            {question}  \
            Ensure your response is precise, well-structured, and contextually relevant. Use logical reasoning and background knowledge if necessary to enhance clarity and coherence.\
            " # promt model
        
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
