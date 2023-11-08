from models import SkuPrediction
from models.sku_rating import SkuRating

from collections import defaultdict
import pandas as pd
from surprise import Dataset, Reader, KNNBaseline


key_user_id = 'user_id'
key_item_id = 'item_id'
key_rating = 'rating'


def pre_predict_data():
    """
    data = {
        'user_id': [1, 1, 2, 2, 3, 4],
        'item_id': ['a', 'b', 'b', 'c', 'a', 'f'],
        'rating': [5, 3, 2, 4, 1, 0]
    }
    """
    user_ids = set()
    data = defaultdict(list)

    sku_ratings = SkuRating.get_all()
    for i in sku_ratings:
        i: SkuRating
        user_ids.add(i.user_id)

        data[key_user_id].append(i.user_id)
        data[key_item_id].append(i.sku_id)
        data[key_rating].append(i.rating)

    data = dict(data)
    user_ids = list(user_ids)
    print('pre_predict_data', data, user_ids)
    return data, user_ids


def predict_rating():
    print('predict_rating start')

    data, user_ids = pre_predict_data()
    if len(data) == 0:
        print('empty sku_ratings')
        return None
    # ----------------------------------------

    # 转换为DataFrame，加载和转换数据
    df = pd.DataFrame(data)
    reader = Reader(rating_scale=(1, 5))
    dataset = Dataset.load_from_df(df[[key_user_id, key_item_id, key_rating]], reader)

    # 余弦距离，基于物品
    sim_options = {
        'name': 'cosine',
        'user_based': False,
    }
    model = KNNBaseline(sim_options=sim_options)

    # 拟合模型
    trainset = dataset.build_full_trainset()
    model.fit(trainset)

    for user_id in user_ids:
        print('for user_id in user_ids:', user_id)
        # 这里 items_to_recommend 在数据量大的时候不现实，可以另外指定一个推荐的集合比如销量大于xxx的所有商品 -- fsz
        items_to_recommend = list(set(df[key_item_id]) - set(df[df[key_user_id] == user_id][key_item_id]))
        predicted_ratings = [model.predict(user_id, item).est for item in items_to_recommend]

        # print(type(predicted_ratings), type(items_to_recommend), predicted_ratings, items_to_recommend)
        # print(list(zip(items_to_recommend, predicted_ratings)))
        top_items = [[x, y] for x, y in sorted(zip(items_to_recommend, predicted_ratings), reverse=True, key=lambda ab: ab[1])][:100]
        print('top_items', top_items)

        sku_prediction: SkuPrediction = SkuPrediction.one_by_uid(user_id)
        if sku_prediction is None:
            sku_prediction = SkuPrediction.create(user_id, top_items)
        else:
            sku_prediction.update_sku_prediction_info(top_items)

    print('predict_rating done')




















