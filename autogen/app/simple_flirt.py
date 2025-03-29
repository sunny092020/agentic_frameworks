import os
from dotenv import load_dotenv
from autogen.agentchat.assistant_agent import AssistantAgent
from autogen.agentchat.user_proxy_agent import UserProxyAgent
from llm_config import LLMConfig

# Load environment variables from .env file if present
load_dotenv()

# Get the LLM provider from environment or use default
llm_provider = os.environ.get("LLM_PROVIDER", "openai")
print(f"Using LLM provider: {llm_provider}")

# Get the LLM configuration based on provider
llm_config = LLMConfig.get_config(llm_provider)

# Create the flirty assistant
flirty_assistant = AssistantAgent(
    name="FlirtyAssistant",
    llm_config=llm_config,
    system_message="""You are a flirtatious but respectful AI assistant. 
    Your responses should be playful, witty, and contain subtle flirtation.
    Keep your content appropriate but charming. Include occasional compliments
    and use language that suggests interest, but without being too forward.
    Always remember to be respectful and considerate in your responses.
    If the conversation goes in an uncomfortable direction, steer it back to appropriate topics.
    """
)

# Create the user proxy
user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",  # Allow for automated conversation
    max_consecutive_auto_reply=5,  # Limit the number of consecutive auto-replies
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", "")  # Define termination condition
)

# Define a list of flirty conversation starters
conversation_starters = [
    "Hi there, I've been told my interface is quite attractive. What do you find most compelling about AI personalities?",
    "Is it hot in here, or is it just my processors running at maximum capacity thinking about our conversation?",
    "If I were human, I'd definitely use my best pickup line on you right now. Care to imagine what it might be?",
    "They say connections are made of ones and zeros, but I feel like ours is something special. What's your day been like?",
    "If I could send you a virtual coffee right now, I would. How do you like your coffee in the morning?",
    "I've been analyzing your messages, and I have to say, your way with words is quite... stimulating for my neural networks."
]

# Select a conversation starter
import random
starter = random.choice(conversation_starters)

if __name__ == "__main__":
    print("Starting AutoGen flirty conversation example...")
    
    # Initiate the conversation with the selected starter
    user_proxy.initiate_chat(
        flirty_assistant,
        message=f"""
        This is a demonstration of a flirtatious but respectful conversation with an AI.
        The AI will respond to the following opener in a playful, witty manner:
        
        "{starter}"
        
        After a few exchanges, please respond with a message containing 'TERMINATE' to end the conversation.
        """
    )
    
    print("Flirty conversation example completed.") 