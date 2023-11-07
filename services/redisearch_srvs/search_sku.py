import json

from extensions import index_search
from redis.commands.search.query import Query
import constant
from services.cache_srvs import cache_to_redis


def process_keywords(key):
    # 澳大利亚电商，暂时只考虑英文

    # todo nltk 需要处理网络问题才能下载，这里先复制下来写死
    # from nltk.corpus import stopwords
    # stop_words = set(stopwords.words('english'))

    stop_words = constant.stop_words
    keywords = key.split(' ')

    filtered_keywords = []
    for word in keywords:
        word = word.strip()
        if word.lower() not in stop_words:
            filtered_keywords.append(f'%{word}%')

    if len(filtered_keywords) > 1:
        r = ' | '.join(filtered_keywords)
    elif len(filtered_keywords) == 1:
        r = filtered_keywords[0]
    else:
        r = ''
    return r


# 查询或搜索一般符合长尾理论，这里缓存一下，考虑到数据更改后情况缓存过于复杂，因此缓存时间设置较短
@cache_to_redis(constant.SEARCH_CACHE_TIME)
def search_sku(key: str, fuzzy: bool):
    if not fuzzy:
        print('search_sku, key', key)
        res = index_search.search(Query(key))
    else:
        s = process_keywords(key)
        print('search_sku, s', s)
        if not s:
            return list()
        res = index_search.search(Query(s))
    print(type(res), res)

    r = []
    for doc in res.docs:
        r.append(json.loads(doc.json))

    return r
