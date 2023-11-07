from extensions import Base, engine, db_session
from models.sku import Sku

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
    from models.sku import Sku
    # Base.metadata.create_all(bind=engine)
    Base.metadata.tables[Sku.__tablename__].create(bind=engine)


def insert_data():
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


def db_drop_all():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    # init_nltk()
    db_drop_all()
    init_db_table()
    insert_data()
