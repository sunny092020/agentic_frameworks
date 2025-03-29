import os
import json
from dotenv import load_dotenv
import autogen
from llm_config import LLMConfig

# Load environment variables from .env file if present
load_dotenv()

# Get the LLM provider from environment or use default
llm_provider = os.environ.get("LLM_PROVIDER", "openai")
print(f"Using LLM provider: {llm_provider}")

# Get the LLM configuration based on provider
llm_config = LLMConfig.get_config(llm_provider)

# Set up a research task
def setup_research_task():
    # Create an assistant agent to perform research
    assistant = autogen.AssistantAgent(
        name="Assistant",
        llm_config=llm_config,
        system_message="""You are a research assistant. Your goal is to provide accurate, factual 
        information about the given topic. Use your knowledge to provide well-structured, 
        comprehensive responses, but be honest about the limitations of your knowledge. 
        If you're uncertain about something, acknowledge it.
        """
    )
    
    # Create a user proxy agent that will converse with the assistant
    user_proxy = autogen.UserProxyAgent(
        name="User",
        human_input_mode="NEVER",  # No human input for automatic execution
        code_execution_config={"use_docker": False},  # Don't use Docker for code execution
        max_consecutive_auto_reply=5  # Allow up to 5 automatic replies before requiring user input
    )
    
    return assistant, user_proxy

def load_research_topics():
    """Load or create research topics if they don't exist."""
    research_topics = [
        {
            "topic": "Quantum Computing",
            "description": "Research the current state of quantum computing, including recent advancements, key players in the field, and potential applications. Include information about quantum bits (qubits), quantum gates, and quantum algorithms. Also discuss the challenges facing quantum computing and when we might expect practical quantum computers."
        },
        {
            "topic": "Climate Change Mitigation",
            "description": "Research effective strategies for climate change mitigation. Include information about renewable energy sources, carbon capture technologies, policy approaches, and individual actions. Discuss the potential impact of these strategies and their feasibility."
        },
        {
            "topic": "Artificial Intelligence Ethics",
            "description": "Research the ethical considerations surrounding artificial intelligence development and deployment. Include discussions about bias in AI, privacy concerns, job displacement, and the long-term implications of increasingly capable AI systems. Also discuss proposed frameworks for ethical AI."
        }
    ]
    
    # Save the research topics to a JSON file
    with open("research_topics.json", "w") as f:
        json.dump(research_topics, f, indent=4)
    
    return research_topics

def conduct_research(topic_index=0):
    """Conduct research on the specified topic."""
    # Load research topics
    research_topics = load_research_topics()
    
    # Check if the topic index is valid
    if topic_index < 0 or topic_index >= len(research_topics):
        print(f"Error: Topic index {topic_index} is out of range.")
        return
    
    # Get the selected topic
    topic = research_topics[topic_index]
    
    print(f"Conducting research on: {topic['topic']}")
    print(f"Description: {topic['description']}")
    print("=" * 80)
    
    # Set up the research agents
    assistant, user_proxy = setup_research_task()
    
    # Initiate a chat between the user proxy and the assistant
    user_proxy.initiate_chat(
        assistant,
        message=f"""Please research the following topic and provide a comprehensive summary:
        
        TOPIC: {topic['topic']}
        
        DETAILS: {topic['description']}
        
        Please structure your response as follows:
        1. Overview (a brief introduction to the topic)
        2. Key Points (the most important information about the topic)
        3. Current Status (where we stand today on this topic)
        4. Future Outlook (where this field is heading)
        5. Conclusion (summary of your findings)
        
        Make your response informative but concise, focusing on factual information.
        """
    )
    
    print("=" * 80)
    print("Research complete!")

if __name__ == "__main__":
    print("Starting AutoGen research assistant example...")
    
    # Conduct research on the first topic (index 0)
    conduct_research(0)
    
    print("Research assistant example completed.") 