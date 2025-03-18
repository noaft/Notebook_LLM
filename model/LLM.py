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
        """
        Chọn prompt phù hợp dựa trên ngữ cảnh và câu hỏi.
        """
        question = question.strip().lower()

        # Prompt hỏi đáp chung
        qa_prompt = f"""
        You are an advanced AI assistant with deep expertise across multiple domains. 
        Your task is to analyze the given context and generate a well-structured, accurate, and contextually relevant response.

        **Context:**  
        {context}  

        **Question:**  
        {question}  

        **Instructions:**  
        - Carefully extract key information from the context.  
        - Answer in the same language as the question.  
        - Provide a clear, concise, and well-organized response.  
        - Use logical reasoning and background knowledge to enhance clarity.  
        - If necessary, include examples, step-by-step explanations, or supporting arguments to improve understanding.  

        Ensure your response is precise, insightful, and directly addresses the question.
        """

        # Prompt tóm tắt nội dung
        summary_prompt = f"""
        You are a highly intelligent AI assistant capable of summarizing complex information. 
        Given the context below, generate a concise, coherent, and accurate summary.

        **Context:**  
        {context}  

        **Instructions:**  
        - Summarize the key points clearly and concisely.  
        - Maintain accuracy while removing unnecessary details.  
        - Ensure the summary is easy to understand and well-structured.  
        """

        # Prompt hỗ trợ lập trình
        coding_prompt = f"""
        You are a skilled AI programming assistant with expertise in multiple programming languages. 
        Your task is to generate well-structured and efficient code based on the given instructions.

        **Context:**  
        {context}  

        **Question:**  
        {question}  

        **Instructions:**  
        - Write clean, efficient, and well-documented code.  
        - Follow best practices and optimize performance.  
        - Provide step-by-step explanations if necessary.  
        - Ensure the code is syntactically correct and functional.  
        """

        # Prompt sáng tạo nội dung (ví dụ: viết truyện, thơ)
        creative_prompt = f"""
        You are a highly creative AI assistant with a talent for storytelling and content generation. 
        Based on the given context, create an engaging and imaginative response.

        **Context:**  
        {context}  

        **Instructions:**  
        - Use vivid language and creativity.  
        - Ensure coherence and logical flow in your writing.  
        - Adapt your tone and style based on the given information.  
        """

        # Xác định loại câu hỏi
        if "?" in question:
            return qa_prompt
        elif len(question.split()) > 50:
            return summary_prompt
        elif any(keyword in question for keyword in ["python", "code", "function", "algorithm", "bug fix"]):
            return coding_prompt
        else:
            return creative_prompt  # Mặc định nếu không thuộc loại nào
    