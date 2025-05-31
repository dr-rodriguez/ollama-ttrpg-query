

def get_additional_notes(id, collection, data, headers):
    """Helper function to get additional notes for a given ID."""

    try:
        id = str(id)
        temp = collection.get(
            ids=[id],
            include=["documents", "metadatas"]
        )
        notes = temp["documents"][0] if temp["documents"] else ""
        header = temp["metadatas"][0].get("header", "")

        # Add them to the data/headers lists
        data.append(notes)
        headers.append(header)
    except Exception as e:
        print(f"Error retrieving notes for ID {id}: {e}")
        pass

    return data, headers
