
from rag import add_website, search_knowledge, get_knowledge_count

print("AI Interview Educator - RAG Test")

url = input("\nEnter a permitted tutorial URL: ").strip()

try:
    result = add_website(url)

    print("\nWebsite successfully processed!")
    print("Title:", result["title"])
    print("Chunks saved:", result["chunks"])
    print("Total knowledge chunks:", get_knowledge_count())

    question = input("\nAsk a question about this tutorial: ")

    matches = search_knowledge(question)

    print("\nRetrieved information:\n")

    for index, match in enumerate(matches, start=1):

        print(f"Result {index}")
        print("Source:", match["source"])
        print("Content:", match["content"][:500])
        print("-" * 50)

except Exception as error:
    print("\nError:", error)
