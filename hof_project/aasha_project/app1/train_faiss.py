import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # app1 directory
DATA_DIR = os.path.join(BASE_DIR, "training_data")  # training_data folder
response_data_path = os.path.join(DATA_DIR, "medical.json")
faiss_index_path = os.path.join(DATA_DIR, "faiss_index.bin")

# Debugging output
print("Looking for dataset at:", response_data_path)


# Load dataset
with open(response_data_path, "r", encoding="utf-8") as f:
    response_data = json.load(f)

questions = [item["question"] for item in response_data]

# Load Sentence Transformer model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Convert questions to embeddings
embeddings = model.encode(questions)
embeddings = np.array(embeddings, dtype="float32")

# Create FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])  # L2 distance index
index.add(embeddings)  # Add embeddings to FAISS

# Save index
faiss.write_index(index, faiss_index_path)
print("FAISS index saved successfully!")
