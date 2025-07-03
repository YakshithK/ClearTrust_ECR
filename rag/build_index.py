import os
import pickle
from sentence_transformers import SentenceTransformer
import faiss

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), 'knowledge')
INDEX_PATH = os.path.join(os.path.dirname(__file__), 'faiss.index')
PASSAGES_PATH = os.path.join(os.path.dirname(__file__), 'passages.pkl')

model = SentenceTransformer('all-MiniLM-L6-v2')
passages = []

# Read and split documents
for fname in os.listdir(KNOWLEDGE_DIR):
    if fname.endswith('.txt'):
        with open(os.path.join(KNOWLEDGE_DIR, fname), 'r', encoding='utf-8') as f:
            for para in f.read().split('\n\n'):
                if para.strip():
                    passages.append(para.strip())

# Compute embeddings
embeddings = model.encode(passages, show_progress_bar=True)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Save index and passages
with open(PASSAGES_PATH, 'wb') as f:
    pickle.dump(passages, f)
faiss.write_index(index, INDEX_PATH)

print(f"Indexed {len(passages)} passages.")
