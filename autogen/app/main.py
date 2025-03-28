from fastapi import FastAPI, Request, Form, Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import autogen
import subprocess
import sys
from typing import Optional

app = FastAPI(title="AutoGen Web UI")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Default model provider
DEFAULT_PROVIDER = "openai"

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/run_conversation", response_class=HTMLResponse)
async def run_conversation(request: Request, user_message: str = Form(...)):
    """Run a conversation with AutoGen agents based on user input"""
    # Here you would implement your AutoGen agent conversation
    # This is a placeholder that you can customize based on your needs
    
    # Example:
    # config_list = [{"model": "gpt-3.5-turbo", "api_key": os.getenv("OPENAI_API_KEY")}]
    # assistant = autogen.AssistantAgent("assistant", llm_config={"config_list": config_list})
    # user_proxy = autogen.UserProxyAgent("user_proxy")
    # user_proxy.initiate_chat(assistant, message=user_message)
    # conversation_history = user_proxy.chat_history
    
    # For now, just echo back the message
    conversation_history = [{"role": "user", "content": user_message}, 
                           {"role": "assistant", "content": f"Received: {user_message}"}]
    
    return templates.TemplateResponse(
        "conversation.html", 
        {"request": request, "conversation": conversation_history, "user_message": user_message}
    )

@app.get("/examples", response_class=HTMLResponse)
async def examples_page(request: Request, llm_provider: Optional[str] = Cookie(None)):
    """Render the examples page."""
    # Set default provider if not in cookie
    if not llm_provider:
        llm_provider = DEFAULT_PROVIDER
        
    examples = [
        {"name": "Code Generation Example", "script": "code_generation_example.py", "description": "Demonstrates code generation capabilities"},
        {"name": "Multi-Agent Conversation", "script": "multi_agent_conversation.py", "description": "Shows conversation between multiple agents"},
        {"name": "Research Assistant", "script": "research_assistant.py", "description": "Demonstrates research assistant functionality"},
        {"name": "Romantic Conversation", "script": "romantic_conversation.py", "description": "Example of agents engaging in romantic dialogue"},
        {"name": "Simple Flirt", "script": "simple_flirt.py", "description": "Demonstrates flirtatious conversation between agents"}
    ]
    return templates.TemplateResponse("examples.html", {
        "request": request, 
        "examples": examples,
        "current_provider": llm_provider
    })

@app.post("/set-provider")
async def set_provider(provider: str = Form(...)):
    """Set the LLM provider."""
    response = RedirectResponse(url="/examples", status_code=303)
    response.set_cookie(key="llm_provider", value=provider)
    return response

@app.post("/run-example")
async def run_example(script: str = Form(...), provider: str = Form(...)):
    """Run the selected example script."""
    # Get the absolute path to the script
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script)
    
    # Run the script as a subprocess with the provider as an environment variable
    print(f"\n\n=== Running {script} with provider: {provider} ===\n")
    env = os.environ.copy()
    env["LLM_PROVIDER"] = provider
    subprocess.Popen([sys.executable, script_path], env=env)
    
    # Redirect back to examples page
    return RedirectResponse(url="/examples", status_code=303)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 