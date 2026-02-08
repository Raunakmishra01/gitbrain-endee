# GitBrain Configuration

import os

# Endee Settings
ENDEE_BASE_URL = os.getenv("ENDEE_BASE_URL", "http://localhost:8081/api/v1")
INDEX_NAME = "gitbrain"
VECTOR_DIMENSION = 384
SPACE_TYPE = "cosine"
PRECISION = "float16"

# Embedding Model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Search Settings
DEFAULT_TOP_K = 5
MAX_TOP_K = 20

# Web App Settings
WEB_HOST = "0.0.0.0"
WEB_PORT = 5000
DEBUG_MODE = False
