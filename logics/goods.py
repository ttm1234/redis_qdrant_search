import typing as tp
from models.sku import Sku
from services import redisearch_srvs
from services.redisearch_srvs.search_sku import search_sku


def sku_to_redisearch(sku_id: tp.Union[int, None]):
    if sku_id is None:
        skus = Sku.get_all_need_sync()
    else:
        sku = Sku.get_one(sku_id)
        skus = [sku, ]

    redisearch_srvs.set_skus_search(skus)


def goods_query(user_id, key):
    if key is None:
        return list()

    # ---------------------------
    r = search_sku(key, fuzzy=False)
    if not r:
        r = search_sku(key, fuzzy=True)

    # if not r:
    #     r = func_todo(user_id, key) todo

    return r
