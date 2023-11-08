import openai
from qdrant_client import QdrantClient
import qdrant_client.http.models as qmodels

import os

from qdrant_client.http.models import PointStruct

# 设置 OpenAI API 密钥
openai.api_key = "sk-f2QmBAMnkOCA0d3pcaQ5iRSDX7hKuSGgbH7Gxn6ddBWjtCtK"
openai.api_base = 'https://api.f2gpt.com/v1'


# 准备要嵌入为向量的数据
data = [
    "这是第一条文本",
    "这是第二条文本",
    "这是第三条文本"
]


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    r = openai.Embedding.create(input=text, model=model)
    # print(r)
    return r['data'][0]['embedding']


# get_embedding('this is a apple')


embeddings = []
for i in data:
    embeddings.append(get_embedding(i))


# 将嵌入向量及其对应的标识符整理为适合导入 Qdrant 的格式
vectors = []
for i, embedding in enumerate(embeddings):
    vector = {
        "id": i + 1,
        'payload': {
            'sku_id': i,
        },
        "vector": embedding,
    }
    vectors.append(PointStruct(**vector))

# 在 Qdrant 中创建集合并导入数据
client = QdrantClient()

collection_name = 'my_collection'
METRIC = qmodels.Distance.DOT
DIMENSION = 1536
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=qmodels.VectorParams(
        size=DIMENSION,
        distance=METRIC,
    )
)
client.upsert(collection_name=collection_name, wait=False, points=vectors)

# 搜索相似向量
query_vector = get_embedding('第二条')
search_result = client.search(collection_name=collection_name, query_vector=query_vector)

print(search_result)
for i in search_result:
    print(i)
    print(type(i.payload), i.payload)

# for result in search_result['result']:
#     print(f"ID: {result['payload']['id']}, Distance: {result['payload']['distance']}")
