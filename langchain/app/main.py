import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
import tempfile
from typing import List, Optional

# LangChain core imports
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import SystemMessage, HumanMessage
from langchain.chains import LLMChain, ConversationChain, RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentType, initialize_agent, Tool

# Imports from langchain-community
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()

# Check for OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    print("WARNING: OPENAI_API_KEY environment variable not set.")

app = FastAPI(title="LangChain API Example")

class QueryRequest(BaseModel):
    query: str

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = "default"

class QueryResponse(BaseModel):
    response: str

# Memory storage for conversations
conversation_memories = {}

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

@app.post("/chat_with_memory")
async def chat_with_memory(request: ChatRequest):
    """
    Chat endpoint with conversation memory to maintain context across interactions.
    """
    try:
        # Get or create memory for this session
        if request.session_id not in conversation_memories:
            conversation_memories[request.session_id] = ConversationBufferMemory()
        
        memory = conversation_memories[request.session_id]
        
        # Create the conversation chain with memory
        llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        conversation = ConversationChain(
            llm=llm, 
            memory=memory,
            verbose=True
        )
        
        # Get response
        response = conversation.predict(input=request.query)
        
        return {"response": response, "session_id": request.session_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat with memory: {str(e)}")

@app.post("/document_qa")
async def document_qa(file: UploadFile = File(...), query: Optional[str] = None):
    """
    Process a document and answer questions about it using RAG (Retrieval Augmented Generation).
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.file.read())
            temp_file_path = temp_file.name
        
        # Load the document
        loader = TextLoader(temp_file_path)
        documents = loader.load()
        
        # Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        
        # Create embeddings and store in vector database
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(chunks, embeddings)
        
        # Create a retrieval QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
            chain_type="stuff",
            retriever=vectorstore.as_retriever()
        )
        
        # Clean up the temp file
        os.unlink(temp_file_path)
        
        # If query is provided, answer it
        if query:
            answer = qa_chain.run(query)
            return {"response": answer}
        else:
            return {"message": "Document processed successfully. You can now ask questions about it using the /document_qa endpoint with a query parameter."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in document QA: {str(e)}")

@app.post("/agent")
async def run_agent(request: QueryRequest):
    """
    Use LangChain's agent capabilities to solve complex tasks.
    """
    try:
        # Initialize the LLM
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        
        # Define tools
        search_tool = Tool(
            name="Search",
            func=lambda x: "Search results for: " + x,
            description="Useful for searching information"
        )
        
        calculator_tool = Tool(
            name="Calculator",
            func=lambda x: eval(x),
            description="Useful for performing calculations"
        )
        
        # Initialize the agent with tools
        agent = initialize_agent(
            tools=[search_tool, calculator_tool],
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
        
        # Run the agent
        response = agent.run(request.query)
        
        return {"response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running agent: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 