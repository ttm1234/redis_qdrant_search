from extensions import Base, engine, db_session, qdrant_cli
from extensions import qdrant_client
import qdrant_client.http.models as qmodels
from models import Sku, SkuPrediction, SkuRating

import csv


# def init_nltk():
#     # 这里在国内默认无法下载，需要自己解决，否则下载失败。
#     # todo nltk 需要处理海外网络问题才能下载，这里先忽略，后面程序中写死
#
#     # 下载停用词数据集
#     import nltk
#     import ssl
#
#     try:
#         _create_unverified_https_context = ssl._create_unverified_context
#     except AttributeError:
#         pass
#     else:
#         ssl._create_default_https_context = _create_unverified_https_context
#
#     # nltk.download()
#     nltk.download('stopwords')


def init_db_table():
    Base.metadata.create_all(bind=engine)
    # for _Model in [Sku, SkuPrediction, SkuRating]:
    #     Base.metadata.tables[_Model.__tablename__].create(bind=engine)


def init_dqrant():
    r = qdrant_cli.recreate_collection(
        collection_name=qdrant_client.qdrant_collection_name,
        vectors_config=qmodels.VectorParams(
            size=qdrant_client.DIMENSION,
            distance=qdrant_client.METRIC,
        )
    )
    print('init_dqrant r', r)


def insert_data_goods():
    """
    批量给数据库插入数据
    """
    filename = 'data_upload/data_demo.csv'

    unsave_skus = []
    with open(filename, 'r') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            # print(row)
            sku_id = row[0] if row[0] else None
            sku = Sku.unsave_create(sku_id, row[1], row[2])
            unsave_skus.append(sku)

    db_session.bulk_save_objects(unsave_skus)
    db_session.commit()

    import celery_task
    celery_task.celery_sync_sku.delay(None)


def insert_data_rating():
    """
    批量给数据库插入数据
    """
    data = [
        [1,	1, 5],
        [1,	2, 3],
        [2,	1, 4],
        [2,	2, 2],
        [2,	3, 1],
        [3,	2, 4],
        [3,	3, 5],
        [4,	1, 2],
        [4,	4, 3],
    ]

    for user_id, sku_id, rating in data:
        m = SkuRating.find_one(user_id, sku_id)
        if m is None:
            m = SkuRating.create(user_id, sku_id, rating)
        else:
            m.update_rating(rating)

    import celery_task
    celery_task.celery_predict_rating.delay()

    return None


def insert_data():
    insert_data_goods()
    insert_data_rating()


def db_drop_all():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    # init_nltk()
    db_drop_all()
    init_dqrant()
    init_db_table()
    insert_data()
