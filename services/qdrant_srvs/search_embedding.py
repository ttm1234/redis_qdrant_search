import constant
from extensions.qdrant_client import qdrant_collection_name
from extensions import qdrant_cli, openai_cli
from extensions.redis_conn import cache_to_redis


@cache_to_redis(constant.SEARCH_CACHE_TIME)
def query_qdrant_info(key: str):
    # 搜索相似向量
    query_vector = openai_cli.get_embedding(key)
    search_result = qdrant_cli.search(collection_name=qdrant_collection_name, query_vector=query_vector)

    r = [i.payload for i in search_result]
    # print('query_qdrant_info', key, r)
    return r
