import os
import json
# from typing import Dict, List, Optional
from typing import Dict, List, Optional, AsyncGenerator

import google.generativeai as genai
from velocityai.llms.base import BaseLLM
from velocityai.llms.config import LLMConfig

class GeminiLLM(BaseLLM):
    """Gemini implementation of the LLM interface."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-1.5-pro",
        temperature: float = 0.7,
        top_p: float = 0.95,
        top_k: int = 40,
        max_output_tokens: int = 8192,
    ):
        """
        Initialize Gemini LLM with simple configuration.
        
        Args:
            api_key: Gemini API key. If not provided, will look for GEMINI_API_KEY in environment
            model: Name of the model to use
            temperature: Controls randomness (0.0 to 1.0)
            top_p: Controls diversity via nucleus sampling (0.0 to 1.0)
            top_k: Controls diversity via top-k sampling
            max_output_tokens: Maximum number of tokens to generate
        """
        super().__init__()
        
        # Configure API
        api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Gemini API key is required")
        
        genai.configure(api_key=api_key)
        
        # Create internal config
        self.config = LLMConfig(
            model_name=model,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_output_tokens=max_output_tokens
        )
        
        # Create model
        self.model = genai.GenerativeModel(
            model_name=self.config.model_name,
            generation_config={
                "temperature": self.config.temperature,
                "top_p": self.config.top_p,
                "top_k": self.config.top_k,
                "max_output_tokens": self.config.max_output_tokens,
            }
        )
        
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response for the given prompt."""
        response = self.model.generate_content(prompt)
        return response.text
        
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a response in a chat context."""
        chat = self.model.start_chat(history=[])
        
        for message in messages:
            if message["role"] == "user":
                response = chat.send_message(message["content"])
            elif message["role"] == "assistant":
                # For assistant messages, we just keep them in history
                continue
            elif message["role"] == "system":
                # Prepend system message to the first user message
                continue
                
        return response.text

    async def stream_generate_content(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream generate content for the given prompt."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.config.model_name}:streamGenerateContent?alt=sse&key={os.getenv('GEMINI_API_KEY')}"
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({"contents": [{"parts": [{"text": prompt}]}]})
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                async for line in response.content:
                    if line:
                        chunk = json.loads(line.decode('utf-8'))
                        yield chunk['candidates'][0]['content']['parts'][0]['text']

    def _parse_json_response(self, text: str) -> Dict:
        """Parse JSON response from the model."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"type": "error", "content": "Failed to parse JSON response"} 