import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.schema import SystemMessage, HumanMessage

# Load environment variables
load_dotenv()

# Check for OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    print("WARNING: OPENAI_API_KEY environment variable not set.")

app = FastAPI(title="LangChain API Example")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

@app.get("/")
async def root():
    return {"message": "Welcome to LangChain API Example"}

@app.post("/generate", response_model=QueryResponse)
async def generate_response(request: QueryRequest):
    try:
        # Initialize the LLM
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7
        )
        
        # Create a prompt template
        prompt_template = PromptTemplate(
            input_variables=["query"],
            template="You are a helpful assistant. Answer the following query: {query}"
        )
        
        # Create a chain
        chain = LLMChain(
            llm=llm,
            prompt=prompt_template
        )
        
        # Run the chain
        response = chain.run(query=request.query)
        
        return QueryResponse(response=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/chat")
async def chat(request: QueryRequest):
    try:
        # Initialize the Chat Model
        chat_model = ChatOpenAI(model_name="gpt-3.5-turbo")
        
        # Create messages
        messages = [
            SystemMessage(content="You are a helpful assistant that provides concise answers."),
            HumanMessage(content=request.query)
        ]
        
        # Get response
        response = chat_model.invoke(messages)
        
        return {"response": response.content}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 