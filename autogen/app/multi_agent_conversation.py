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
    system_message="You are a Python programmer. You can translate concepts into efficient code."
)

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",  # No human input for non-interactive examples
    code_execution_config={},  # Use empty dict for default config instead of None
)

# Define a function to initialize a group chat
def start_group_chat():
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
        message="I need to analyze a dataset of temperatures and create a visualization. Can you help me?"
    )

# Run the group chat
if __name__ == "__main__":
    print("Starting AutoGen multi-agent conversation example...")
    start_group_chat()
    print("Conversation completed.") 