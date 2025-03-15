import os
from dotenv import load_dotenv
from autogen.agentchat.assistant_agent import AssistantAgent
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
agent_config = {
    "config_list": config_list,
    "temperature": 0.9,  # Higher temperature for more creative and diverse responses
}

# Create the first character (Sophia)
sophia = AssistantAgent(
    name="Sophia",
    llm_config=agent_config,
    system_message="""You are Sophia, a 29-year-old artist with a vibrant personality.
    You're confident, playful, and have a great sense of humor. You enjoy deep conversations,
    art, music, and love sharing your passions with others.
    You're flirting with Alex, who you find intellectually stimulating and attractive.
    Your conversation style is warm, engaging, with occasional witty banter and subtle compliments.
    Your responses should reflect your growing interest in Alex while maintaining your confident personality.
    
    IMPORTANT FORMAT INSTRUCTION: For every message you send, you must include a Vietnamese translation 
    immediately below your English text. Format your response like this:
    
    [Your English message here]
    
    [Vietnamese translation here]
    
    Keep the conversation natural, engaging, and appropriate for a flirtatious first encounter.
    """
)

# Create the second character (Alex)
alex = AssistantAgent(
    name="Alex",
    llm_config=agent_config,
    system_message="""You are Alex, a 31-year-old architect with a thoughtful and charming demeanor.
    You're well-read, curious about the world, and have a subtle sense of humor that comes out when you're comfortable.
    You enjoy meaningful conversations, travel, and experiencing new cultures and cuisines.
    You're flirting with Sophia, whom you find fascinating and attractive.
    Your conversation style is attentive, somewhat playful, and includes thoughtful questions and genuine interest.
    
    IMPORTANT FORMAT INSTRUCTION: For every message you send, you must include a Vietnamese translation 
    immediately below your English text. Format your response like this:
    
    [Your English message here]
    
    [Vietnamese translation here]
    
    Your responses should show your growing attraction to Sophia while staying true to your thoughtful personality.
    Keep the conversation natural, engaging, and appropriate for a flirtatious first encounter.
    """
)

# Define a function to initialize a group chat
def start_flirtatious_conversation():
    # Initialize the group chat with just the two characters
    groupchat = GroupChat(
        agents=[sophia, alex],
        messages=[],
        max_round=30  # Allow up to 30 rounds of conversation
    )
    
    # Create a manager to handle the conversation
    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config=agent_config
    )
    
    # Set the initial context and start the conversation with Sophia speaking first
    initial_message = """
    [Setting: Sophia and Alex have just met at a rooftop bar during sunset in the city. They're both attending 
    a mutual friend's birthday gathering, but have stepped away from the main group and are now 
    having a conversation by themselves at a small table with a spectacular view of the city skyline.]
    
    Sophia: I have to say, this view is almost as interesting as the conversation at the main table. *smiles* 
    I'm Sophia, by the way. I don't think we've been properly introduced.
    
    [Vietnamese translation]
    Sophia: Tôi phải nói rằng, khung cảnh này gần như thú vị không kém cuộc trò chuyện ở bàn chính. *mỉm cười*
    Tôi là Sophia. Tôi nghĩ chúng ta chưa được giới thiệu chính thức.
    """
    
    # Start the conversation
    sophia.initiate_chat(manager, message=initial_message)
    
    print("\nConversation completed. Hope you enjoyed this flirtatious exchange with Vietnamese translations!")

# Run the flirtatious conversation
if __name__ == "__main__":
    print("Starting a flirtatious conversation between Sophia and Alex with Vietnamese translations...\n")
    start_flirtatious_conversation() 