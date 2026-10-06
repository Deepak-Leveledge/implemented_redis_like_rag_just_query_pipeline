import hashlib
import json

from src.redis_client import redis_client
from src.config import EXACT_CACHE_TTL
from src.metric import (record_exact_hit,record_exact_miss)


def normalized_query(query: str)-> str:
     """
    Normalize user query so small formatting differences
    don't create different exact-cache keys.
    """

     return " ".join(query.lower().strip().split())


def create_exact_cache_key(query:str) -> str:
    """
    Create a deterministic Redis key from the normalized query.
    """

    normalize_query =  normalized_query(query)
    query_hash = hashlib.sha256(normalize_query.encode("utf-8")).hexdigest()

    return f"rag:exact:{query_hash}"



def get_exact_cache(query:str):
    """
    Get cached response from Redis.
    """

    cached_key = create_exact_cache_key(query)

    cached_data = redis_client.get(cached_key)

    if cached_data is None:

        record_exact_miss()

        print(
            "EXACT CACHE: MISS"
        )

        return None


    record_exact_hit()

    print(
        "EXACT CACHE: HIT"
    )

    return json.loads(cached_data)



def set_exact_cache(
        query: str,
        response : str,
        sources : list | None = None
        ):
     
     
     

    """
    Store response in Redis with TTL.
    """

    cache_key = create_exact_cache_key(query)

    cache_data = {
        "response": response,
        "sources": sources or [],
    }

    redis_client.set(
        cache_key,
        json.dumps(cache_data),
        ex=EXACT_CACHE_TTL,
    )

    print("EXACT CACHE: STORED")

    return cache_key



     