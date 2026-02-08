# GitBrain 🧠
Agentic Repository Memory using Endee Vector Database

GitBrain is a terminal-based AI assistant that remembers developer errors and fixes using semantic vector search.

It acts as a "developer second brain" by storing debugging memories and retrieving them when similar problems occur.

This project demonstrates an Agentic AI workflow using Endee as the vector database.

---

## Project Overview

Developers often encounter the same errors across projects but forget past solutions.

GitBrain solves this by:
- Converting debugging knowledge into embeddings
- Storing them in Endee vector database
- Retrieving similar fixes using semantic search

This reduces debugging time and improves productivity.

---

## Demonstrated AI Use Case

Agentic AI workflow  
Semantic Search  
Vector Database integration  

Example:
A developer encounters a Docker build error. GitBrain retrieves a similar past fix.

---

## System Architecture

User Query (Terminal)
        ↓
Sentence Transformer
        ↓
Endee Vector Database
        ↓
Top-K Similar Memories
        ↓
Agent Suggestions

---

## Tech Stack

Python  
Endee Vector Database  
Sentence Transformers  
Docker  
Rich CLI  

Embedding Model:
sentence-transformers/all-MiniLM-L6-v2

Vector Dimension:
384

---

## How Endee is Used

Endee acts as long-term memory storage.

GitBrain:
- Creates index `gitbrain`
- Stores debugging memories as vectors
- Queries similar memories using vector similarity search

---

## Project Structure

