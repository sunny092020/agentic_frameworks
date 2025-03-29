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
                "model": "gpt-4o-mini",
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
        base_url = os.environ.get("LM_STUDIO_BASE_URL", "http://host.docker.internal:1234/v1")
        model = os.environ.get("LM_STUDIO_MODEL", "default_model")
        
        print(f"Connecting to LM Studio at: {base_url}")
        
        config_list = [
            {
                "model": model,
                "base_url": base_url,
                "api_key": "not-needed",  # LM Studio doesn't require an API key
                "price": [0.0, 0.0]  # Add pricing information [prompt_price_per_1k, completion_price_per_1k]
            }
        ]
        
        llm_config = {
            "config_list": config_list,
            "temperature": 0.7,
        }
        
        return llm_config
    
    @staticmethod
    def get_deepseek_config():
        """Get DeepSeek API configuration."""
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
            
        base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        model = os.environ.get("DEEPSEEK_MODEL", "deepseek-reasoner")
        
        print(f"Connecting to DeepSeek API at: {base_url}")
        
        config_list = [
            {
                "model": model,
                "base_url": base_url,
                "api_key": api_key,
                "price": [0.0005, 0.0015]  # Approximate pricing [prompt_price_per_1k, completion_price_per_1k]
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
        elif provider == "deepseek":
            return LLMConfig.get_deepseek_config()
        else:
            raise ValueError(f"Unsupported provider: {provider}") 