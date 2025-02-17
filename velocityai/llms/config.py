from typing import Dict, Optional
from pydantic import BaseModel, Field, ConfigDict

class LLMConfig(BaseModel):
    """Configuration for Language Models."""
    
    model_config = ConfigDict(protected_namespaces=())
    
    # Model settings
    model_name: str = Field(
        default="gemini-1.5-pro",
        description="Name of the model to use"
    )
    
    # Generation settings
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Controls randomness in the output. Higher values make the output more random"
    )
    
    top_p: float = Field(
        default=0.95,
        ge=0.0,
        le=1.0,
        description="Controls diversity via nucleus sampling"
    )
    
    top_k: int = Field(
        default=40,
        ge=1,
        description="Controls diversity via top-k sampling"
    )
    
    max_output_tokens: int = Field(
        default=8192,
        ge=1,
        description="Maximum number of tokens to generate"
    )
    
    @classmethod
    def default(cls) -> "LLMConfig":
        """Get default configuration."""
        return cls()
    
    def merge(self, updates: Dict) -> "LLMConfig":
        """Create new config by merging updates with current config."""
        data = self.model_dump()
        data.update(updates)
        return LLMConfig(**data) 