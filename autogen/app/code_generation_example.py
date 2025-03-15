import os
from dotenv import load_dotenv
from autogen.agentchat.assistant_agent import AssistantAgent
from autogen.agentchat.user_proxy_agent import UserProxyAgent

# Load environment variables from .env file if present
load_dotenv()

# Get OpenAI API key from environment
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Create the temperature data file in the workspace directory
def create_temperature_data(workspace_dir):
    # Ensure workspace directory exists
    os.makedirs(workspace_dir, exist_ok=True)
    
    data_path = os.path.join(workspace_dir, "temperature_data.csv")
    
    # Write the temperature data
    with open(data_path, "w") as f:
        f.write("""date,location,temperature
2023-01-01,New York,32.5
2023-01-02,New York,31.2
2023-01-03,New York,33.7
2023-01-04,New York,36.1
2023-01-05,New York,35.8
2023-01-06,New York,28.9
2023-01-07,New York,27.5
2023-01-01,San Francisco,58.3
2023-01-02,San Francisco,57.9
2023-01-03,San Francisco,59.2
2023-01-04,San Francisco,62.1
2023-01-05,San Francisco,60.5
2023-01-06,San Francisco,61.8
2023-01-07,San Francisco,63.2
2023-01-01,Chicago,22.1
2023-01-02,Chicago,20.8
2023-01-03,Chicago,19.5
2023-01-04,Chicago,21.3
2023-01-05,Chicago,24.7
2023-01-06,Chicago,26.2
2023-01-07,Chicago,23.9""")
    
    print(f"Created temperature dataset at: {data_path}")
    return data_path

# Configure OpenAI
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

# Create an AssistantAgent instance named "assistant"
assistant = AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    system_message="""You are a helpful AI assistant with expertise in Python programming.
    Always provide complete, runnable code blocks that can execute independently.
    Make sure all variables are defined before they are used.
    Use a step-by-step approach that keeps all the needed variables in scope."""
)

# Create a UserProxyAgent instance named "user_proxy" with code execution capabilities
user_proxy = UserProxyAgent(
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
    # Create workspace directory and dataset
    workspace_dir = os.path.join(os.getcwd(), "workspace")
    data_path = create_temperature_data(workspace_dir)
    
    print("Starting AutoGen code generation example...")
    
    # Initiate a chat with the assistant
    user_proxy.initiate_chat(
        assistant,
        message=f"""
Please help me with the following tasks. For each task, provide a complete, runnable Python code block that I can execute:

TASK 1: Load the temperature data from this file: {data_path}
Use this exact code to start your solution:
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('{data_path}')

# Display basic information
print(df.head())
print(df.info())
```

TASK 2: Calculate the average temperature for each location
Make sure to use the DataFrame created in Task 1.

TASK 3: Create a visualization of temperature trends for each location over time

TASK 4: Save the visualization as a PNG file

Execute each code block separately and verify it works before proceeding to the next task.
After completing all tasks, please respond with 'TERMINATE'.
"""
    )
    
    print("Code generation example completed.") 