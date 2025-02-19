import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Get absolute path to the training_data folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # app1 directory
DATA_DIR = os.path.join(BASE_DIR, "training_data")  # training_data path

# Load Sentence Transformer model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Load FAISS index
faiss_index_path = os.path.join(DATA_DIR, "faiss_index.bin")
if not os.path.exists(faiss_index_path):
    raise FileNotFoundError(f"FAISS index file not found: {faiss_index_path}")

faiss_index = faiss.read_index(faiss_index_path)

# Load chatbot responses
response_data_path = os.path.join(DATA_DIR, "medical.json")
if not os.path.exists(response_data_path):
    raise FileNotFoundError(f"Response data file not found: {response_data_path}")

with open(response_data_path, "r", encoding="utf-8") as f:
    response_data = json.load(f)

# Function to get chatbot response
def get_chatbot_response(query):
    query_embedding = model.encode([query])  # Convert query to vector
    query_embedding = np.array(query_embedding, dtype="float32")

    _, index = faiss_index.search(query_embedding, 1)  # Find best match
    best_match_index = index[0][0]

    if best_match_index != -1:
        return response_data[best_match_index]["answer"]
    return "Sorry, I couldn't understand your question."

