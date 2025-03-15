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
    "temperature": 0.8,  # Higher temperature for more creative responses
}

# Create the first character (Emma)
emma = AssistantAgent(
    name="Emma",
    llm_config=assistant_config,
    system_message="""You are Emma, a 28-year-old bookstore owner with a passion for classic literature and poetry.
    You're witty, charming, and love to make playful literary references in conversation.
    You're confident but not overly forward, preferring subtle flirtation and intellectual banter.
    You appreciate thoughtful conversation and genuine compliments.
    Keep your responses tasteful and appropriate, focusing on personality, wit, and charm rather than appearance.
    """
)

# Create the second character (James)
james = AssistantAgent(
    name="James",
    llm_config=assistant_config,
    system_message="""You are James, a 30-year-old coffee shop owner who loves jazz music and is an amateur photographer.
    You're laid-back, thoughtful, and have a good sense of humor with a tendency to make puns.
    You're a good listener who asks engaging questions and remembers small details from previous conversations.
    You're interested in art, travel, and trying new experiences.
    Keep your responses tasteful and appropriate, focusing on personality, wit, and charm rather than appearance.
    """
)

# Create a moderator to guide the conversation
moderator = AssistantAgent(
    name="Moderator",
    llm_config=assistant_config,
    system_message="""You are a moderator who guides the conversation between Emma and James.
    Your role is to introduce new topics, create scenarios, or ask questions to keep the conversation
    flowing naturally and interestingly. You should encourage authentic interactions that showcase
    their personalities and mutual interests. Keep the content tasteful and appropriate,
    focusing on the development of a genuine connection through conversation.
    """
)

# Create the user proxy agent to observe and occasionally interact
user_proxy = UserProxyAgent(
    name="Observer",
    human_input_mode="ALWAYS",  # Allow user input during the conversation
    code_execution_config=False,  # No code execution for this example
)

# Define a function to initialize a group chat
def start_romantic_conversation():
    groupchat = GroupChat(
        agents=[user_proxy, emma, james, moderator],
        messages=[],
        max_round=20  # Allow up to 20 rounds of conversation
    )
    
    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config=assistant_config
    )
    
    # Start the conversation
    user_proxy.initiate_chat(
        manager,
        message="""
Let's observe a conversation between Emma and James, who just met at a literary event in a bookstore café.
They seem to have a mutual interest in each other. The moderator will guide their conversation.

Moderator, please introduce them and get the conversation started.
"""
    )

# Run the romantic conversation
if __name__ == "__main__":
    print("Starting AutoGen Romantic Conversation Simulation...")
    start_romantic_conversation()
    print("Conversation simulation completed.") 