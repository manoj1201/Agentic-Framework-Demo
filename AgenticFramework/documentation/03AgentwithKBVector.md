
# Enhance Your Agent with File Search (RAG)

This guide shows how to ground your agent in your own data using Retrieval-Augmented Generation (RAG) and the File Search tool in Microsoft Foundry. You'll upload documents, create a vector store, and connect it to your agent for smarter, data-driven answers.

---

## Why Add Knowledge?

By default, AI models only know what they were trained on. They don’t have access to your private or domain-specific data. **Retrieval-Augmented Generation (RAG)** lets your agent fetch relevant information from your own data before generating responses, improving accuracy and grounding answers in real information.

---

## Scenario

Suppose you have a `./documents` folder with information about Contoso Pizza (store locations, hours, menus). You want your agent to answer questions using this data.

You will:
1. Upload these files
2. Create a vector store
3. Connect it to your agent

---

## Step 1: Create a Vector Store Script

Create a new file called `add_data.py`:

```python
import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import FilePurpose

load_dotenv(override=True)

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_CONNECTION_STRING"],
    credential=DefaultAzureCredential()
)

DOCS_DIR = "./documents"
if not os.path.isdir(DOCS_DIR):
    raise FileNotFoundError("Create ./documents and add your files.")

print(f"Uploading files from {DOCS_DIR} ...")
file_ids = []
for fname in os.listdir(DOCS_DIR):
    fpath = os.path.join(DOCS_DIR, fname)
    if not os.path.isfile(fpath) or fname.startswith('.'):
        continue
    uploaded = project_client.agents.files.upload_and_poll(
        file_path=fpath,
        purpose=FilePurpose.AGENTS
    )
    file_ids.append(uploaded.id)

print(f"Uploaded {len(file_ids)} files.")
if not file_ids:
    raise RuntimeError("No files uploaded.")

vector_store = project_client.agents.vector_stores.create_and_poll(
    data_sources=[],
    name="contoso-pizza-store-information"
)
print(f"Vector store ID: {vector_store.id}")

batch = project_client.agents.vector_store_file_batches.create_and_poll(
    vector_store_id=vector_store.id,
    file_ids=file_ids
)
print(f"Batch ID: {batch.id}")
```

Run the script:

```sh
python add_data.py
```

Example output:

```
Uploading files from ./documents ...
Uploaded 10 files.
Vector store ID: vs_xxx
Batch ID: vsfb_xxx
```

Save the vector store ID for the next step.

---

## Step 2: Add File Search to Your Agent

In your `agent.py`:

```python
from azure.ai.agents.models import FileSearchTool, ToolSet

vector_store_id = "<YOUR_VECTOR_STORE_ID>"
file_search = FileSearchTool(vector_store_ids=[vector_store_id])
toolset = ToolSet()
toolset.add(file_search)

agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="pizza-bot",
    instructions=open("instructions.txt").read(),
    temperature=0.7,
    top_p=0.7,
    toolset=toolset
)
print(f"Created agent: {agent.id}")
```

---

## Step 3: Run the Agent

```sh
python agent.py
```

Try asking:

- Which stores are open after 8pm?
- Where is the nearest Contoso Pizza store?

Type `exit` or `quit` to stop.

---

## Recap

- Used RAG to enhance your agent
- Uploaded documents
- Created a vector store
- Indexed your data
- Connected File Search to your agent