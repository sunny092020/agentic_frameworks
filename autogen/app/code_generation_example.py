import os
import autogen
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Get OpenAI API key from environment
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Configure OpenAI
config_list = [
    {
        "model": "gpt-4",
        "api_key": api_key,
    }
]

llm_config = {
    "seed": 42,  # for reproducibility
    "config_list": config_list,
    "temperature": 0.7,
}

# Create an AssistantAgent instance named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    system_message="You are a helpful AI assistant with expertise in Python programming."
)

# Create a UserProxyAgent instance named "user_proxy" with code execution capabilities
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "workspace",
        "use_docker": False,  # Set to True to execute code in Docker
    }
)

if __name__ == "__main__":
    # Create workspace directory if it doesn't exist
    os.makedirs("workspace", exist_ok=True)
    
    print("Starting AutoGen code generation example...")
    
    # Initiate a chat with the assistant
    user_proxy.initiate_chat(
        assistant,
        message="""
        Please help me with the following tasks:
        
        1. Create a simple Python function that calculates the Fibonacci sequence up to n terms
        2. Create a visualization of this sequence using matplotlib
        3. Save the visualization as a PNG file
        
        After completing all tasks, please respond with 'TERMINATE'.
        """
    )
    
    print("Code generation example completed.") 