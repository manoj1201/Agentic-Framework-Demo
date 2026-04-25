# Create Your First Agent

In this chapter, you'll learn how to build your first AI agent using the Foundry Agent Service.  
By the end, you'll have a simple agent running locally that you can interact with in real time.

---

## 🧰 Open Your Development Environment

Open **VS Code**. By default, it should open the directory `C:\agent`.  
If not, follow these steps:

### Open your project folder

1. Open VS Code  
2. Click **File**  
3. Select **Open Folder**  
4. Navigate to `This Computer > Local Disk (C:) > Agent`  
5. Click **Select Folder**  
6. Choose **Yes, I trust the authors**

---

## 🔐 Sign in to Azure

Before using the Foundry Agent Service, sign in to your Azure account.

### Open the terminal (if not visible)

- Click **Terminal** in the top menu  
- Select **New Terminal**

### Run the login command

```bash
az login --use-device-code
```

> **Note:** After signing in, press Enter to select the default Azure subscription.

---

## ⚙️ Create a .env File

Store sensitive data securely in an environment file.

### Steps

1. Create a file named `.env` in your project root
2. Add the following:

```env
PROJECT_CONNECTION_STRING="https://<your-foundry-resource>.services.ai.azure.com/projects/<your-project-name>"
```

Replace the placeholder with your actual Foundry project values.

### Find your connection string

1. Go to https://ai.azure.com
2. Sign in
3. Open your project
4. Navigate to **Overview**
5. Copy the connection string from the **Project Endpoint**

> ⚠️ **Ensure there are no spaces around the `=` sign.**

---

## 🤖 Create a Basic Agent

Open `agent.py` and start building your agent.

### Add imports

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import MessageRole, FilePurpose, FunctionTool, FileSearchTool, ToolSet
from dotenv import load_dotenv
```

### Load Environment Variables

```python
load_dotenv(override=True)
```

### Create Project Client

```python
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_CONNECTION_STRING"],
    credential=DefaultAzureCredential()
)
```

### Create the Agent

```python
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="my-agent"
)
print(f"Created agent, ID: {agent.id}")
```

> **Tip:** To find your model name, go to **Model + endpoints** in Azure.

### Create a Conversation Thread

```python
thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")
```

### Send Messages

```python
try:
    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role=MessageRole.USER,
            content=user_input
        )
```

### Process Agent Response

```python
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent.id
        )
```

### Retrieve and Display Response

```python
        messages = project_client.agents.messages.list(thread_id=thread.id)
        first_message = next(iter(messages), None)

        if first_message:
            print(next(
                (item["text"]["value"] for item in first_message.content if item.get("type") == "text"),
                ""
            ))
```

### Clean Up

```python
finally:
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
```

> ⚠️ **Place this block outside the loop to avoid deleting the agent too early.**

---

## ▶️ Run the Agent

Save your file, then run:

```bash
python agent.py
```

### Example prompts

- What is the tallest mountain in the world?
- What do you recommend I do in San Francisco?

Type `exit` or `quit` to end the session.

---

## 📌 Recap

In this chapter, you:

- Logged into Azure
- Retrieved your connection string
- Stored secrets using `.env`
- Created a basic AI agent
- Interacted with a GPT-4o model
- Cleaned up resources