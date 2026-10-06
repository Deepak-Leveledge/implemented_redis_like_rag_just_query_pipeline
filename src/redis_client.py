import redis
from src.config import REDIS_URL

redis_client = redis.from_url(REDIS_URL , decode_responses=False)

def test_redis_connection()-> bool:
    try:
        response = redis_client.ping()
        return response
    except redis.ConnectionError:
        return False