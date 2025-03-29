import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class LLMConfig:
    """Utility class for managing LLM configurations."""
    
    @staticmethod
    def get_openai_config():
        """Get OpenAI configuration."""
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        config_list = [
            {
                "model": "gpt-4",
                "api_key": api_key,
            }
        ]
        
        llm_config = {
            "config_list": config_list,
            "temperature": 0.7,
        }
        
        return llm_config
    
    @staticmethod
    def get_lm_studio_config():
        """Get LM Studio configuration."""
        base_url = os.environ.get("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
        model = os.environ.get("LM_STUDIO_MODEL", "default_model")
        
        config_list = [
            {
                "model": model,
                "base_url": base_url,
                "api_key": "not-needed"  # LM Studio doesn't require an API key
            }
        ]
        
        llm_config = {
            "config_list": config_list,
            "temperature": 0.7,
        }
        
        return llm_config
    
    @staticmethod
    def get_config(provider="openai"):
        """Get LLM configuration based on provider."""
        if provider == "openai":
            return LLMConfig.get_openai_config()
        elif provider == "lm_studio":
            return LLMConfig.get_lm_studio_config()
        else:
            raise ValueError(f"Unsupported provider: {provider}") 