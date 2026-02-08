from sentence_transformers import SentenceTransformer
from endee import Client

client = Client()
model = SentenceTransformer("all-MiniLM-L6-v2")

query = "Docker SIMD build error"
query_vector = model.encode([query])[0].tolist()

results = client.search(
    index="gitbrain-memory",
    vector=query_vector,
    top_k=2
)

for r in results:
    print(r["payload"]["text"])

