# Query the model with document embeddings
# Following setup in https://ollama.com/blog/embedding-models

import chromadb
import ollama

EMBEDDING_MODEL = "mxbai-embed-large"
QUERY_MODEL = "gemma3:12b"  # default context size of 128k
NUM_RESULTS = 3  # how many results to include for context

# Main question to answer
input = "When did Soren get the most scrolls?"
# input = "Who is Queen Tesselia and what is her role in the campaign?"
# input = "How and when did Tririn die?"
# input = "How did the party invent Chrismas?"

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

# Grab the prior session notes
id = str(indices[0] - 1)
temp = collection.get(
	ids=[id],
    include=["documents", "metadatas"]
)
prior_notes = temp["documents"][0] if temp["documents"] else ""
prior_header = temp["metadatas"][0].get("header", "")
# Next session notes
try:
    id = str(indices[0] + 1)
    temp = collection.get(
        ids=[id],
        include=["documents", "metadatas"]
    )
    next_notes = temp["documents"][0] if temp["documents"] else ""
    next_header = temp["metadatas"][0].get("header", "")
except:
    next_notes = ""
    pass

# Use the top documents to generate a response
prompt = "Using the notes from these session: "
for d, h in zip(data, headers):
    prompt += f"{h} - {d}"
prompt += f"and this prompt: {input}. "
prompt += "Answer the prompt, including references to the session notes. "
prompt += "Attempt to be concise if possible. If you don't have enough information- say so. "
if prior_notes != "":
    prompt += f"For added context, here are prior session notes: {prior_notes} from {prior_header}. "
if next_notes != "":
    prompt += f"For added context, here are next session notes: {next_notes} from {next_header}. "

output = ollama.generate(model=QUERY_MODEL, prompt=prompt)

print(output["response"])
