from flask import Flask, render_template, request, jsonify
from endee import Endee
from sentence_transformers import SentenceTransformer
import uuid
from datetime import datetime
from config import *

app = Flask(__name__)

client = Endee()
client.set_base_url(ENDEE_BASE_URL)
model = SentenceTransformer(EMBEDDING_MODEL)

try:
    index = client.get_index(name=INDEX_NAME)
except:
    index = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    if not index:
        return jsonify({"error": "Index not initialized. Run insert_vector.py first."}), 500
    
    data = request.json
    query = data.get('query', '')
    top_k = data.get('top_k', 5)
    
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    qvec = model.encode(query).tolist()
    results = index.query(vector=qvec, top_k=top_k) or []
    
    formatted = []
    for r in results:
        meta = r.get("meta", {}) or {}
        score = r.get("score")
        if score is None:
            score = r.get("distance", 0)
        formatted.append({
            "score": round(float(score), 4) if score else 0,
            "type": meta.get("type", ""),
            "tool": meta.get("tool", ""),
            "tag": meta.get("tag", ""),
            "text": meta.get("text", ""),
            "timestamp": meta.get("timestamp", "")
        })
    
    return jsonify({"results": formatted})

@app.route('/api/store', methods=['POST'])
def store():
    if not index:
        return jsonify({"error": "Index not initialized"}), 500
    
    data = request.json
    text = data.get('text', '')
    mem_type = data.get('type', 'note')
    tool = data.get('tool', 'general')
    tag = data.get('tag', 'misc')
    
    if not text:
        return jsonify({"error": "Text is required"}), 400
    
    vec = model.encode(text).tolist()
    meta = {"type": mem_type, "tool": tool, "tag": tag, "text": text, "timestamp": datetime.now().isoformat()}
    
    index.upsert([{"id": str(uuid.uuid4()), "vector": vec, "meta": meta}])
    
    return jsonify({"success": True, "message": "Memory stored successfully"})

@app.route('/api/stats', methods=['GET'])
def stats():
    if not index:
        return jsonify({"error": "Index not initialized"}), 500
    
    return jsonify({
        "index_name": INDEX_NAME,
        "dimension": 384,
        "model": "all-MiniLM-L6-v2",
        "status": "active"
    })

if __name__ == '__main__':
    app.run(host=WEB_HOST, port=WEB_PORT, debug=DEBUG_MODE)
