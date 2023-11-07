import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

from config import config


def sentry_init():
    """
    可以多次 init
    https://docs.sentry.io/platforms/python/configuration/options/
    https://develop.sentry.dev/sdk/data-handling/
    """

    print('sentry_init start===========!!!!!!!!!')
    sentry_sdk.init(
        dsn=config.sentry_dsn,
        integrations=[
            FlaskIntegration(),
            CeleryIntegration(),
        ],
        traces_sample_rate=0.001,
        debug=False,
    )
    return sentry_sdk


sentry_init()
