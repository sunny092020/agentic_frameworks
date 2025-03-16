# LangChain with Docker Compose Example

This example demonstrates how to use LangChain with Docker Compose to create a simple API for interacting with language models.

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key

## Setup

1. Create a `.env` file in the root directory and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

2. Build and start the services:

```bash
docker-compose up --build
```

This will start a FastAPI application that uses LangChain to interact with OpenAI's models.

## API Endpoints

Once the service is running, you can access the following endpoints:

- `GET /`: Welcome message
- `POST /generate`: Generate a response using a LangChain LLMChain
- `POST /chat`: Generate a response using LangChain's chat model interface
- `POST /chat_with_memory`: Chat with memory to maintain conversation context
- `POST /document_qa`: Upload a document and ask questions about it (RAG pattern)
- `POST /agent`: Use LangChain's agent capabilities for complex tasks

## Example Requests

### Generate endpoint

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain what LangChain is in simple terms"}'
```

### Chat endpoint

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the main components of LangChain?"}'
```

### Chat with Memory endpoint

```bash
curl -X POST "http://localhost:8000/chat_with_memory" \
  -H "Content-Type: application/json" \
  -d '{"query": "My name is Alice", "session_id": "user123"}'

# Later in the conversation, referring to previous context:
curl -X POST "http://localhost:8000/chat_with_memory" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is my name?", "session_id": "user123"}'
```

### Document QA endpoint

```bash
# Upload a document and ask a question about it:
curl -X POST "http://localhost:8000/document_qa" \
  -F "file=@your_document.txt" \
  -F "query=What is the main topic of this document?"
```

### Agent endpoint

```bash
curl -X POST "http://localhost:8000/agent" \
  -H "Content-Type: application/json" \
  -d '{"query": "Calculate 25 * 437 and then search for information about the result"}'
```

## Project Structure

```
langchain/
  ├── docker-compose.yml   # Defines our service
  ├── Dockerfile           # Builds the Python environment
  ├── requirements.txt     # Python dependencies
  ├── app/
  │   └── main.py          # FastAPI application with LangChain examples
  └── README.md            # This file
```

## LangChain Features Demonstrated

1. **LLMChain with PromptTemplates**: Basic building block for chaining together prompts and LLMs
2. **ChatModels**: Using LangChain's chat interfaces with different message types
3. **Memory**: Maintaining context in conversations with `ConversationBufferMemory`
4. **Document Processing**: Loading and splitting documents for processing
5. **Embeddings and Vector Stores**: Using FAISS for storing and retrieving document embeddings
6. **Retrieval Augmented Generation (RAG)**: Answering questions based on your own documents
7. **Agents and Tools**: Using LangChain's agent framework for solving complex tasks
8. **Containerization**: Running LangChain apps in Docker containers

## Advanced Usage

You can extend this example by:

1. Adding more sophisticated memory types (e.g., ConversationSummaryMemory)
2. Implementing more document loaders (PDF, CSV, etc.)
3. Creating custom agents with specialized tools
4. Integrating with different vector databases (Pinecone, Chroma, etc.)
5. Adding streaming responses
6. Implementing caching mechanisms 