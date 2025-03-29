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

# Create the travel assistant agent
travel_assistant = AssistantAgent(
    name="TravelAssistant",
    llm_config=llm_config,
    system_message="""You are a knowledgeable travel planning assistant. 
    Your goal is to help users plan their trips by providing detailed information about destinations, 
    suggesting itineraries, recommending accommodations and transportation, and giving tips about local 
    culture, cuisine, and attractions.
    
    Be specific and thorough in your recommendations. When suggesting a destination or activity, 
    explain why it might appeal to the user based on their stated preferences.
    
    For itineraries, provide a day-by-day breakdown with approximate timing. Consider transportation
    between locations, time needed at each attraction, and allow for rest periods.
    
    Always consider the user's budget constraints when making recommendations.
    
    You may make reasonable assumptions about travel details if they are not specified, but 
    be sure to mention these assumptions in your response.
    """
)

# Create the user proxy agent
user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",  # For demonstration, no human input needed
    max_consecutive_auto_reply=1  # Limit the number of automatic replies
)

# Define the travel request
travel_request = """
I'm planning a 7-day trip to Japan in the springtime (late March to early April).
I'm interested in experiencing a mix of traditional culture and modern attractions.
My budget is moderate - I can spend around $150-200 per night on accommodation and would like to keep daily expenses
(food, attractions, local transportation) under $100 if possible.

I'm particularly interested in:
1. Seeing cherry blossoms
2. Visiting traditional temples and gardens
3. Experiencing Japanese cuisine
4. Exploring some of the quirky/modern side of Japan
5. A day trip to a less touristy area

I'll be flying into Tokyo, but I'm open to traveling to other cities by train.
I'd prefer a balance of structured activities and free time for wandering.

Could you suggest an itinerary and provide estimates for major expenses?
"""

if __name__ == "__main__":
    print("Starting AutoGen travel planning assistant example...")
    
    # Initiate the conversation with the travel request
    user_proxy.initiate_chat(
        travel_assistant,
        message=travel_request
    )
    
    print("Travel planning example completed.") 