---
title: AIAgentic-Framework
description: Workshop repository with five progressive Azure AI agent examples, local setup steps, and chapter-based documentation.
---

## Overview

This repository contains five progressive Azure AI agent examples. Each script builds on the previous one, starting from a basic conversational agent and ending with MCP integration.

## Project Structure

- `AgenticFramework/01BasicAgent.py`: basic chat agent
- `AgenticFramework/02AgentwithInstruction.py`: agent with instruction file and tuning parameters
- `AgenticFramework/03AgentwithKBVector.py`: agent with vector search (RAG)
- `AgenticFramework/04AgentwithTool.py`: agent with custom Python function tool
- `AgenticFramework/05AgentwithMCP.py`: agent with MCP server integration
- `AgenticFramework/add_data.py`: uploads files from `AgenticFramework/knowledgebase` and creates vector store
- `AgenticFramework/documentation/`: chapter-wise markdown guides

## Local Installation

These steps are based on project files in this repo:

- `pyproject.toml` requires Python `>=3.11`
- Existing `.venv` is Python `3.13.x`
- `uv.lock` is present, so `uv` is the recommended installer

### 1. Clone and Open the Project

```powershell
git clone <your-repo-url>
cd AIAgentic-Framework
```

### 2. Create and Activate Virtual Environment

If `.venv` already exists, you can reuse it. Otherwise create one:

```powershell
uv venv .venv --python 3.13
```

Activate it (Windows PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

Recommended (uses lock file):

```powershell
uv sync
```

Alternative with pip:

```powershell
python -m pip install -e .
```

### 4. Configure Environment Variables

Create or update `.env` in the repo root:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-foundry-resource>.services.ai.azure.com/projects/<your-project-name>
AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME=gpt-4.1
```

### 5. Authenticate to Azure

```powershell
az login --use-device-code
```

### 6. (For RAG/Tool/MCP Chapters) Build Vector Store

```powershell
python AgenticFramework/add_data.py
```

Copy the vector store ID from output and paste it into:

- `AgenticFramework/03AgentwithKBVector.py`
- `AgenticFramework/04AgentwithTool.py`
- `AgenticFramework/05AgentwithMCP.py`

## Run the Examples

Run each script independently:

```powershell
python AgenticFramework/01BasicAgent.py
python AgenticFramework/02AgentwithInstruction.py
python AgenticFramework/03AgentwithKBVector.py
python AgenticFramework/04AgentwithTool.py
python AgenticFramework/05AgentwithMCP.py
```

Type `exit` or `quit` in terminal to stop an active chat loop.

## Documentation Guides

Detailed chapter documentation is available under `AgenticFramework/documentation`.

1. [01BasicAgent.md](AgenticFramework/documentation/01BasicAgent.md)
   Build your first agent, configure `.env`, authenticate, and run a basic chat loop.
2. [02AgentwithInstruction.md](AgenticFramework/documentation/02AgentwithInstruction.md)
   Add system instructions from `instruction.txt`, and tune `temperature` and `top_p`.
3. [03AgentwithKBVector.md](AgenticFramework/documentation/03AgentwithKBVector.md)
   Add RAG with File Search, upload knowledge files, create vector store, and ground responses.
4. [04AgentwithTool.md](AgenticFramework/documentation/04AgentwithTool.md)
   Add custom function tools from `tools.py` and enable auto function calling.
5. [05AgentwithMCP.md](AgenticFramework/documentation/05AgentwithMCP.md)
   Connect to an MCP server, configure allowed tools, and handle MCP approvals.

## Notes

- `instruction.txt` is shared by multiple chapters and controls assistant behavior.
- `knowledgebase/` contains sample Contoso Pizza content used for File Search.
- Update placeholder values in script files (for example vector store ID and MCP server URL) before running advanced chapters.

## License

MIT
