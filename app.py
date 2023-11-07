import connexion
import flask
import flask_cors
import datetime

import exceptions
from config import config
from extensions import db_session, sentry_init


def create_app():
    sentry_init()

    connexion_app = connexion.FlaskApp(
        __name__,
        specification_dir='swaggers/',
        options={
            "swagger_ui": config.dev,
        },
    )

    connexion_app.add_api('goods.yaml')
    connexion_app.add_error_handler(exceptions.BaseError, exceptions.exception_handler)

    app: flask.Flask = connexion_app.app
    app.secret_key = config.flask_secret_key
    app.session_cookie_name = 'goods_search_session'
    app.permanent_session_lifetime = datetime.timedelta(days=100)

    @app.teardown_request
    def hook_teardown_request(e=None):
        db_session.remove()

    flask_cors.CORS(app)
    return app


app = create_app()


# @app.route('/hello_world')
# def route_hello_world():
#     from celery_tasks import add
#     add.delay(1, 0, k=666)
#     return flask.Response('hello world act-yys-sign-back')


@app.route('/')
def route_abc():
    return flask.Response('hello world')


def main():
    app.run(port=8000, debug=config.dev)
    # app.run(port=8000)


if __name__ == '__main__':
    main()

'''
/usr/local/bin/gunicorn app:app -c gunicorn.conf.py
'''