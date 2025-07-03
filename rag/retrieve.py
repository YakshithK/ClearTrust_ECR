import os
import pickle
from sentence_transformers import SentenceTransformer
import faiss

MODEL_NAME = 'all-MiniLM-L6-v2'
BASE_DIR = os.path.dirname(__file__)
INDEX_PATH = os.path.join(BASE_DIR, 'faiss.index')
PASSAGES_PATH = os.path.join(BASE_DIR, 'passages.pkl')

model = SentenceTransformer(MODEL_NAME)
index = faiss.read_index(INDEX_PATH)
with open(PASSAGES_PATH, 'rb') as f:
    passages = pickle.load(f)

def retrieve(query, top_k=3, threshold=None):
    q_emb = model.encode([query])
    D, I = index.search(q_emb, top_k)
    results = []
    for dist, idx in zip(D[0], I[0]):
        if idx < len(passages):
            if threshold is None or dist < threshold:
                results.append((passages[idx], dist))
    return results 