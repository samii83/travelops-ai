
import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent
DOCUMENT_DIR = BASE_DIR / "documents"
VECTOR_DIR = BASE_DIR / "vectorstore"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_documents():
    chunks = []

    for file_path in DOCUMENT_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        # Simple paragraph-based chunking
        paragraphs = [
            p.strip()
            for p in text.split("\n\n")
            if p.strip()
        ]

        for paragraph in paragraphs:
            chunks.append({
                "text": paragraph,
                "source": file_path.name
            })

    return chunks


def build_index():
    VECTOR_DIR.mkdir(parents=True, exist_ok=True)

    documents = load_documents()

    if not documents:
        raise ValueError("No documents found in the knowledge base.")

    model = SentenceTransformer(MODEL_NAME)

    texts = [doc["text"] for doc in documents]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    embeddings = np.asarray(embeddings, dtype="float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(
        index,
        str(VECTOR_DIR / "travel.index")
    )

    with open(VECTOR_DIR / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2)

    print(f"Indexed {len(documents)} document chunks successfully.")


if __name__ == "__main__":
    build_index()
