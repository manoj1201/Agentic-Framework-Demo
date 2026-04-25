# AIAgentic-Framework

This repository demonstrates a progression of agent-based projects using Azure AI Agents, each building on the previous with increasing capabilities. Below is an overview of each project:

## Projects Overview

### 1. 01BasicAgent.py
- **Description:**
  - A minimal agent setup using Azure AI Agents.
  - Demonstrates agent creation and basic message loop.
- **Key Features:**
  - Simple agent instantiation
  - User input loop

### 2. 02AgentwithInstruction.py
- **Description:**
  - Extends the basic agent by adding custom instructions and model parameters.
- **Key Features:**
  - Loads instructions from a file
  - Configures model parameters (e.g., `top_p`, `temperature`)

### 3. 03AgentwithKBVector.py
- **Description:**
  - Adds knowledge base (vector search) capability to the agent.
- **Key Features:**
  - Integrates a vector store for file search
  - Demonstrates toolset usage

### 4. 04AgentwithTool.py
- **Description:**
  - Introduces function tools, allowing the agent to call Python functions.
- **Key Features:**
  - Adds a custom function tool (e.g., pizza calculation)
  - Combines file search and function tools
  - Enables automatic function calling

### 5. 05AgentwithMCP.py
- **Description:**
  - Integrates MCP (Microservices Control Plane) tools for advanced agent capabilities.
- **Key Features:**
  - Adds MCP tool for microservice interaction
  - Supports multiple tool types (file search, function, MCP)
  - Demonstrates advanced agent orchestration

## Usage

Each project can be run independently. Ensure you have the required environment variables and dependencies set up (see below).

### Prerequisites
- Python 3.8+
- Azure AI Agents SDK
- `dotenv` for environment variable management
- Properly configured Azure resources (endpoint, credentials, vector store, etc.)

### Running a Project
```bash
python AgenticFramework/01BasicAgent.py
# or
python AgenticFramework/02AgentwithInstruction.py
# ...and so on
```

## License
MIT
