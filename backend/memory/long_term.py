import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# load embedding model (free)
model = SentenceTransformer('all-MiniLM-L6-v2')

dimension = 384

index = faiss.IndexFlatL2(dimension)
memory_texts = []

def embed(text):
    return model.encode([text])[0]

def add_to_long_memory(text):
    vector = embed(text).astype('float32')
    index.add(np.array([vector]))
    memory_texts.append(text)
top_k = 3
def retrieve_long_memory(query):
    if len(memory_texts) == 0:
        return []

    vector = embed(query).astype('float32')
    D, I = index.search(np.array([vector]), k=top_k)

    results = []
    for idx, dist in zip(I[0], D[0]):
        if idx < len(memory_texts):
            results.append({
                "text": memory_texts[idx],
                "score": float(dist)
            })

    return results