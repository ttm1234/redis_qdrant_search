import functools
import json

import redis
from config import config


red = redis.StrictRedis(
    host=config.redis_host,
    port=config.redis_port,
    password=config.redis_password,
    db=config.redis_db,

    decode_responses=True,
)


def cache_to_redis(cache_time=None):
    """
    没有用 pickle，只写了参数返回值都是能 json 的
    """
    def decorator_cache(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"goods_search-cache_to_redis:{func.__name__}:{str((args, kwargs))}"
            # print('cache key', cache_key)

            if red.exists(cache_key):
                # print('red.exists(cache_key)', cache_key)
                result = json.loads(red.get(cache_key))

            else:
                result = func(*args, **kwargs)
                red.set(cache_key, json.dumps(result))

                if cache_time:
                    red.expire(cache_key, cache_time)

            return result
        return wrapper
    return decorator_cache
