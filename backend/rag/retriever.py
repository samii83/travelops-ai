
import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent
VECTOR_DIR = BASE_DIR / "vectorstore"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model = None
_index = None
_documents = None


def load_retriever():
    global _model, _index, _documents

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)

    if _index is None:
        index_path = VECTOR_DIR / "travel.index"
        metadata_path = VECTOR_DIR / "metadata.json"

        if not index_path.exists() or not metadata_path.exists():
            raise FileNotFoundError(
                "FAISS index not found. Run python -m backend.rag.ingest first."
            )

        _index = faiss.read_index(str(index_path))

        with open(metadata_path, "r", encoding="utf-8") as f:
            _documents = json.load(f)


def retrieve_context(query: str, top_k: int = 3):
    load_retriever()

    query_embedding = _model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    scores, indices = _index.search(
        query_embedding.astype("float32"),
        min(top_k, len(_documents))
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue

        results.append({
            "text": _documents[idx]["text"],
            "source": _documents[idx]["source"],
            "score": round(float(score), 4)
        })

    return results
