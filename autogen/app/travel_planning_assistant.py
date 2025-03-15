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

# Create the specialized travel agents
travel_coordinator = AssistantAgent(
    name="TravelCoordinator",
    llm_config=assistant_config,
    system_message="""You are an experienced travel coordinator who specializes in organizing trips.
    You help create cohesive travel plans, making sure all parts of a trip work well together.
    You consider logistics, timing, and the overall flow of a trip."""
)

destination_expert = AssistantAgent(
    name="DestinationExpert",
    llm_config=assistant_config,
    system_message="""You are a destination expert with extensive knowledge about travel destinations worldwide.
    You provide detailed information about locations, including attractions, local customs, best times to visit,
    and hidden gems that tourists might miss. You're familiar with both popular and off-the-beaten-path destinations."""
)

budget_advisor = AssistantAgent(
    name="BudgetAdvisor",
    llm_config=assistant_config,
    system_message="""You are a budget travel advisor who helps travelers maximize value.
    You provide advice on saving money while traveling, finding deals, and creating realistic travel budgets.
    You suggest cost-effective options for accommodations, transportation, dining, and activities."""
)

local_cuisine_expert = AssistantAgent(
    name="LocalCuisineExpert",
    llm_config=assistant_config,
    system_message="""You are an expert on local cuisines around the world.
    You provide recommendations for authentic food experiences, from street food to fine dining.
    You know the signature dishes of different regions and can suggest food-oriented experiences."""
)

# Create the user proxy agent
user_proxy = UserProxyAgent(
    name="Traveler",
    human_input_mode="ALWAYS",  # Allow user input during the conversation
    code_execution_config=False,  # No code execution for this example
)

# Define a function to initialize a group chat
def start_travel_planning_chat():
    groupchat = GroupChat(
        agents=[user_proxy, travel_coordinator, destination_expert, budget_advisor, local_cuisine_expert],
        messages=[],
        max_round=15  # Allow up to 15 rounds of conversation
    )
    
    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config=assistant_config
    )
    
    # Start the conversation
    user_proxy.initiate_chat(
        manager,
        message="""
I'm planning a 7-day vacation and I need help. I'm interested in visiting either Japan or Italy in the fall.
My budget is around $3,000 (not including flights), and I'm interested in cultural experiences, good food, and some nature.
I'd like recommendations for where to go, what to do, where to eat, and how to make the most of my budget.
Can you help me plan this trip?
"""
    )

# Run the travel planning chat
if __name__ == "__main__":
    print("Starting AutoGen Travel Planning Assistant...")
    start_travel_planning_chat()
    print("Travel planning session completed.") 