
# Integrating MCP (Model Context Protocol)

In earlier chapters, your agent learned to follow instructions, ground itself in your own data using File Search (RAG), and call custom tools.
In this final chapter, we'll connect your agent to a live MCP server - giving it access to external capabilities like live menus, toppings, and order management through a standard, secure protocol.

## What is MCP and why use it?

MCP (Model Context Protocol) is an open standard for connecting AI agents to external tools, data sources, and services through interoperable MCP servers.
Instead of integrating with individual APIs, you connect once to an MCP server and automatically gain access to all the tools that server exposes.

### Benefits of MCP

- 🧩 **Interoperability**: A universal way to expose tools from any service to any MCP-aware agent.
- 🔐 **Security & governance**: Centrally manage access and tool permissions.
- ⚙️ **Scalability**: Add or update server tools without changing your agent code.
- 🧠 **Simplicity**: Keep integrations and business logic in the server; keep your agent focused on reasoning.

## Install the Azure AI Agents SDK (with MCP support)

First, make sure you have the latest SDK version that supports MCP integration.

```bash
pip install "azure-ai-agents>=1.2.0b5"
```

Then, update your imports in `agent.py` to include MCP-related classes and utilities:

```python
from azure.ai.agents.models import McpTool, ToolApproval, ThreadRun, RequiredMcpToolCall, RunHandler
import time
from typing import Any
```

Your full import section should now look like this:

```python
import os
import time
from typing import Any
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import (
    MessageRole, FilePurpose, FunctionTool, FileSearchTool, ToolSet,
    McpTool, ToolApproval, ThreadRun, RequiredMcpToolCall, RunHandler
)
from tools import calculate_pizza_for_people
from dotenv import load_dotenv
```

## The Contoso Pizza MCP server

For Contoso Pizza, the MCP server exposes APIs for:

- 🧀 **Pizzas**: Available menu items and prices
- 🍅 **Toppings**: Categories, availability, and details
- 📦 **Orders**: Create, view, and cancel customer orders

You'll connect your agent to this server and grant it explicit permission to use a curated list of tools for these operations.

## Create and add the MCP tool

You'll define the MCP tool right before creating your ToolSet, alongside other tools (like File Search or the Pizza Calculator).

### Add the MCP tool

```python
# Add MCP tool so the agent can call Contoso Pizza microservices
```python
mcp_tool = McpTool(
    server_label="contoso_pizza",
    server_url="https://api.example.com/mcp/sse",
    allowed_tools=[
        "get_menu_items",
        "get_item_details",
        "get_categories",
        "get_item_by_category",
        "list_orders",
        "get_order_details",
        "create_order",
        "cancel_order",
    ],
)
```
mcp_tool.set_approval_mode("never")
```

Then, add it to the toolset:

```python
toolset.add(mcp_tool)
```

### Parameters explained

| Parameter | Description |
|-----------|-------------|
| `server_label` | A human-readable name for logs and debugging. |
| `server_url` | The MCP server endpoint. |
| `allowed_tools` | A whitelist of MCP tools your agent can call. |
| `approval_mode` | Defines whether calls require manual approval ("never" disables prompts). |

> In production, use more restrictive approval modes and scoped tool access.

## Handling tool approvals

When the agent calls an MCP tool, you can intercept and approve these calls dynamically.
This gives you visibility and fine-grained control over what's executed.

For this we will create a custom run handler:

```python
# Custom RunHandler to approve MCP tool calls
class MyRunHandler(RunHandler):
    def submit_mcp_tool_approval(
        self, *, run: ThreadRun, tool_call: RequiredMcpToolCall, **kwargs: Any
    ) -> ToolApproval:
        print(f"[RunHandler] Approving MCP tool call: {tool_call.id} for tool: {tool_call.name}")
        return ToolApproval(
            tool_call_id=tool_call.id,
            approve=True,
            headers=mcp_tool.headers,
        )
```

This is added after defining and enabling the toolset, but before creating the agent.

Then, pass the handler when running the agent:

```python
run = project_client.agents.runs.create_and_process(
    thread_id=thread.id,
    agent_id=agent.id,
    run_handler=MyRunHandler()  # Enables controlled MCP approvals
)
```


## Trying it out

Now it's time to test your connected agent!

Run the agent and try out these prompts:

```
Show me the available pizzas.
```

```
What is the price for a Hawaiian pizza?
```

```
Place an order for 2 large pepperoni pizzas.
```

The agent will automatically call the appropriate MCP tools, retrieve data from the live Contoso Pizza API, and respond conversationally - following your `instructions.txt` rules (e.g., tone, local currency, and time zone conversions).

## Best practices for MCP integration

- 🔒 **Principle of least privilege**: Only allow tools the agent truly needs.
- 📜 **Observability**: Log all tool calls for traceability and debugging.
- 🔁 **Resilience**: Handle connection errors gracefully and retry failed tool calls.
- 🧩 **Versioning**: Pin MCP server versions to prevent breaking changes.
- 👩‍💼 **Human-in-the-loop**: Use approval modes for sensitive actions (like order placement).

## Recap


- ✅ Learned what MCP is and why it matters for scalable agent design.
- ✅ Installed the updated Azure AI Agents SDK with MCP support.
- ✅ Connected your agent to the Contoso Pizza MCP Server.
- ✅ Implemented a custom run handler for tool approvals.
- ✅ Tested real-time integration with menu, toppings, and order tools.

