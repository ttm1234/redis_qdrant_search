from redis.commands.json.path import Path

from extensions import redis_search
from models.sku import Sku


def set_sku_search(sku: Sku):
    r = redis_search.json().set(f"sku:{sku.id}", Path.root_path(), sku.to_dict())
    return r


def set_skus_search(skus: [Sku]):
    for sku in skus:
        set_sku_search(sku)
    return True
