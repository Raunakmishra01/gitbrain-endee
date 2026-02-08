import sys
from endee import Endee
from sentence_transformers import SentenceTransformer
from rich import print

ENDEE_BASE_URL = "http://localhost:8081/api/v1"
INDEX_NAME = "gitbrain"

def fmt_score(score):
    # score kabhi None aa sakta hai, isliye safe formatting
    if isinstance(score, (int, float)):
        return f"{score:.4f}"
    return "N/A"

def main():
    mode = "search"
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()

    client = Endee()
    client.set_base_url(ENDEE_BASE_URL)
    index = client.get_index(name=INDEX_NAME)

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    print(f"[bold cyan]GitBrain[/bold cyan] connected to [green]{ENDEE_BASE_URL}[/green] index=[yellow]{INDEX_NAME}[/yellow]")
    print("Modes: [bold]search[/bold] (default), [bold]agent[/bold]\n")

    q = input("Paste your query / error: ").strip()
    if not q:
        print("[red]Empty input[/red]")
        return

    qvec = model.encode(q).tolist()
    results = index.query(vector=qvec, top_k=5) or []

    if len(results) == 0:
        print("\n[yellow]No results found. Try a more specific query (add keywords like docker/avx2/simd/405 etc.)[/yellow]")
        return

    if mode == "agent":
        print("\n[bold magenta]🤖 GitBrain Agent Output (similar past fixes)[/bold magenta]")
        for i, r in enumerate(results, 1):
            meta = r.get("meta", {}) or {}
            score_str = fmt_score(r.get("score"))

            print(f"\n[i]{i})[/i] [bold]score:[/bold] {score_str}")
            print(f"   [dim]type:[/dim] {meta.get('type')}  [dim]tool:[/dim] {meta.get('tool')}  [dim]tag:[/dim] {meta.get('tag')}")
            print(f"   [yellow]{(meta.get('text','') or '')[:500]}[/yellow]")

        print("\n[bold]Next step suggestion:[/bold] Use top result as your likely fix, or refine query with file/module name.")
    else:
        print("\n[bold cyan]🔎 Search Results[/bold cyan]")
        for r in results:
            meta = r.get("meta", {}) or {}
            score_str = fmt_score(r.get("score"))
            print(f"- score={score_str} | {meta.get('type')} | {meta.get('tool')} | {meta.get('tag')}")
            print(f"  {(meta.get('text','') or '')[:300]}")

if __name__ == "__main__":
    main()
