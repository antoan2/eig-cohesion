import os
from redis import Redis
from tests.crud.test_weekly_meetings import redis_server


def get_redis_server() -> Redis:
    redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
    return Redis.from_url(url=redis_url)


redis_server = get_redis_server()
