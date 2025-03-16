# LangChain Architecture

## Overview

LangChain is a framework designed for developing applications powered by language models. It provides a modular, composable architecture that simplifies building complex LLM-based applications by breaking them down into reusable components.

## Core Design Principles

LangChain's architecture is built on these foundational principles:

1. **Modularity**: Components are designed to be used independently or combined.
2. **Customizability**: Easy to extend and modify for specific use cases.
3. **Composability**: Building blocks that can be chained together to create complex workflows.
4. **Abstraction**: Hide implementation complexity behind simple interfaces.

## Package Structure

LangChain has recently been restructured into modular packages:

- **langchain-core**: Core abstractions, interfaces, and base classes
- **langchain-community**: Integrations with third-party tools and services
- **langchain**: High-level components that tie everything together
- **Specialized packages**:
  - langchain-openai: OpenAI-specific integrations
  - langchain-anthropic: Anthropic-specific integrations
  - langchain-text-splitters: Text chunking algorithms
  - and more

This modular approach allows developers to include only what they need.

## Key Components

### 1. Models

Models are the foundation of LangChain and include various types:

#### LLMs (Large Language Models)
Base text generation models that accept text input and provide text output.

```python
from langchain_openai import OpenAI

llm = OpenAI(model_name="gpt-3.5-turbo-instruct")
llm.invoke("What is the capital of France?")
```

#### Chat Models
Models specialized for conversational applications with formatted inputs/outputs.

```python
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

chat = ChatOpenAI(model_name="gpt-3.5-turbo")
chat.invoke([
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is the capital of France?")
])
```

#### Text Embedding Models
Models that convert text into vector representations.

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
text_embedding = embeddings.embed_query("Hello world")
```

### 2. Prompts

Prompts handle the formatting of inputs to language models:

#### PromptTemplates
Create templates with variables that can be filled in.

```python
from langchain.prompts import PromptTemplate

template = PromptTemplate(
    input_variables=["product"],
    template="Write a description for {product}:"
)
formatted_prompt = template.format(product="iPhone")
```

#### Few-Shot Learning
Templates that include examples to guide the model's responses.

```python
from langchain.prompts import FewShotPromptTemplate, PromptTemplate

examples = [
    {"word": "happy", "antonym": "sad"},
    {"word": "tall", "antonym": "short"},
]

example_formatter = PromptTemplate(
    input_variables=["word", "antonym"],
    template="Word: {word}\nAntonym: {antonym}"
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_formatter,
    prefix="Give the antonym of each word:",
    suffix="Word: {input_word}\nAntonym:",
    input_variables=["input_word"]
)
```

#### Output Parsers
Convert model outputs into structured formats.

```python
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class Person(BaseModel):
    name: str = Field(description="Person's name")
    age: int = Field(description="Person's age")

parser = PydanticOutputParser(pydantic_object=Person)
```

### 3. Memory

Memory systems store and retrieve information from past interactions:

#### ConversationBufferMemory
Stores all messages in a conversation.

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
memory.chat_memory.add_user_message("Hello, how are you?")
memory.chat_memory.add_ai_message("I'm doing well, thank you!")
```

#### ConversationSummaryMemory
Maintains a summary of the conversation to manage context length.

```python
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI

memory = ConversationSummaryMemory(llm=ChatOpenAI())
```

#### Vector-based Memory
Uses embeddings to find relevant information from past exchanges.

```python
from langchain.memory import VectorStoreRetrieverMemory
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_texts(["Memory is the key to learning"], embedding=embeddings)
retriever = vectorstore.as_retriever()
memory = VectorStoreRetrieverMemory(retriever=retriever)
```

### 4. Chains

Chains combine multiple components to create complex workflows:

#### LLMChain
Connect prompts to models.

```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-3.5-turbo")
prompt = PromptTemplate(
    input_variables=["product"],
    template="Write a description for {product}:"
)
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(product="iPhone")
```

#### SequentialChain
Run multiple chains in sequence.

```python
from langchain.chains import SequentialChain, LLMChain

first_chain = LLMChain(llm=llm, prompt=first_prompt, output_key="first_output")
second_chain = LLMChain(llm=llm, prompt=second_prompt, output_key="second_output")

overall_chain = SequentialChain(
    chains=[first_chain, second_chain],
    input_variables=["input"],
    output_variables=["first_output", "second_output"]
)
```

#### RouterChain
Conditionally route to different chains.

```python
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain

router_chain = LLMRouterChain.from_llm(llm, prompt=router_prompt)
destination_chains = {"math": math_chain, "history": history_chain}
chain = MultiPromptChain(router_chain=router_chain, destination_chains=destination_chains)
```

### 5. Retrievers and Vector Stores

For retrieval-augmented generation (RAG):

#### Vector Stores
Store vector embeddings for efficient similarity search.

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
texts = ["LangChain is a framework for LLM applications", "Vector databases store embeddings"]
vectorstore = FAISS.from_texts(texts, embeddings)
```

#### Retrievers
Query vector stores to find relevant information.

```python
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
documents = retriever.get_relevant_documents("What is LangChain?")
```

### 6. Document Loaders

Document Loaders ingest content from various sources:

```python
from langchain_community.document_loaders import TextLoader, PyPDFLoader, WebBaseLoader

# Load from text file
text_loader = TextLoader("data.txt")
text_docs = text_loader.load()

# Load from PDF
pdf_loader = PyPDFLoader("document.pdf")
pdf_docs = pdf_loader.load()

# Load from web
web_loader = WebBaseLoader("https://example.com")
web_docs = web_loader.load()
```

### 7. Text Splitters

Text Splitters break documents into manageable chunks:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200
)
splits = text_splitter.split_documents(documents)
```

### 8. Tools and Agents

Tools are functions that agents can use:

```python
from langchain.tools import Tool

search_tool = Tool(
    name="Search",
    func=lambda x: "Search results for: " + x,
    description="Useful for finding information on the internet"
)
```

Agents use language models to decide which tools to use:

```python
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-3.5-turbo")
tools = [search_tool]
agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

agent.run("What is the weather in New York?")
```

## Common Architecture Patterns

### 1. RAG (Retrieval Augmented Generation)

One of the most common patterns in LangChain applications:

```python
# 1. Data ingestion pipeline
loader = TextLoader("document.txt")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter()
chunks = text_splitter.split_documents(documents)
vectorstore = FAISS.from_documents(chunks, embeddings)

# 2. RAG chain
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(),
    retriever=vectorstore.as_retriever(),
    chain_type="stuff"  # Other options: "map_reduce", "refine"
)

# 3. Query
result = qa_chain.run("What does the document say about AI?")
```

### 2. Conversation with Memory

Creating stateful conversations:

```python
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

conversation = ConversationChain(
    llm=ChatOpenAI(),
    memory=ConversationBufferMemory(),
    verbose=True
)

response1 = conversation.predict(input="My name is Bob")
response2 = conversation.predict(input="What's my name?")  # Should remember "Bob"
```

### 3. Agentic Workflows

Enabling autonomous decision-making:

```python
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_openai import ChatOpenAI

# Define tools
tools = [
    Tool(name="Search", func=search_function, description="Search the web"),
    Tool(name="Calculator", func=lambda x: eval(x), description="Perform calculations")
]

# Create agent
agent = initialize_agent(
    tools, 
    ChatOpenAI(temperature=0), 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Run agent
result = agent.run("Calculate 15% of $39.99 and then find information about sales tax.")
```

## Advanced Architectural Concepts

### 1. Callbacks and Event System

LangChain provides a callback system for monitoring and logging:

```python
from langchain.callbacks import StdOutCallbackHandler
from langchain.chains import LLMChain

handler = StdOutCallbackHandler()
chain = LLMChain(llm=llm, prompt=prompt, callbacks=[handler], verbose=True)
```

### 2. Custom Components

LangChain's architecture allows for easy customization:

```python
from langchain.chains.base import Chain
from typing import Dict, List, Any

class MyCustomChain(Chain):
    @property
    def input_keys(self) -> List[str]:
        return ["input"]
    
    @property
    def output_keys(self) -> List[str]:
        return ["output"]
    
    def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # Custom logic here
        return {"output": processed_result}
```

### 3. Streaming Responses

Many components support streaming for responsive UIs:

```python
from langchain_openai import ChatOpenAI

chat = ChatOpenAI(streaming=True)
for chunk in chat.stream("Write a poem about AI"):
    print(chunk.content, end="", flush=True)
```

## Execution Flow

A typical LangChain application flows through these stages:

1. **Input Processing**: Parse and prepare user input
2. **Context Gathering**: Retrieve relevant information (documents, memory)
3. **Prompt Construction**: Format input and context into prompts
4. **Model Invocation**: Send prompts to language models
5. **Output Processing**: Parse and format model outputs
6. **Action Execution**: Perform actions based on outputs (for agents)
7. **Response Generation**: Formulate the final response

## Integration Architecture

LangChain provides integrations with:

1. **Model Providers**: OpenAI, Anthropic, HuggingFace, etc.
2. **Vector Databases**: FAISS, Pinecone, Chroma, Weaviate, etc.
3. **Traditional Databases**: PostgreSQL, MongoDB, Redis, etc.
4. **API Services**: SerpAPI, Zapier, etc.
5. **Development Frameworks**: FastAPI, Flask, Streamlit, etc.

## Conclusion

LangChain's architecture offers a flexible, modular approach to building LLM-powered applications. By understanding its components and patterns, developers can efficiently create sophisticated AI applications that leverage the power of language models while maintaining clean, maintainable code.

The framework continues to evolve rapidly, with new components and patterns emerging as the field of LLM application development matures. This architecture enables developers to adapt to these changes while building on solid foundations.
