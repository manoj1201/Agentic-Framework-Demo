import os
import time
from typing import Any
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import MessageRole, FilePurpose, FunctionTool, FileSearchTool, ToolSet
from azure.ai.agents.models import McpTool, ToolApproval, ThreadRun, RequiredMcpToolCall, RunHandler 
from tools import calculate_pizza_for_people
from dotenv import load_dotenv

load_dotenv(override=True)

# Creating the AgentsClient
agents_client = AgentsClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential()
)

# Create the file_search tool
vector_store_id = "vs______"
file_search = FileSearchTool(vector_store_ids=[vector_store_id])

# Create the function tool
function_tool = FunctionTool(functions={calculate_pizza_for_people})

# Add MCP tool so the agent can call Contoso Pizza microservices
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
mcp_tool.set_approval_mode("never")

# Creating the toolset
toolset = ToolSet()
toolset.add(file_search)
toolset.add(function_tool)
toolset.add(mcp_tool)

# Enable automatic function calling for this toolset so the agent can call functions directly
agents_client.enable_auto_function_calls(toolset)

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

# Creating the agent
agent = agents_client.create_agent(
    model="gpt-4.1",
    name="my-agent",
    instructions=open("instruction.txt").read(),
    top_p=0.7,
    temperature=0.7,
    toolset=toolset  # Add the toolset to the agent
)
print(f"Created agent, ID: {agent.id}")

# Creating the thread
thread = agents_client.threads.create()
print(f"Created thread, ID: {thread.id}")

try:
    while True:
        # Get the user input
        user_input = input("You: ")

        # Break out of the loop
        if user_input.lower() in ["exit", "quit"]:
            break

        # Add a message to the thread
        message = agents_client.messages.create(
            thread_id=thread.id,
            role=MessageRole.USER,
            content=user_input
        )

        # Process the agent run
        run = agents_client.runs.create_and_process(  
            thread_id=thread.id, 
            agent_id=agent.id,
            run_handler=MyRunHandler() ## Custom run handler
        )

        # List messages and print the first text response from the agent
        messages = agents_client.messages.list(thread_id=thread.id)
        first_message = next(iter(messages), None)
        if first_message:
            print(next((item["text"]["value"] for item in first_message.content if item.get("type") == "text"), "")) 

finally:
    # Clean up the agent when done
    agents_client.delete_agent(agent.id)
    print("Deleted agent")