from qdrant_client import QdrantClient
import qdrant_client.http.models as qmodels

from config import config


# 在 Qdrant 中创建集合并导入数据
qdrant_cli = QdrantClient(host=config.qdrant_host)

qdrant_collection_name = 'goods_search'
METRIC = qmodels.Distance.DOT
DIMENSION = 1536
