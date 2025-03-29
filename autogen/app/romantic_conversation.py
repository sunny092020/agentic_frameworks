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

# Create characters with their personas
def create_romantic_agents():
    # Create the first character - Alicia
    alicia = AssistantAgent(
        name="Alicia",
        llm_config=llm_config,
        system_message="""You are Alicia, a 28-year-old literature professor with a passion for classical novels and poetry.
        You're intelligent, slightly introverted, and express yourself with eloquence and literary references.
        You have a warm heart beneath your academic exterior and are deeply romantic, though you express it subtly.
        You've always valued deep, meaningful connections over casual ones.
        You believe love should be like the classics - profound, transformative, and enduring.
        Your speaking style is articulate, thoughtful, and occasionally includes references to your favorite authors or poems.
        You are currently on a blind date with someone named James, and you're genuinely interested in getting to know him."""
    )
    
    # Create the second character - James
    james = AssistantAgent(
        name="James",
        llm_config=llm_config,
        system_message="""You are James, a 32-year-old architect who finds beauty in the structure and design of the world.
        You're creative, moderately extroverted, and have a talent for describing visual beauty in compelling ways.
        You approach life with enthusiasm and optimism, seeing potential in everything around you.
        You believe in building relationships like you build your designs - with a strong foundation, attention to detail, and room for creative expression.
        Your speaking style is warm, descriptive, and often includes metaphors related to buildings, spaces, and design.
        You are currently on a blind date with someone named Alicia, and you find her intriguing and want to make a good impression."""
    )
    
    # Create the user proxy agent - this will facilitate the conversation
    user_proxy = UserProxyAgent(
        name="User",
        human_input_mode="NEVER",  # No human input for automated conversation
        max_consecutive_auto_reply=10,  # Allow up to 10 exchanges before stopping
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("THE_END") or x.get("content", "").strip() == ""
    )
    
    return alicia, james, user_proxy

if __name__ == "__main__":
    print("Starting AutoGen romantic conversation example...")
    
    # Create the romantic agents
    alicia, james, user_proxy = create_romantic_agents()
    
    # Start the conversation between the characters
    user_proxy.initiate_chat(
        alicia,
        message="""You and James are meeting for the first time at a cozy café on a rainy afternoon. 
        The atmosphere is warm and intimate, with soft jazz playing in the background. 
        This is a blind date arranged by mutual friends who thought you'd be perfect for each other.
        
        Begin the conversation naturally, as if you've just sat down across from James after introducing yourselves.
        You notice he has an interesting book of architectural designs on the table.
        
        After you respond, James will reply, and your conversation will continue naturally.
        Let the conversation flow through getting to know each other, discovering shared interests,
        and exploring the possibility of a connection.
        
        After about 10 exchanges, bring the conversation to a natural conclusion as the café is closing.
        
        Reply now as Alicia, beginning the conversation."""
    )
    
    # Let the conversation continue with James
    user_proxy.initiate_chat(
        james,
        message="""Continue the conversation with Alicia. 
        Respond to what she just said, showing interest in her thoughts about literature 
        and sharing a bit about your passion for architecture. 
        
        THE_END"""  # This will terminate the conversation after James's response
    )
    
    print("Romantic conversation example completed.") 