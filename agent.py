from endee import Endee
from sentence_transformers import SentenceTransformer
import uuid
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

ENDEE_BASE_URL = "http://localhost:8081/api/v1"
INDEX_NAME = "gitbrain"

class GitBrainAgent:
    def __init__(self):
        self.client = Endee()
        self.client.set_base_url(ENDEE_BASE_URL)
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        try:
            self.index = self.client.get_index(name=INDEX_NAME)
        except:
            console.print(f"[red]Index {INDEX_NAME} not found. Run insert_vector.py first.[/red]")
            raise
    
    def store_memory(self, text, meta):
        vec = self.model.encode(text).tolist()
        self.index.upsert([{"id": str(uuid.uuid4()), "vector": vec, "meta": {**meta, "text": text, "timestamp": datetime.now().isoformat()}}])
        console.print("[green]OK[/green] Memory stored")
    
    def search_similar(self, query, top_k=5):
        qvec = self.model.encode(query).tolist()
        return self.index.query(vector=qvec, top_k=top_k) or []
    
    def analyze_error(self, error_text):
        console.print(Panel(f"[yellow]Analyzing:[/yellow] {error_text[:100]}...", title="GitBrain Agent"))
        results = self.search_similar(error_text, top_k=3)
        
        if not results:
            console.print("[red]No similar memories found.[/red]")
            return None
        
        table = Table(title="Similar Past Issues")
        table.add_column("Score", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Tool", style="green")
        table.add_column("Memory", style="yellow")
        
        for r in results:
            meta = r.get("meta", {})
            score = f"{r.get('score', 0):.4f}" if r.get('score') else "N/A"
            table.add_row(score, meta.get("type", ""), meta.get("tool", ""), meta.get("text", "")[:80])
        
        console.print(table)
        return results[0] if results else None

def main():
    agent = GitBrainAgent()
    console.print("[bold cyan]GitBrain Agent[/bold cyan] - Your Developer Second Brain\n")
    
    while True:
        console.print("\n[bold]Options:[/bold] [1] Search Error [2] Store Memory [3] Exit")
        choice = input("Choose: ").strip()
        
        if choice == "1":
            error = input("\nPaste error/query: ").strip()
            if error:
                agent.analyze_error(error)
        elif choice == "2":
            text = input("\nMemory text: ").strip()
            mem_type = input("Type (error/fix/note): ").strip() or "note"
            tool = input("Tool (docker/python/git/api): ").strip() or "general"
            tag = input("Tag: ").strip() or "misc"
            if text:
                agent.store_memory(text, {"type": mem_type, "tool": tool, "tag": tag})
        elif choice == "3":
            console.print("[green]Goodbye![/green]")
            break

if __name__ == "__main__":
    main()
