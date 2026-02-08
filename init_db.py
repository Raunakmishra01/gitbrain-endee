import time
import requests
from fix_index import main as create_index
from insert_vector import main as insert_data

def wait_for_endee(max_retries=30):
    """Wait for Endee to be ready"""
    import os
    base_url = os.getenv("ENDEE_BASE_URL", "http://localhost:8081/api/v1")
    health_url = base_url.replace("/api/v1", "/health")
    
    for i in range(max_retries):
        try:
            response = requests.get(health_url, timeout=2)
            if response.status_code == 200:
                print("Endee is ready!")
                return True
        except:
            pass
        print(f"Waiting for Endee... ({i+1}/{max_retries})")
        time.sleep(2)
    
    return False

if __name__ == "__main__":
    print("Initializing GitBrain...")
    
    if wait_for_endee():
        print("Creating index...")
        create_index()
        
        print("Inserting sample data...")
        insert_data()
        
        print("Initialization complete!")
    else:
        print("Failed to connect to Endee")
