from config import config

import redis
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType


redis_search = redis.Redis(host=config.redisearch_host, port=config.redisearch_port, db=0, decode_responses=True)

# redis_search.get('foo')  # todo delete


schema = (
    TextField("$.title", as_name="brand"),
    TextField("$.description", as_name="description"),
)

index_search = redis_search.ft("idx:sku")

try:
    index_search.create_index(
        schema,
        definition=IndexDefinition(prefix=["sku:"], index_type=IndexType.JSON),
    )
except redis.exceptions.ResponseError as e:
    if 'Index already exists' in str(e):
        print('redisearch: Index already exists ignore -- ', str(e))
        pass
    else:
        raise e

