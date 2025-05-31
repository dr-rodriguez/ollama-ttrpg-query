# Basic script to read and parse the file

FILENAME = "DnD5e Campaign 2023 Notes.txt"

def prepare_documents(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data_list = f.readlines()

    document_list = []
    document = ""
    date_header = "Initial"

    for line in data_list:
        text = line.strip()

        # Sanitize the text (quotation marks, mainly)
        text = text.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")

        # Skip empty lines
        if text == "" or text.startswith(("__", "One Shot")):
            continue

        # New session, store the document and reset
        if text.startswith(("2023-", "2024-", "2025-", "Extra Notes")):
            document_list.append({"document": document, "header": date_header})
            date_header = text
            document = ""
        else:
            document += text + "\n"
    return document_list

if __name__ == "__main__":
    document_list = prepare_documents(FILENAME)
    
    # Print the documents
    for doc in document_list:
        print(doc.get("header"))
        print(doc.get("document"))
