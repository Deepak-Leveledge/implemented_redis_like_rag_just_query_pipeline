import redis
import json
import uuid
import numpy as np
from src.metric import (
    record_semantic_hit,
    record_semantic_miss,
)

from redis.commands.search.field import (
    TextField,
    VectorField,
)

from redis.commands.search.index_definition import (
    IndexDefinition,
    IndexType,
)

from redis.commands.search.query import Query


from src.redis_client import redis_client
from src.config import (EMBEDDING_DIMENSION,SEMANTIC_CACHE_TTL,SEMANTIC_DISTANCE_THRESHOLD)


SEMANTIC_INDEX_NAME = "rag:semantic:idx"
SEMANTIC_KEY_PREFIX = "rag:semantic:"


# =========================================================
# 1. Create Semantic Vector Index
# =========================================================

def create_semantic_index():
    """
    Create Redis vector search index for semantic cache.
    """

    # -----------------------------
    # Check if index already exists
    # -----------------------------

    try:
        redis_client.ft(
            SEMANTIC_INDEX_NAME
        ).info()

        print(
            "Semantic index already exists."
        )

        return

    except redis.exceptions.ResponseError:
        pass


    # -----------------------------
    # Define Redis Search schema
    # -----------------------------

    schema = (

        TextField("prompt"),

        TextField("response"),

        TextField("sources"),

        VectorField(
            "embedding",
            "HNSW",
            {
                "TYPE": "FLOAT32",
                "DIM": EMBEDDING_DIMENSION,
                "DISTANCE_METRIC": "COSINE",
            },
        ),

    )


    # -----------------------------
    # Create index
    # -----------------------------

    redis_client.ft(
        SEMANTIC_INDEX_NAME
    ).create_index(
        schema,
        definition=IndexDefinition(
            prefix=[
                SEMANTIC_KEY_PREFIX
            ],
            index_type=IndexType.HASH,
        ),
    )


    print(
        "Semantic vector index created."
    )



# =========================================================
# 2. Convert Embedding to Redis Format
# =========================================================

def embedding_to_bytes(
        embedding: list[float]
)-> bytes:

    vector = np.array(embedding,dtype=np.float32)

    if len(vector) != EMBEDDING_DIMENSION:

        raise ValueError(
            f"Expected {EMBEDDING_DIMENSION} "
            f"dimensions, got {len(vector)}"
        )

    return vector.tobytes()


# =========================================================
# 3. Store Semantic Cache
# =========================================================


def set_semantic_cache(
        prompt: str,
        response: str,
        embedding: list[float],
        sources: list | None = None
):

    cache_id = uuid.uuid4().hex

    cache_key = (
        f"{SEMANTIC_KEY_PREFIX}"
        f"{cache_id}"
    )

    embedding_bytes = embedding_to_bytes(
        embedding
    )

    cache_data = {

        "prompt": prompt,

        "response": response,

        "sources": json.dumps(
            sources or []
        ),

        "embedding": embedding_bytes,
    }


    # Store Hash
    redis_client.hset(
        cache_key,
        mapping=cache_data
    )


     # Set TTL
    redis_client.expire(
        cache_key,
        SEMANTIC_CACHE_TTL
    )


    print(
        "\nSEMANTIC CACHE: STORED"
    )

    print(
        "Cache Key:",
        cache_key
    )

    return cache_key


# =========================================================
# 4. Semantic Search
# =========================================================

def search_semantic_cache(
    query_embedding: list[float],
):

    query_vector = embedding_to_bytes(
        query_embedding
    )


    q = (
        Query(
            "*=>[KNN 1 @embedding "
            "$vec AS distance]"
        )
        .sort_by("distance")
        .return_fields(
            "prompt",
            "response",
            "sources",
            "distance",
        )
        .paging(0, 1)
        .dialect(2)
    )


    results = redis_client.ft(
        SEMANTIC_INDEX_NAME
    ).search(
        q,
        query_params={
            "vec": query_vector
        }
    )


    # No semantic cache entry
    if not results.docs:

        record_semantic_miss()

        print(
            "\nSEMANTIC CACHE: MISS"
        )

        return None


    doc = results.docs[0]
    # print(doc)
    # print(doc.distance)



    distance = float(
        doc.distance
    )


    print(
        "\nNearest Semantic Cache Entry"
    )

    print(
        "Prompt:",
        doc.prompt
    )

    print(
        "Distance:",
        distance
    )


    # =====================================================
    # Threshold Decision
    # =====================================================

    if distance <= SEMANTIC_DISTANCE_THRESHOLD:

        record_semantic_hit()

        print(
            "SEMANTIC CACHE: HIT"
        )


        sources = json.loads(
            doc.sources
        )


        return {
            "response": doc.response,
            "sources": sources,
            "distance": distance,
        }


    record_semantic_miss()

    print(
        "SEMANTIC CACHE: MISS "
        "(distance above threshold)"
    )

    return None

