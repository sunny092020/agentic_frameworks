from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import autogen

app = FastAPI(title="AutoGen Web UI")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 