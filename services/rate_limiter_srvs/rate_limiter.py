import datetime
import functools
import redis

from config import config
from exceptions import TooManyRequestsError
from extensions import red
from util import uid_from_request


class DailyRateLimiter(object):
    key_expire_time = 3600 * 48

    def __init__(self, redis_client, daily_limit):
        self.redis_client: redis.Redis = redis_client
        self.daily_limit = daily_limit

    def is_allowed(self, user_id):
        day_str = datetime.datetime.now().strftime("%Y-%m-%d")
        key = f'{self.__class__.__name__}:{day_str}_{user_id}'
        count = int(self.redis_client.get(key) or 0)
        if count < self.daily_limit:
            self.redis_client.incr(key)
            if count == 0:
                self.redis_client.expire(key, self.key_expire_time)
            return True
        else:
            return False

    def deco_limit(self, func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user_id = uid_from_request()
            # print('deco_limit, user_id', user_id)
            if not self.is_allowed(user_id):
                raise TooManyRequestsError()
            # -------------------------
            result = func(*args, **kwargs)

            return result

        return wrapper


# 使用示例
rate_limiter = DailyRateLimiter(red, daily_limit=config.daily_limit)
