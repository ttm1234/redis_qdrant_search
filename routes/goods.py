from flask import request

from logics.goods import goods_query, goods_update, goods_recommend
from services.rate_limiter_srvs.rate_limiter import rate_limiter
from util import result_handler, uid_from_request


@rate_limiter.deco_limit
def api_goods_query():
    user_id = uid_from_request()
    key = request.args.get('key')

    r = goods_query(user_id, key)
    return result_handler(r)


def api_goods_recommend():
    user_id = uid_from_request()

    r = goods_recommend(user_id)
    return result_handler(r)


def api_goods_update():
    user_id = uid_from_request()
    data = request.json
    r = goods_update(user_id, data)
    return result_handler(r)
