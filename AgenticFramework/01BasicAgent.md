# Create Your First AI Agent

This guide walks you through building your first AI agent using the Foundry Agent Service. By the end, you’ll have a simple, interactive agent running locally.

---

## 1. Set Up Your Development Environment

1. **Open Visual Studio Code (VSCode).**
2. If VSCode doesn’t open the correct folder by default:
    - Go to **File** > **Open Folder**
    - Navigate to `C:\Agent` and select the folder
    - Click **Yes, I trust the authors** if prompted

---

## 2. Sign In to Azure

Before using the Azure Foundry Agent Service, sign in to your Azure subscription:

1. Open the terminal in VSCode (**Terminal** > **New Terminal**)
2. Run the following command:
    ```sh
    az login --use-device-code
    ```
3. Follow the on-screen instructions and use credentials with access to your Microsoft Foundry resource.
4. After signing in, select your default Azure subscription when prompted.

---

## 3. Create a `.env` File for Secrets

Store sensitive information like your project connection string in a `.env` file:

1. In your project’s root directory, create a file named `.env`.
2. Add the following line (replace with your actual values):
    ```env
    PROJECT_CONNECTION_STRING="https://<your-foundry-resource>.services.ai.azure.com/projects/<your-project-name>"
    ```
    - Ensure there are no spaces around the `=` sign.

### How to Find Your Connection String

1. Go to [https://ai.azure.com](https://ai.azure.com) and sign in.
2. Navigate to your project and select **Overview**.
3. The connection string appears under the **Microsoft Foundry project endpoint** section.

---
To confirm your model name, check the Model + endpoints section in the Azure portal.

Create a Conversation Thread

Threads store the conversation between you and the agent:

thread = project_client.agents.threads.create()

# Build Your First AI Agent

This guide will help you create your first AI agent using the Foundry Agent Service. By the end, you’ll have a working agent running locally that you can interact with in real time.

---

## 1. Set Up Your Development Environment

1. **Open Visual Studio Code (VSCode).**
2. If VSCode doesn’t open the correct folder by default:
    - Go to **File** > **Open Folder**
    - Navigate to `C:\Agent` and select the folder
    - Click **Yes, I trust the authors** if prompted

---

## 2. Sign In to Azure

Before using the Foundry Agent Service, sign in to your Azure subscription:

1. Open the terminal in VSCode (**Terminal** > **New Terminal**)
2. Run the following command:
    ```sh
    az login --use-device-code
    ```
3. Follow the on-screen instructions and use credentials with access to your Foundry resource.
4. After signing in, select your default Azure subscription when prompted.

---

## 3. Create a `.env` File for Secrets

Store sensitive information like your project connection string in a `.env` file:

1. In your project’s root directory, create a file named `.env`.
2. Add the following line (replace with your actual values):
    ```env
    PROJECT_CONNECTION_STRING="https://<your-foundry-resource>.services.ai.azure.com/projects/<your-project-name>"
    ```
    - Ensure there are no spaces around the `=` sign.

### How to Find Your Connection String

1. Go to [https://ai.azure.com](https://ai.azure.com) and sign in.
2. Navigate to your project and select **Overview**.
3. The connection string appears under the **Microsoft Foundry project endpoint** section.

---

## 4. Confirm Your Model Name

Check the **Model + endpoints** section in the Azure portal to confirm your model name.

---

## 5. Create and Interact with Your Agent

### Create a Conversation Thread

Threads store the conversation between you and the agent:

```python
thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")
```

### Send Messages to the Agent

Use a loop to continuously accept user input and send it to the agent:

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
        # Run the agent and generate a reply
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent.id
        )
        # Fetch messages and print the latest response
        messages = project_client.agents.messages.list(thread_id=thread.id)
        first_message = next(iter(messages), None)
        if first_message:
            print(next(
                (item["text"]["value"] for item in first_message.content if item.get("type") == "text"),
                ""
            ))
finally:
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
```

> [!IMPORTANT]
> Make sure the cleanup code is placed outside the loop so the agent isn’t deleted after the first message.

---

## 6. Run the Agent

Save your file, then execute:

```sh
python agent.py
```

You can now chat with your agent in the terminal.

Try prompts like:

- What is the tallest mountain in the world?
- What should I do in San Francisco?

Type `exit` or `quit` to end the session.

---

## Summary

In this chapter, you:

- Logged into Azure
- Retrieved your project connection string
- Stored secrets securely using a `.env` file
- Built a basic AI agent
- Interacted with it using a GPT-4o model
- Cleaned up resources by deleting the agent