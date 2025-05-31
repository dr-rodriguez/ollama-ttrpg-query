# Construct a vector database with document embeddings
# Following setup in https://docs.trychroma.com/docs/overview/getting-started

import chromadb
import ollama
from read_file import prepare_documents, FILENAME

EMBEDDING_MODEL = "mxbai-embed-large"

# Parse the file
document_list = prepare_documents(FILENAME)

# Instantiate the ChromaDB for storing the RAG
client = chromadb.PersistentClient(path=".chroma")
collection = client.get_or_create_collection(name="ttrpg_notes")

# Loop over entries for specific posts
for i, entry in enumerate(document_list):
    # Get the tags used and skip any without Books in it
    header = entry.get("header", "")
    content = entry.get("document", "")
    if content == "":
        print(f"Skipping {i}: No content found for header '{header}'")
        continue

    print(f"Processing {i}: {header}")

    # Use index as the ID
    id = str(i)

    # Gather metadata
    metadata = {
        "header": header,
        "index": i,
    }

    # Generate embeddings
    response = ollama.embed(model=EMBEDDING_MODEL, input=content)
    embeddings = response["embeddings"]

    # Add or update documents
    collection.upsert(
        documents=content, metadatas=metadata, embeddings=embeddings, ids=id
    )

print("RAG complete")
