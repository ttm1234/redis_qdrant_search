"""
测试用，非项目运行代码
"""
import requests
import json


def json_log(r: requests.Response):
    try:
        print(json.dumps(r.json(), indent=4, ensure_ascii=False))
    except Exception as e:
        print(r.status_code, r.content)


_base_url = 'http://127.0.0.1:8000'

headers = {
    'GoodsSearch-Token': '''
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjQ4MjEzMzAyMTcsImN0IjoxNjk5MjY2MjE3fQ.mbTwkLMmORM1atKUkgMsIzpecdsgeTAb-B0-p5XGT6w
    '''.strip(),
}


def update_sku():
    url = _base_url + '/goods_search/update'
    data = {
        'sku_id': 5,
        'title': 'new apple',
        'description': 'this is a new apple',
    }
    r = requests.post(url, json=data, headers=headers)
    json_log(r)


if __name__ == '__main__':
    update_sku()
