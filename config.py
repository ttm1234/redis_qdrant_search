import yaml


path = 'config.txt.yaml'
with open(path, encoding='utf-8') as f:
    yaml_conf = yaml.safe_load(f)
    # print(type(yaml_conf), yaml_conf)


class Config(object):
    def __init__(self):
        self.dev = yaml_conf['dev']

        self.flask_secret_key = yaml_conf['flask_secret_key']
        self.jwt_secret = yaml_conf['jwt_secret']
        self.broker_url = yaml_conf['broker_url']
        self.DB_CONFIG = yaml_conf['DB_CONFIG']

        self.redis_host = yaml_conf['redis_host']
        self.redis_port = yaml_conf['redis_port']
        self.redis_db = yaml_conf['redis_db']
        self.redis_password = yaml_conf['redis_password']

        self.redisearch_host = yaml_conf['redisearch_host']
        self.redisearch_port = yaml_conf['redisearch_port']
        self.redisearch_password = yaml_conf['redisearch_password']

        self.sentry_dsn = yaml_conf['sentry_dsn']

        self.openai_api_key = yaml_conf['openai_api_key']
        self.openai_api_base = yaml_conf['openai_api_base']

        self.qdrant_host = yaml_conf['qdrant_host']

        # ====================================================
        # 业务参数
        self.daily_limit = yaml_conf['daily_limit']


config = Config()
