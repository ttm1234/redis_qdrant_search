import redis
from config import config


red = redis.StrictRedis(
    host=config.redis_host,
    port=config.redis_port,
    db=config.redis_db,

    decode_responses=True,
)
