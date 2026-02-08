from endee import Endee

ENDEE_BASE_URL = "http://localhost:8081/api/v1"
INDEX_NAME = "gitbrain"

def main():
    client = Endee()
    client.set_base_url(ENDEE_BASE_URL)

    # delete if exists (ignore if not)
    try:
        idx = client.get_index(name=INDEX_NAME)
        idx.delete()
        print("Deleted old index:", INDEX_NAME)
    except Exception as e:
        print("No old index to delete (ok):", str(e)[:120])

    # create fresh index (384 dims)
    client.create_index(
        name=INDEX_NAME,
        dimension=384,
        space_type="cosine",
        precision="float16"
    )
    print("✅ Created fresh index:", INDEX_NAME)

if __name__ == "__main__":
    main()
