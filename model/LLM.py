import requests
import os
import logging
from typing import Optional, Dict, Any, List, Iterator
from dotenv import load_dotenv
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.outputs import GenerationChunk

# Load .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLM_model(LLM):
    model: str = "meta-llama/llama-3.3-70b-instruct:free"
    api_key: Optional[str] = None
    max_tokens: int = 195
    temperature: float = 0.7
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    timeout: int = 30

    # Internal fields (not Pydantic-managed)
    url: str = "https://openrouter.ai/api/v1/chat/completions"
    headers: Dict[str, str] = {}

    def __init__(self, **kwargs):
        # Use Pydantic BaseModel init
        super().__init__(**kwargs)

        # Set api_key from environment if not passed
        self.api_key = self.api_key or os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either directly or via environment variables")

        # Construct headers
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.model = self.model# Replace '/' with '-' for URL compatibility

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call OpenRouter API."""
        try:
            data = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": kwargs.get("max_tokens", self.max_tokens),
                "temperature": kwargs.get("temperature", self.temperature),
                "top_p": kwargs.get("top_p", self.top_p),
                "frequency_penalty": kwargs.get("frequency_penalty", self.frequency_penalty),
                "presence_penalty": kwargs.get("presence_penalty", self.presence_penalty),
            }

            logger.info(f"Sending request to {self.model} with prompt: {prompt[:30]}...")

            response = requests.post(
                self.url,
                headers=self.headers,
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            output = result['choices'][0]['message']['content']

            logger.info(f"Received response of length {len(output)}")
            return output

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    def _stream(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[GenerationChunk]:
        """Simulated streaming output (char-by-char)."""
        for char in prompt[:100]:  # Simulate max 100 tokens
            chunk = GenerationChunk(text=char)
            if run_manager:
                run_manager.on_llm_new_token(chunk.text, chunk=chunk)
            yield chunk

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {"model_name": self.model}

    @property
    def _llm_type(self) -> str:
        return "custom"


# ✅ Example usage
if __name__ == "__main__":
    llm = LLM_model(
        model="meta-llama/llama-3.3-70b-instruct:free",
        api_key=os.getenv("API_KEY"),
        max_tokens=100
    )
    prompt = "What is the capital of France?"
    response = llm.invoke(prompt)
    print(f"Response: {response}")
