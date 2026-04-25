import os
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import MessageRole
from dotenv import load_dotenv

load_dotenv(override=True)

agents_client = AgentsClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential()
)

agent = agents_client.create_agent(
    model="gpt-4.1",
    name="my-agent",

)

print(f"Created agent, ID: {agent.id}")

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
            agent_id=agent.id
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
