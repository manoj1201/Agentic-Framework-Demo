
# Tool Calling – Making Your Agent Act

In the previous chapters, you gave your agent instructions and grounded it in your own data with File Search (RAG). Now, let's enable your agent to take actions by calling tools—small, well-defined functions your agent can invoke to perform tasks (e.g., calculations, lookups, API calls).

## What are Tools (Function Calling)?

Tools let your agent call your code with structured inputs. When a user asks for something that matches a tool's purpose, the agent will select that tool, pass validated arguments, and use the tool's result to craft a final answer.

## Why This Matters

- **Deterministic actions**: Offload precise work (math, lookup, API calls) to your code.
- **Safety & control**: You define what the agent is allowed to do.
- **Better UX**: The agent can provide concrete, actionable answers.

## Adding the Pizza Size Calculator Tool

We'll add a tool that, given a group size and an appetite level, recommends how many and what size pizzas to order.

### Step 1: Create `tools.py`

```python
def calculate_pizza_for_people(people_count: int, appetite_level: str = "normal") -> str:
    """
    Calculate the number and size of pizzas needed for a group of people.

    Args:
        people_count (int): Number of people who will be eating
        appetite_level (str): Appetite level - "light", "normal", or "heavy" (default: "normal")

    Returns:
        str: Recommendation for pizza size and quantity
    """
    print(f"[TOOL CALLED] Calculating pizza for {people_count} people with {appetite_level} appetite.")
    if people_count <= 0:
        return "Please provide a valid number of people (greater than 0)."

    appetite_multipliers = {"light": 0.7, "normal": 1.0, "heavy": 1.3}
    multiplier = appetite_multipliers.get(appetite_level.lower(), 1.0)
    adjusted_people = people_count * multiplier

    recommendations = []

    if adjusted_people <= 2:
        if adjusted_people <= 1:
            recommendations.append("1 Small pizza (perfect for 1-2 people)")
        else:
            recommendations.append("1 Medium pizza (great for 2-3 people)")
    elif adjusted_people <= 4:
        recommendations.append("1 Large pizza (serves 3-4 people)")
    elif adjusted_people <= 6:
        recommendations.append("1 Extra Large pizza (feeds 4-6 people)")
    elif adjusted_people <= 8:
        recommendations.append("2 Large pizzas (perfect for sharing)")
    elif adjusted_people <= 12:
        recommendations.append("2 Extra Large pizzas (great for groups)")
    else:
        extra_large_count = int(adjusted_people // 5)
        remainder = adjusted_people % 5

        pizza_list = []
        if extra_large_count > 0:
            pizza_list.append(f"{extra_large_count} Extra Large pizza{'s' if extra_large_count > 1 else ''}")

        if remainder > 2:
            pizza_list.append("1 Large pizza")
        elif remainder > 0:
            pizza_list.append("1 Medium pizza")

        recommendations.append(" + ".join(pizza_list))

    result = f"For {people_count} people with {appetite_level} appetite:\n"
    result += f"Recommendation: {recommendations[0]}\n"

    if appetite_level != "normal":
        result += f"(Adjusted for {appetite_level} appetite level)"

    return result
```

### Step 2: Import the Function in `agent.py`

Add the import alongside your other imports:

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import MessageRole, FilePurpose, FunctionTool, FileSearchTool, ToolSet
from tools import calculate_pizza_for_people
from dotenv import load_dotenv
```

### Step 3: Expose the Function as a Tool

Create a `FunctionTool` seeded with the Python function:

```python
# Create a FunctionTool for the calculate_pizza_for_people function
function_tool = FunctionTool(functions={calculate_pizza_for_people})
```

Add it to your toolset after File Search setup:

```python
# Create the file_search tool
vector_store_id = "<INSERT COPIED VECTOR STORE ID>"
file_search = FileSearchTool(vector_store_ids=[vector_store_id])

# Create the function tool
function_tool = FunctionTool(functions={calculate_pizza_for_people})

# Creating the toolset
toolset = ToolSet()
toolset.add(file_search)
toolset.add(function_tool)
```

### Step 4: Enable Automatic Function Calling

```python
toolset.add(function_tool)

# Enable automatic function calling for this toolset
project_client.agents.enable_auto_function_calls(toolset)
```

## Trying It Out

Run your agent and ask:

```
We are 7 people with heavy appetites. What pizzas should we order?
```

The agent should call `calculate_pizza_for_people` and reply with the recommendation.

## Tips & Best Practices

- **Schema first**: Define clear types, enums, and required fields.
- **Validate inputs**: Handle bad or missing data gracefully.
- **Single-purpose tools**: Keep tools small and focused.
- **Explainability**: Name and describe tools so the agent knows when to use them.

## Recap

You've now:
- Created a pizza calculator in `tools.py`
- Exposed it as a function tool
- Added it to your `ToolSet` (alongside File Search)
- Enabled automatic function calling
- Tested tool invocation with a prompt

## Complete Code Sample

See the final implementation in your project for the full `04AgentwithTool.py` with all tools integrated and ready to use.
