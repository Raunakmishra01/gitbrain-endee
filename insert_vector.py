from endee import Endee
from sentence_transformers import SentenceTransformer
import uuid
from datetime import datetime

ENDEE_BASE_URL = "http://localhost:8081/api/v1"
INDEX_NAME = "gitbrain"

def main():
    client = Endee()
    client.set_base_url(ENDEE_BASE_URL)
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    
    try:
        index = client.get_index(name=INDEX_NAME)
    except:
        print("Creating index...")
        client.create_index(name=INDEX_NAME, dimension=384, space_type="cosine", precision="float16")
        index = client.get_index(name=INDEX_NAME)

    memories = [
        {"text": "Docker build failed: x86 architecture detected but no SIMD option selected.", "meta": {"type": "error", "tool": "docker", "tag": "simd"}},
        {"text": "Fix: Build Endee with AVX2 flag: ./install.sh --release --avx2 (or Docker build-arg BUILD_ARCH=avx2).", "meta": {"type": "fix", "tool": "docker", "tag": "simd"}},
        {"text": "Error: 405 Method Not Allowed happened because hitting UI route /collections. API is under /api/v1.", "meta": {"type": "error", "tool": "api", "tag": "routing"}},
        {"text": "Fix: Use Endee base URL like http://localhost:8081/api/v1 and use Python SDK Endee().", "meta": {"type": "fix", "tool": "api", "tag": "routing"}},
        {"text": "Python ImportError: No module named 'torch'. Install PyTorch first.", "meta": {"type": "error", "tool": "python", "tag": "dependencies"}},
        {"text": "Fix: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu", "meta": {"type": "fix", "tool": "python", "tag": "dependencies"}},
        {"text": "Git merge conflict in package.json dependencies section.", "meta": {"type": "error", "tool": "git", "tag": "merge"}},
        {"text": "Fix: Manually resolve conflicts, keep both dependencies, run npm install to verify.", "meta": {"type": "fix", "tool": "git", "tag": "merge"}},
    ]

    payload = []
    for m in memories:
        vec = model.encode(m["text"]).tolist()
        payload.append({"id": str(uuid.uuid4()), "vector": vec, "meta": {**m["meta"], "text": m["text"], "timestamp": datetime.now().isoformat()}})

    index.upsert(payload)
    print(f"OK Inserted {len(payload)} memories into {INDEX_NAME}")

if __name__ == "__main__":
    main()
