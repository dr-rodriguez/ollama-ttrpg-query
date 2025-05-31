# Query the model with document embeddings
# Following setup in https://ollama.com/blog/embedding-models

import chromadb
import ollama
from utils import get_additional_notes

EMBEDDING_MODEL = "mxbai-embed-large"  # 512 context size, but larger number of parameters
# EMBEDDING_MODEL = "nomic-embed-text"  # larger context size of 2k, but smaller model and yields less accurate results
QUERY_MODEL = "gemma3:12b"  # default context size of 128k
NUM_RESULTS = 2  # how many results to include for context

# Main question to answer
# input = "When did Soren get the most scrolls?"
# input = "Who is Queen Tesselia and what is her role in the campaign?"
# input = "How and when did Tririn die?"
# input = "How did the party invent Chrismas?"
# input = "What god does Zinjaro worship? What are their characteristics?"
# input = "Why is the party journeying north from Helines? What is their quest and who gave it to them?"
input = "What is the 'Mountain', the creature that destroyed the dwarven home?"

# Load up the ChromaDB collection
client = chromadb.PersistentClient(path=".chroma")
collection = client.get_collection(name="ttrpg_notes")

# Generate an embedding for the input and retrieve the most relevant documents
response = ollama.embed(model=EMBEDDING_MODEL, input=input)
results = collection.query(query_embeddings=response["embeddings"], n_results=NUM_RESULTS)
metadata = results["metadatas"][0]
data = results["documents"][0]
distances = results["distances"][0]

# List of closest documents that matched
headers = [x["header"] for x in metadata]
indices = [x["index"] for x in metadata]
print(headers)
print(indices)
print(distances)

# Add prior and next session notes to the data/headers lists
orig_indeces = indices.copy()  # to avoid modifying the list while iterating
for id in orig_indeces:
    # Skip any that are already in the indices
    # Grab the prior session notes
    if id-1 not in indices and id > 0:
        print(f"Adding prior session notes for ID {id-1}")
        data, headers = get_additional_notes(id-1, collection, data, headers)
        indices.append(id-1)

    # Grab the next session notes
    if id+1 not in indices:
        print(f"Adding next session notes for ID {id+1}")
        data, headers = get_additional_notes(id+1, collection, data, headers)
        indices.append(id+1)

print("Final indexes:", indices)

# Use the documents to generate a response
prompt = "Using the notes from these session: \n"
for d, h in zip(data, headers):
    prompt += f"[START NOTES FROM {h}] \n{d}[END NOTES FROM {h}] \n\n"
prompt += f"Answer this prompt: {input}, including references to the session notes. \n"
prompt += "Attempt to be concise if possible. If you don't have enough information- say so and avoid making assumptions. "

# Store prompt for debugging
with open("prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)

output = ollama.generate(model=QUERY_MODEL, prompt=prompt)

print(output["response"])
