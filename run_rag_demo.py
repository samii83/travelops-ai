
from backend.rag.retriever import retrieve_context

queries = [
    "What are the popular heritage attractions in Goa?",
    "What are the rules for hotel pricing and availability?",
    "What should the system do if transport prices are missing?"
]

for query in queries:
    print("\nQUERY:", query)
    print("-" * 60)

    results = retrieve_context(query, top_k=3)

    for result in results:
        print("Source:", result["source"])
        print("Similarity:", result["score"])
        print("Content:", result["text"])
