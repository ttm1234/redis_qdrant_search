import yaml


path = 'config.yaml'
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

        self.redisearch_host = yaml_conf['redisearch_host']
        self.redisearch_port = yaml_conf['redisearch_port']

        self.sentry_dsn = yaml_conf['sentry_dsn']

        # ====================================================
        # 业务参数
        self.daily_limit = yaml_conf['daily_limit']


config = Config()
