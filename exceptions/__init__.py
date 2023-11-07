import json
import flask


class BaseError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.code = kwargs.get('code', 400)
        self.msg = args[0] if len(args) > 0 else kwargs.get('msg', '')


class InvalidAuthorization(BaseError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = 401
        self.msg = '未登录'


class TooManyRequestsError(BaseError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = 429
        self.msg = '请求太频繁'


def exception_handler(e: BaseError):
    assert isinstance(e, BaseError)
    code = 200
    r = {
        'code': e.code,
        'msg': e.msg or str(e),
        'data': None,
    }
    return flask.Response(response=json.dumps(r, indent=4, ensure_ascii=False), status=code,
                          mimetype='application/json')
