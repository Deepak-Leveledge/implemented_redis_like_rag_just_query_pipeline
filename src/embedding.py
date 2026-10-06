import numpy as np
from google import genai
from google.genai import types
from src.exact_cache import normalized_query

from src.config import (
    GEMINI_API_KEY,
    EMBEDDING_MODEL,
    EMBEDDING_DIMENSION,
)

# Gemini client
client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_query_embedding(query: str) -> list[float]:
    """
    Generate a 768-dimensional normalized embedding
    for a user retrieval query.
    """

    normalize_query = normalized_query(query)

    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=normalize_query,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSION,
            task_type="RETRIEVAL_QUERY",
        ),
    )

    # First embedding
    embedding_values = result.embeddings[0].values

    # Convert to numpy
    vector = np.array(
        embedding_values,
        dtype=np.float32
    )

    # Validate dimension
    if len(vector) != EMBEDDING_DIMENSION:
        raise ValueError(
            f"Expected {EMBEDDING_DIMENSION} dimensions, "
            f"but received {len(vector)}"
        )

    # IMPORTANT:
    # gemini-embedding-001 needs manual normalization
    # for non-default dimensions such as 768.
    norm = np.linalg.norm(vector)

    if norm == 0:
        raise ValueError(
            "Embedding vector has zero norm."
        )

    normalized_vector = vector / norm

    return normalized_vector.tolist()