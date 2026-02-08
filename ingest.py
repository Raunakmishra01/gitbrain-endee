import requests
import json

ENDEE_URL = "http://localhost:8080"
COLLECTION = "gitbrain"

def create_collection():
    url = f"{ENDEE_URL}/collections/{COLLECTION}"
    r = requests.put(url)
    print("Create collection:", r.status_code, r.text)

def ingest_doc(text, metadata):
    url = f"{ENDEE_URL}/collections/{COLLECTION}/documents"
    payload = {
        "documents": [
            {
                "text": text,
                "metadata": metadata
            }
        ]
    }
    r = requests.post(url, json=payload)
    print("Ingest:", r.status_code, r.text)

if __name__ == "__main__":
    create_collection()

    ingest_doc(
        text="Docker build failed due to missing AVX2 flag",
        metadata={
            "type": "error",
            "tool": "docker",
            "fix": "Used --avx2 flag in install.sh",
            "date": "2026-02-06"
        }
    )
