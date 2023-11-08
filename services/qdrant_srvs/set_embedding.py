from qdrant_client.http.models import PointStruct

from extensions.qdrant_client import qdrant_collection_name
from models.sku import Sku
from extensions import qdrant_cli, openai_cli


def set_sku_qdrant(sku: Sku):
    return set_skus_qdrant([sku, ])


def set_skus_qdrant(skus: [Sku]):
    vectors = []
    for i in skus:
        i: Sku
        embedding = openai_cli.get_embedding(f'{i.title} {i.description}')
        vector = {
            "id": i.id,
            'payload': i.to_dict(),
            "vector": embedding,
        }
        vectors.append(PointStruct(**vector))
    qdrant_cli.upsert(collection_name=qdrant_collection_name, wait=False, points=vectors)
