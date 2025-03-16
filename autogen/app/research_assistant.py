import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from autogen.agentchat.assistant_agent import AssistantAgent
from autogen.agentchat.user_proxy_agent import UserProxyAgent

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment
openai_api_key = os.environ.get("OPENAI_API_KEY")
news_api_key = os.environ.get("NEWS_API_KEY", "your_news_api_key")  # You'll need to add this to your .env

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Configure LLM
config_list = [
    {
        "model": "gpt-4",
        "api_key": openai_api_key,
    }
]

# Define tool functions that the agent can use
def search_news(query, days=7):
    """
    Search for news articles related to the query from the past few days.
    
    Args:
        query (str): The search query
        days (int): How many days back to search
        
    Returns:
        dict: JSON response with news articles
    """
    try:
        url = "https://newsapi.org/v2/everything"
        
        # Calculate date from days ago
        from_date = (datetime.now() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
        
        params = {
            'q': query,
            'from': from_date,
            'sortBy': 'relevancy',
            'apiKey': news_api_key,
            'language': 'en',
            'pageSize': 5  # Limit to 5 articles
        }
        
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        return {"error": str(e), "source": "news_api"}

def weather_forecast(location):
    """
    Get the weather forecast for a location (simulated).
    
    Args:
        location (str): The location to get the weather for
        
    Returns:
        dict: Weather information
    """
    # This is a mock function - in a real app, you would call a weather API
    forecasts = {
        "new york": {"condition": "Partly Cloudy", "temp_c": 22, "temp_f": 72, "humidity": 65},
        "london": {"condition": "Rainy", "temp_c": 18, "temp_f": 64, "humidity": 80},
        "tokyo": {"condition": "Sunny", "temp_c": 26, "temp_f": 79, "humidity": 70},
        "sydney": {"condition": "Clear", "temp_c": 24, "temp_f": 75, "humidity": 60},
    }
    
    location_lower = location.lower()
    if location_lower in forecasts:
        return {"location": location, "forecast": forecasts[location_lower]}
    else:
        return {"location": location, "forecast": {"condition": "Sunny", "temp_c": 25, "temp_f": 77, "humidity": 50}}

def generate_report_template(title, sections):
    """
    Generate a report template with the given title and sections.
    
    Args:
        title (str): Report title
        sections (list): List of section names
        
    Returns:
        str: Report template
    """
    template = f"# {title}\n\n"
    template += f"*Generated on {datetime.now().strftime('%Y-%m-%d')}*\n\n"
    
    for i, section in enumerate(sections, 1):
        template += f"## {i}. {section}\n\n"
        template += "[Content for this section will be filled in]\n\n"
    
    return template

# Create an assistant agent with function calling capabilities
assistant = AssistantAgent(
    name="ResearchAssistant",
    llm_config={
        "config_list": config_list,
        "temperature": 0.5,
        "functions": [
            {
                "name": "search_news",
                "description": "Search for recent news articles on a specific topic",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query"
                        },
                        "days": {
                            "type": "integer",
                            "description": "Number of days back to search"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "weather_forecast",
                "description": "Get the weather forecast for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The location to get the weather for"
                        }
                    },
                    "required": ["location"]
                }
            },
            {
                "name": "generate_report_template",
                "description": "Generate a template for a report with sections",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Title of the report"
                        },
                        "sections": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of section titles"
                        }
                    },
                    "required": ["title", "sections"]
                }
            }
        ]
    },
    system_message="""You are a research assistant with access to tools for searching news, 
    checking weather, and creating report templates. Use these tools to help the user 
    gather information and organize it effectively. Always think about which tool would 
    be most appropriate for the user's request. When providing information, be concise and 
    well-organized. If you search for news, summarize the key points rather than listing 
    all articles. Make recommendations based on the information you find."""
)

# Create a user proxy agent that can execute functions
user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",
    function_map={
        "search_news": search_news,
        "weather_forecast": weather_forecast,
        "generate_report_template": generate_report_template
    }
)

if __name__ == "__main__":
    print("Starting the Research Assistant with Tool Use capabilities...")
    print("This assistant can search for news, check weather, and create report templates.")
    print("Try asking things like:")
    print("- 'Find me news about renewable energy'")
    print("- 'What's the weather in Tokyo?'")
    print("- 'Create a report template about climate change'")
    print("- 'Research the impact of AI on healthcare and create a report'\n")
    
    # Start the conversation
    user_proxy.initiate_chat(
        assistant,
        message="Hi, I'd like your help researching current trends in sustainable transportation. Can you find some recent news and help me organize the information?"
    ) 