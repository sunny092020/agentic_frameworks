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

1. Using LLMChain with PromptTemplates
2. Using ChatModels with SystemMessage and HumanMessage
3. Integration with OpenAI models
4. Containerization of a LangChain application 