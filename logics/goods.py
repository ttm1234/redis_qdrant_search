import typing as tp

from exceptions import BaseError
from models import SkuPrediction
from models.sku import Sku
from services.permission_srv import PermissionEnum, check_permission
from services.qdrant_srvs.search_embedding import query_qdrant_info
from services.qdrant_srvs.set_embedding import set_skus_qdrant
from services.redisearch_srvs import set_skus_search
from services.redisearch_srvs.search_sku import query_redisearch_info


def sku_to_redisearch(sku_id: tp.Union[int, None]):
    if sku_id is None:
        skus = Sku.get_all_need_sync()
    else:
        sku = Sku.get_one(sku_id)
        skus = [sku, ]

    set_skus_search(skus)
    set_skus_qdrant(skus)


def goods_query(user_id, key):
    if key is None:
        return list()

    # ---------------------------
    r = query_redisearch_info(key, fuzzy=False)
    if not r:
        r = query_redisearch_info(key, fuzzy=True)

    if not r:
        r = query_qdrant_info(key)

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


def goods_recommend(user_id):
    sku_prediction = SkuPrediction.one_by_uid(user_id)
    if sku_prediction is None:
        return list()

    # ------------------------
    sku_prediction_info = sku_prediction.sku_prediction_info

    # todo 没有分页
    partial_info = sku_prediction_info[: 10]

    r = []
    for i in partial_info:
        sku_id = i[0]

        sku = Sku.get_one(sku_id)
        if sku is None:
            print('sku is None')
            # raise Exception('测试数据不严谨可能到这里，生产不会')
            continue
        r.append(sku.to_dict())

    return r

