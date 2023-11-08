import openai

import constant
from config import config
from .redis_conn import cache_to_redis

openai.api_key = config.openai_api_key
openai.api_base = config.openai_api_base


class OpenaiClient(object):
    get_embedding_model = 'text-embedding-ada-002'

    def get_embedding(self, content):

        @cache_to_redis(constant.EMBEDDING_CACHE_TIME)
        def _get_embedding(text):
            # todo 批量 embedding
            text = text.replace("\n", " ")
            r = openai.Embedding.create(input=text, model=self.get_embedding_model)
            # print('get_embedding', r)
            return r['data'][0]['embedding']

        return _get_embedding(content)


openai_cli = OpenaiClient()
