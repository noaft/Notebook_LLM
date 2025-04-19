import requests
import os
import logging
from typing import Optional, Dict, Any, List, Union
from dotenv import load_dotenv
from data.data import save_message
load_dotenv() # load env from file.env
from model.prompts import PromptTemplates

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLM:
    def __init__(
        self, 
        model_name: str = "meta-llama/llama-3.3-70b-instruct:free",
        api_key: Optional[str] = None,
        max_tokens: int = 195,
        temperature: float = 0.7,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        timeout: int = 30
    ):
        """
        Initialize the LLM class with configurable parameters.
        
        Args:
            model_name: Name of the model to use
            api_key: API key for authentication. If None, will try to get from environment
            max_tokens: Maximum number of tokens to generate
            temperature: Controls randomness in the output
            top_p: Controls diversity via nucleus sampling
            frequency_penalty: Penalizes repeated tokens
            presence_penalty: Penalizes new tokens
            timeout: Request timeout in seconds
        """
        self.model = model_name
        self.api_key = api_key or os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either directly or through environment variables")
            
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Model parameters
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.timeout = timeout

    def get_response(
        self, 
        context: str, 
        question: str,
        stream: bool = False,
        **kwargs
    ) -> Union[str, requests.Response]:
        """
        Get response from the LLM model.
        
        Args:
            context: Context for the question
            question: Question to ask
            stream: Whether to stream the response
            **kwargs: Additional parameters to override default settings
            
        Returns:
            Response from the model or streaming response object
        """
        try:
            prompt = self.get_prompt(context, question)
            
            # Prepare request data with default and override parameters
            data = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": kwargs.get('max_tokens', self.max_tokens),
                "temperature": kwargs.get('temperature', self.temperature),
                "top_p": kwargs.get('top_p', self.top_p),
                "frequency_penalty": kwargs.get('frequency_penalty', self.frequency_penalty),
                "presence_penalty": kwargs.get('presence_penalty', self.presence_penalty),
                "stream": stream
            }
            
            logger.info(f"Sending request to {self.model} with prompt length: {len(prompt)}")
            response = requests.post(
                self.url, 
                headers=self.headers, 
                json=data,
                timeout=self.timeout,
                stream=stream
            )
            
            response.raise_for_status()
            
            if stream:
                return response
                
            result = response.json()
            data = result['choices'][0]['message']['content']
            
            # Save conversation
            save_message(question, data)
            logger.info(f"Successfully got response with length: {len(data)}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise

    def get_prompt(self, context: str, question: str) -> str:
        """
        Get formatted prompt based on question type.
        
        Args:
            context: Context for the question
            question: Question to ask
            
        Returns:
            Formatted prompt string
        """
        prompt_type = PromptTemplates.detect_prompt_type(question)
        return PromptTemplates.get_prompt(prompt_type, document_content=context, question=question)
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available models from the API.
        
        Returns:
            List of available model names
        """
        try:
            response = requests.get(
                "https://openrouter.ai/api/v1/models",
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            models = response.json()
            return [model['id'] for model in models]
        except Exception as e:
            logger.error(f"Error getting available models: {str(e)}")
            return []
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model.
        
        Returns:
            Dictionary containing model information
        """
        try:
            response = requests.get(
                f"https://openrouter.ai/api/v1/models/{self.model}",
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting model info: {str(e)}")
            return {}
    