# AutoGen Docker Compose Example

This example demonstrates how to use Microsoft's [AutoGen](https://github.com/microsoft/autogen) framework with Docker Compose for creating and orchestrating multiple AI agents.

## Overview

AutoGen is a framework that enables the development of LLM applications via multiple agents that can converse with each other to solve tasks. This example includes:

1. A multi-agent conversation demo for data analysis
2. A code generation demo that can write and execute Python code
3. A travel planning assistant that demonstrates non-coding use cases
4. A romantic conversation simulation between two characters
5. A simple flirtation example with just two characters interacting directly (with Vietnamese translations)

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
   OPENAI_API_KEY=sk-your_actual_api_key_here
   ```
   
   > **Important**: The OpenAI API key must start with `sk-` followed by the rest of your key. Using an incorrect format will result in a warning and the examples won't work properly.

## Running the Examples

### Data Analysis Example

To run the multi-agent conversation example for data analysis:

```bash
docker-compose up autogen
```

This will build the Docker image and run the multi-agent conversation example.

### Code Generation Example

To run the code generation example:

```bash
docker-compose run --rm autogen python /app/code_generation_example.py
```

### Travel Planning Assistant

To run the travel planning assistant example (which demonstrates a non-coding use case):

```bash
docker-compose up travel-planner
```

This example allows you to interact with a group of agents that help plan a vacation, including a travel coordinator, destination expert, budget advisor, and local cuisine expert.

### Romantic Conversation Simulation

To run the romantic conversation example between two characters:

```bash
docker-compose up romantic-chat
```

This example simulates a flirtatious conversation between two characters (Emma and James) who just met at a literary event. It demonstrates how AutoGen can be used for creative content generation and character roleplay. The conversation is guided by a moderator agent, and you can observe or participate as desired.

### Simple Flirtation Example with Vietnamese Translations

For a direct flirtatious conversation between two characters with Vietnamese translations:

```bash
docker-compose up simple-flirt
```

This stripped-down example shows Sophia and Alex flirting at a rooftop bar, with the conversation flowing naturally between just the two of them. Each message is followed by its Vietnamese translation, demonstrating AutoGen's multilingual capabilities and potential for language learning applications.

## Project Structure

```
autogen/
├── app/
│   ├── multi_agent_conversation.py     # Data analysis example with multiple agents
│   ├── code_generation_example.py      # Example that generates and executes code
│   ├── travel_planning_assistant.py    # Non-coding example for travel planning
│   ├── romantic_conversation.py        # Simulated conversation with moderator/observer
│   └── simple_flirt.py                 # Direct conversation with Vietnamese translations
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

- If you encounter errors related to the OpenAI API, ensure your API key is correctly set in the `.env` file and includes the `sk-` prefix.
- If you're seeing warnings about `flaml.automl`, make sure your requirements.txt includes `flaml[automl]` and rebuild the Docker image.
- If you're having issues with Docker, ensure Docker and Docker Compose are properly installed and the Docker daemon is running.

## Resources

- [AutoGen GitHub Repository](https://github.com/microsoft/autogen)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## Web UI

This project includes a web-based user interface built with FastAPI that allows you to interact with AutoGen agents through your browser.

### Features

- Simple, intuitive web interface
- Submit messages to AutoGen agents
- View conversation history
- Continue conversations with follow-up messages

### Usage

1. Start the application using Docker:
   ```
   docker-compose up
   ```

2. Open your browser and navigate to [http://localhost:8000](http://localhost:8000)

3. Type your message in the form and click "Submit" to start a conversation with the AutoGen agents

4. View the responses and continue the conversation as needed

### Customization

You can customize the AutoGen agent configuration in `app/main.py`. The web UI is built with FastAPI, Jinja2 templates, and CSS. You can modify the templates in the `app/templates` directory and the styles in `app/static/css/styles.css`. 