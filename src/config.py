import os
from dotenv import load_dotenv


load_dotenv()


# =========================
# Gemini Configuration
# =========================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "gemini-embedding-001"
)

EMBEDDING_DIMENSION = int(
    os.getenv(
        "EMBEDDING_DIMENSION",
        "768"
    )
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "gemini-3.1-flash-lite"
)


# =========================
# Pinecone Configuration
# =========================

PINECONE_API_KEY = os.getenv(
    "PINECONE_API_KEY"
)

PINECONE_INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME",
    "company-knowledge-base"
)

PINECONE_NAMESPACE = os.getenv(
    "PINECONE_NAMESPACE",
    "kairosoft"
)


# =========================
# Redis Configuration
# =========================

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379"
)



# Cache Configuration
# =========================

EXACT_CACHE_TTL = int(
    os.getenv(
        "EXACT_CACHE_TTL",
        "3600"
    )
)



SEMANTIC_CACHE_TTL = int(
    os.getenv(
        "SEMANTIC_CACHE_TTL",
        "3600"
    )
)

SEMANTIC_DISTANCE_THRESHOLD = float(
    os.getenv(
        "SEMANTIC_DISTANCE_THRESHOLD",
        "0.25"
    )
)

# =========================
# Validation
# =========================

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing in .env"
    )

if not PINECONE_API_KEY:
    raise ValueError(
        "PINECONE_API_KEY is missing in .env"
    )