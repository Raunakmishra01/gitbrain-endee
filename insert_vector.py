from endee import Endee
from sentence_transformers import SentenceTransformer

ENDEE_BASE_URL = "http://localhost:8081/api/v1"
INDEX_NAME = "gitbrain"

def main():
    # 1) Connect to Endee
    client = Endee()
    client.set_base_url(ENDEE_BASE_URL)

    # 2) Load embedding model (384 dims)
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    # 3) Get existing index (tu UI se bana chuka hai)
    index = client.get_index(name=INDEX_NAME)

    # 4) GitBrain sample memories (errors + fixes)
    memories = [
        {
            "id": "mem1",
            "text": "Docker build failed: x86 architecture detected but no SIMD option selected.",
            "meta": {"type": "error", "tool": "docker", "tag": "simd"}
        },
        {
            "id": "mem2",
            "text": "Fix: Build Endee with AVX2 flag: ./install.sh --release --avx2 (or Docker build-arg BUILD_ARCH=avx2).",
            "meta": {"type": "fix", "tool": "docker", "tag": "simd"}
        },
        {
            "id": "mem3",
            "text": "Error: 405 Method Not Allowed happened because hitting UI route /collections. API is under /api/v1.",
            "meta": {"type": "error", "tool": "api", "tag": "routing"}
        },
        {
            "id": "mem4",
            "text": "Fix: Use Endee base URL like http://localhost:8081/api/v1 and use Python SDK Endee().",
            "meta": {"type": "fix", "tool": "api", "tag": "routing"}
        },
    ]

    # 5) Upsert vectors
    payload = []
    for m in memories:
        vec = model.encode(m["text"]).tolist()  # length 384
        payload.append({
            "id": m["id"],
            "vector": vec,
            "meta": {**m["meta"], "text": m["text"]}
        })

    index.upsert(payload)
    print("✅ Insert done:", len(payload), "memories inserted into", INDEX_NAME)

if __name__ == "__main__":
    main()
