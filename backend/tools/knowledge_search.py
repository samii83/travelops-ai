
from backend.rag.retriever import retrieve_context


def search_travel_knowledge(query: str, top_k: int = 3):
    """
    Search the travel knowledge base for relevant information.
    """
    results = retrieve_context(query, top_k)

    return {
        "found": len(results) > 0,
        "query": query,
        "results": results,
        "data_source": "faiss_travel_knowledge_base"
    }
