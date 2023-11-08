import json
import time

import flask
import jwt

import constant
from config import config
from exceptions import InvalidAuthorization


def unix_timestamp():
    return int(time.time() * 1000)


def result_handler(data, msg='not found', errcode=400):
    if data is None:
        r = {
            'code': errcode,
            'data': data,
            'msg': msg,
        }
    else:
        r = {
            'code': 200,
            'data': data,
            'msg': 'ok',
        }

    http_code = 200
    return flask.Response(response=json.dumps(r, indent=4, ensure_ascii=False), status=http_code,
                          mimetype='application/json')


def generate_jwt_token(user_id: int):
    """根据用户id生成token"""
    t = int(time.time())
    payload = {
        'user_id': user_id,
        'exp': t + constant.JWT_TOKEN_EXPIRE_TIME,
        'ct': t,
    }
    jwt_str = jwt.encode(payload, config.jwt_secret, algorithm=constant.JWT_ALGORITHM)
    return jwt_str


def uid_from_request():
    jwt_str = flask.request.headers.get(constant.JWT_HEADER_KEY)
    return uid_from_jwt(jwt_str)


def uid_from_jwt(jwt_str):
    if jwt_str is None:
        raise InvalidAuthorization()
    try:
        _payload = jwt.decode(jwt_str, config.jwt_secret, algorithms=[constant.JWT_ALGORITHM])
    except jwt.PyJWTError:
        # print('token解析失败')
        raise InvalidAuthorization()
    else:
        exp = int(_payload.pop('exp'))
        if time.time() > exp:
            # print('已失效')
            raise InvalidAuthorization()
        else:
            return _payload['user_id']
