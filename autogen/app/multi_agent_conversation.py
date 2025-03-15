import os
from dotenv import load_dotenv
from autogen.agentchat.assistant_agent import AssistantAgent
from autogen.agentchat.user_proxy_agent import UserProxyAgent
from autogen.agentchat.groupchat import GroupChat, GroupChatManager

# Load environment variables from .env file if present
load_dotenv()

# Get OpenAI API key from environment
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Create the temperature data file in the current working directory
def create_temperature_data():
    current_dir = os.getcwd()
    data_path = os.path.join(current_dir, "temperature_data.csv")
    
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

# Create assistant agent configuration
assistant_config = {
    "config_list": config_list,
    "temperature": 0.7,
}

# Create the agents
assistant = AssistantAgent(
    name="Assistant",
    llm_config=assistant_config,
    system_message="You are a helpful AI assistant."
)

data_scientist = AssistantAgent(
    name="DataScientist",
    llm_config=assistant_config,
    system_message="You are a data scientist. You analyze data and create models."
)

programmer = AssistantAgent(
    name="Programmer",
    llm_config=assistant_config,
    system_message="""You are a Python programmer. You can translate concepts into efficient code. 
    Always check that your code runs properly and all variables are defined before they are used.
    Use a sequential approach where you first load data, then process it, and finally visualize it.
    Always execute your code in complete blocks that can run on their own."""
)

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",  # No human input for non-interactive examples
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "."  # Execute code in the current directory
    },  # Configured to execute in current directory
)

# Define a function to initialize a group chat
def start_group_chat():
    # Create the temperature data file
    data_path = create_temperature_data()
    
    groupchat = GroupChat(
        agents=[user_proxy, assistant, data_scientist, programmer],
        messages=[],
        max_round=10
    )
    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config=assistant_config  # Provide the LLM config to the manager
    )
    
    # Start the conversation
    user_proxy.initiate_chat(
        manager,
        message=f"""
I need to analyze a dataset of temperatures and create a visualization. 

Please use the file 'temperature_data.csv' which is available at: {data_path}
The file contains temperature data for different cities over a week period.

I'd like you to:

1. First, load and explore the dataset using this exact code:
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('{data_path}')

# Display the first few rows to understand the data
print(df.head())

# Get basic information about the dataset
print(df.info())
print(df.describe())
```

2. Second, calculate average temperatures by location (not by city):
```python
# Calculate average temperature by location
average_temps = df.groupby('location')['temperature'].mean()
print("Average Temperatures by Location:")
print(average_temps)
```

3. Finally, create a line chart visualization comparing the temperatures across locations:
```python
# Create a line chart of temperatures by date for each location
plt.figure(figsize=(12, 6))

for location in df['location'].unique():
    location_data = df[df['location'] == location]
    plt.plot(location_data['date'], location_data['temperature'], marker='o', label=location)

plt.title('Temperature Trends by Location')
plt.xlabel('Date')
plt.ylabel('Temperature (°F)')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Save the visualization
plt.savefig('temperature_trends.png')

# Show the plot
plt.show()
```

Please execute these code blocks in order, making sure each runs successfully before proceeding to the next.
"""
    )

# Run the group chat
if __name__ == "__main__":
    print("Starting AutoGen multi-agent conversation example...")
    start_group_chat()
    print("Conversation completed.") 