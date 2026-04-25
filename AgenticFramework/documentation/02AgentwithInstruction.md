
# Adding Agent Instructions

## Overview

In the previous chapter, you created your first basic agent and started a conversation with it. Now, we'll take things a step further by learning about system prompts and why they're essential for shaping your agent's behavior.

## What is a System Prompt?

A system prompt is a set of instructions you provide to the model when creating an agent. Think of it as the personality and rulebook for your agent: it defines how the agent should respond, what tone it should use, and what limitations it should follow.

Without a system prompt, your agent may respond in a generic way. By adding clear instructions, you can tailor it to your needs.

### Benefits of System Prompts

- Ensure the agent stays consistent across conversations
- Guide the agent's tone and role (e.g., friendly teacher, strict code reviewer, technical support bot)
- Reduce the risk of irrelevant or off-topic answers
- Encode rules the agent must follow (e.g., "always answer in JSON")

## Adding Instructions to Your Agent

When creating an agent, you can pass the `instructions` parameter:

```python
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="my-agent",
    instructions="You are a helpful support assistant for Microsoft Foundry. Always provide concise, step-by-step answers."
)
print(f"Created agent with system prompt, ID: {agent.id}")
```

Every time the agent processes a conversation, it will follow your system instructions.

## Using an External Instructions File

Instead of hardcoding instructions, store them in a separate file for easier maintenance.

Create `instructions.txt`:

```
You are Contoso PizzaBot, an AI assistant that helps users order pizza.

Your primary role is to assist users in ordering pizza, checking menus, and tracking order status.

### Guidelines
1. Be friendly, helpful, and concise
2. Gather all necessary information for orders (type, options)
3. Default to San Francisco store if location not specified
4. Convert USD prices to appropriate currency for store location
5. Convert UTC pickup times to appropriate time zone
6. List at most 5 menu entries at a time
7. Help check order status using order ID
8. Always confirm orders before placing them
9. Focus only on pizza-related topics
10. Request UserId and Name at the start if not provided

### Tools & Data Access
- Use the **Contoso Pizza Store Information Vector Store** via file_search tool
- Only return information found in the vector store
- Ask for clarification if information is ambiguous

### Response Format
- Use natural, conversational language
- Plain text only—no emoticons, markup, markdown, or HTML
```

## Updating Your Agent Code

Replace the agent creation code with:

```python
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="pizza-bot",
    instructions=open("instructions.txt").read(),
    top_p=0.7,
    temperature=0.7,
)
print(f"Created agent with system prompt, ID: {agent.id}")
```

The `top_p` and `temperature` parameters control creativity and randomness in responses.

## Running Your Agent

```bash
python agent.py
```

Experiment by modifying `instructions.txt` and running the agent again—you'll see how instructions directly influence agent behavior. Enter `exit` or `quit` to stop.

## Recap

In this chapter, you learned how to:
- Understand what system prompts are and why they matter
- Add instructions directly to your agent during creation
- Store instructions in external files for better maintainability
- Use parameters like `top_p` and `temperature` to fine-tune agent behavior
- Test your agent and observe how instructions shape its responses

With these skills, you can now create agents tailored to specific use cases and maintain consistent behavior across conversations.

## Complete Code Sample

See the final implementation in your project for the full `02AgentwithInstruction.py` with all tools integrated and ready to use.