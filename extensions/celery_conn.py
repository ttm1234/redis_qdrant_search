from celery import Celery
from celery.signals import task_postrun
from celery import signals

from config import config

log = print

broker_url = config.broker_url

_prefix = 'goods_search_20231105'

celery_app = Celery(
    _prefix + '_celery_app',
    broker=broker_url,
)

celery_app.conf.update({
    'task_acks_late': True,

    'task_default_queue': _prefix + '_default',
    'task_default_exchange': _prefix + '_default',
    'task_default_routing_key': _prefix + '_default',
})


@task_postrun.connect
def hook_task_postrun(*args, **kwargs):
    """
    :param args: tuple empty
    """
    # print('hook_task_postrun start ================', args, kwargs)
    from .mysql_conn import db_session
    db_session.remove()


# @signals.task_retry.connect
# def hook_task_retry(*args, **kwargs):
#     print('hook_task_retry start ================', args, kwargs, kwargs.keys())
#     einfo = kwargs['einfo']
#     print(type(einfo), einfo)
#     einfo_exception = einfo.exception
#     print(type(einfo_exception), einfo_exception)
#     sentry_sdk.capture_exception(einfo_exception)


from .sentry_client import sentry_init

sentry_init()
