import typing as tp

from exceptions import BaseError
from models.sku import Sku
from services import redisearch_srvs
from services.permission_srv import PermissionEnum, check_permission
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


def goods_update(user_id, data):
    if not check_permission(user_id, PermissionEnum.Update):
        raise BaseError('无权限')

    # ------------------------------
    sku_id = data['sku_id']
    sku = Sku.get_one(sku_id)
    if sku is not None:
        sku.update(data['title'], data['description'])
    else:
        sku = Sku.create(data['sku_id'], data['title'], data['description'])

    import celery_task
    celery_task.celery_sync_sku.delay(sku.id)

    return sku.to_dict()

