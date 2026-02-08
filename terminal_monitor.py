import subprocess
import sys
import re
from config import ENDEE_BASE_URL, INDEX_NAME
from endee import Endee
from sentence_transformers import SentenceTransformer
import uuid
from datetime import datetime

ERROR_PATTERNS = [
    r"Error:",
    r"Exception:",
    r"Failed:",
    r"fatal:",
    r"FAILED",
    r"\[ERROR\]",
    r"Traceback"
]

class TerminalMonitor:
    def __init__(self):
        self.client = Endee()
        self.client.set_base_url(ENDEE_BASE_URL)
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        try:
            self.index = self.client.get_index(name=INDEX_NAME)
            print("GitBrain Terminal Monitor - Errors will be auto-stored")
            print("Type 'exit' to quit\n")
        except:
            print("Error: Index not found. Run: python fix_index.py && python insert_vector.py")
            raise
    
    def is_error(self, text):
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in ERROR_PATTERNS)
    
    def store_error(self, error_text):
        try:
            vec = self.model.encode(error_text[:500]).tolist()
            meta = {
                "type": "error",
                "tool": "terminal",
                "tag": "auto-captured",
                "text": error_text[:500],
                "timestamp": datetime.now().isoformat()
            }
            self.index.upsert([{"id": str(uuid.uuid4()), "vector": vec, "meta": meta}])
            print("[GitBrain: Error stored]")
        except:
            pass
    
    def run_command(self, command):
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate()
        
        if stdout:
            sys.stdout.write(stdout)
            sys.stdout.flush()
        
        if stderr:
            sys.stderr.write(stderr)
            sys.stderr.flush()
        
        output = stdout + stderr
        if process.returncode != 0 or self.is_error(output):
            self.store_error(output)

def main():
    try:
        monitor = TerminalMonitor()
    except:
        return
    
    while True:
        try:
            cmd = input("$ ").strip()
            if cmd.lower() in ['exit', 'quit']:
                print("Goodbye")
                break
            if cmd:
                monitor.run_command(cmd)
        except KeyboardInterrupt:
            print("\nGoodbye")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()
