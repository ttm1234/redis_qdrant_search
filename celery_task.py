import typing as tp
import logging

from extensions.celery_conn import celery_app
from logics.goods import sku_to_redisearch


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@celery_app.task()
def celery_hello(*args, **kwargs):
    print('celery hello world', args, kwargs)


@celery_app.task(
    autoretry_for=(Exception,),
    max_retries=10,
    retry_backoff=5,
    retry_backoff_max=60 * 10,
    retry_jitter=False,
)
def celery_sync_sku(sku_id: tp.Union[int, None]):
    return sku_to_redisearch(sku_id)


'''
python3.9 -m celery worker -A celery_task -l INFO --pool=gevent --concurrency=10
'''
