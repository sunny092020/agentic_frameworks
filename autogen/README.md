# AutoGen Docker Compose Example

This example demonstrates how to use Microsoft's [AutoGen](https://github.com/microsoft/autogen) framework with Docker Compose for creating and orchestrating multiple AI agents.

## Overview

AutoGen is a framework that enables the development of LLM applications via multiple agents that can converse with each other to solve tasks. This example includes:

1. A multi-agent conversation demo
2. A code generation demo that can write and execute Python code

## Prerequisites

- Docker and Docker Compose installed
- An OpenAI API key

## Setup

1. Clone this repository
2. Copy the `.env.example` file to `.env`:
   ```
   cp .env.example .env
   ```
3. Edit the `.env` file to add your OpenAI API key
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

## Running the Examples

### Using Docker Compose

To run the multi-agent conversation example:

```bash
docker-compose up
```

This will build the Docker image and run the multi-agent conversation example.

### Running the Code Generation Example

To run the code generation example:

```bash
docker-compose run --rm autogen python /app/code_generation_example.py
```

## Project Structure

```
autogen/
├── app/
│   ├── multi_agent_conversation.py     # Main example with multiple agents
│   └── code_generation_example.py      # Example that generates and executes code
├── docker-compose.yml                  # Docker Compose configuration
├── Dockerfile                          # Docker image definition
├── requirements.txt                    # Python dependencies
└── .env.example                        # Template for environment variables
```

## Customizing the Examples

Feel free to modify the example scripts in the `app` directory. The Docker container mounts this directory as a volume, so changes will be reflected immediately without rebuilding the container.

### Modifying the Agent Prompts

You can modify the system messages for each agent in the Python scripts to customize their behavior.

### Enabling Docker Code Execution

In the code generation example, you can set `use_docker: True` in the `code_execution_config` to execute code within a Docker container for additional security (requires Docker-in-Docker configuration).

## Troubleshooting

- If you encounter errors related to the OpenAI API, ensure your API key is correctly set in the `.env` file.
- If you're having issues with Docker, ensure Docker and Docker Compose are properly installed and the Docker daemon is running.

## Resources

- [AutoGen GitHub Repository](https://github.com/microsoft/autogen)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [Docker Compose Documentation](https://docs.docker.com/compose/) 