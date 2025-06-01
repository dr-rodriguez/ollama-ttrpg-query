# Query the model with document embeddings
# Following setup in https://ollama.com/blog/embedding-models

import argparse
import chromadb
import ollama
from utils import get_additional_notes

EMBEDDING_MODEL = "mxbai-embed-large"  # 512 context size, but larger number of parameters
QUERY_MODEL = "gemma3:12b"  # default context size of 128k

# Example questions to answer
# input = "When did Soren get the most scrolls?"
# input = "Who is Tesselia and what is her role in the campaign?"
# input = "How and when did Tririn die?"
# input = "How did the party invent Chrismas?"
# input = "What god does Zinjaro worship? What are their characteristics?"
# input = "Why is the party journeying north from Helines? What is their quest and who gave it to them?"
# input = "What is the 'Mountain', the creature that destroyed the dwarven home?"

def main(input: str, num_notes: int=2, disable_extra : bool=False):
    """Main program loop to query the DnD notes."""

    # Load up the ChromaDB collection
    client = chromadb.PersistentClient(path=".chroma")
    collection = client.get_collection(name="ttrpg_notes")

    # Generate an embedding for the input and retrieve the most relevant documents
    response = ollama.embed(model=EMBEDDING_MODEL, input=input)
    results = collection.query(query_embeddings=response["embeddings"], n_results=num_notes)
    metadata = results["metadatas"][0]
    data = results["documents"][0]
    distances = results["distances"][0]

    # List of closest documents that matched
    headers = [x["header"] for x in metadata]
    indices = [x["index"] for x in metadata]
    print(f"Session notes to consider: {headers}")
    print(f"Database indices: {indices}")
    print(f"Vector distances: {distances}")

    # Add prior and next session notes to the data/headers lists
    if not disable_extra:
        orig_indeces = indices.copy()  # to avoid modifying the list while iterating
        for id in orig_indeces:
            # Skip any that are already in the indices
            # Grab the prior session notes
            if id-1 not in indices and id > 0:
                # print(f"Adding prior session notes for ID {id-1}")
                data, headers = get_additional_notes(id-1, collection, data, headers)
                indices.append(id-1)

            # Grab the next session notes
            if id+1 not in indices:
                # print(f"Adding next session notes for ID {id+1}")
                data, headers = get_additional_notes(id+1, collection, data, headers)
                indices.append(id+1)

        print("Final indexes after adding extra sessions:", indices)

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query the DnD notes for relevant information.")

    # Required string argument 'prompt'
    parser.add_argument("prompt", type=str,
                        help="A required string prompt for the program.")

    # Optional integer argument 'number_of_notes' with a default value of 2
    parser.add_argument("-n", "--num-notes", type=int, default=2,
                        help="An optional integer specifying the number of notes (default: 2).")

    # Optional flag 'disable_extra' with a default value of False
    parser.add_argument("-d", "--disable-extra", action="store_true",
                        help="An optional flag to disable fetching extra notes from prior/future sessions (default: False).")

    args = parser.parse_args()

    # Accessing the parsed arguments
    prompt = args.prompt
    num_notes = args.num_notes
    disable_extra = args.disable_extra

    print(f"Prompt: {prompt}")
    print(f"Number of notes: {num_notes}")
    print(f"Disable feching extra notes: {disable_extra}")

    # You can now use these arguments to call your program's logic
    main(prompt, num_notes=num_notes, disable_extra=disable_extra)
