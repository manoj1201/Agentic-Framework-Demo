import os
from dotenv import load_dotenv

# Azure SDK imports
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import FilePurpose

# Load environment variables (expects PROJECT_CONNECTION_STRING in .env)
load_dotenv(override=True)

agents_client = AgentsClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential()
)


DOCS_DIR = "./knowledgebase"

if not os.path.isdir(DOCS_DIR):
    raise FileNotFoundError(
        f"knowledgebase folder not found at {DOCS_DIR}. "
        "Create it and add your Contoso Pizza files (PDF, TXT, MD, etc.)."
    )

print(f"Uploading files from {DOCS_DIR} ...")
file_ids = []
for fname in os.listdir(DOCS_DIR):
    fpath = os.path.join(DOCS_DIR, fname)
    # skip directories and hidden files like .DS_Store
    if not os.path.isfile(fpath) or fname.startswith('.'):
        continue
    uploaded = agents_client.files.upload_and_poll(
        file_path=fpath,
        purpose=FilePurpose.AGENTS
    )
    file_ids.append(uploaded.id)

print(f"Uploaded {len(file_ids)} files.")
if not file_ids:
    raise RuntimeError("No files uploaded. Put files in ./knowledgebase and re-run.")


vector_store = agents_client.vector_stores.create_and_poll(
    data_sources=[],
    name="contoso-pizza-store-information"
)
print(f"Created vector store, ID: {vector_store.id}")

batch = agents_client.vector_store_file_batches.create_and_poll(
    vector_store_id=vector_store.id,
    file_ids=file_ids
)
print(f"Created vector store file batch, ID: {batch.id}")