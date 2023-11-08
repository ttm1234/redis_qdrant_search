from surprise import Dataset, Reader, KNNBasic, KNNWithMeans, KNNBaseline

import pandas as pd

# 初始数据
data = {
    'user_id': [1, 1, 2, 2, 3, 4],
    'item_id': ['a', 'b', 'b', 'c', 'a', 'f'],
    'rating': [5, 3, 2, 4, 1, 0]
}

# 转换为DataFrame
df = pd.DataFrame(data)

# 定义Reader对象用于加载数据
reader = Reader(rating_scale=(1, 5))

# 加载数据
dataset = Dataset.load_from_df(df[['user_id', 'item_id', 'rating']], reader)

# 使用KNNBasic算法构建推荐系统
sim_options = {'name': 'cosine', 'user_based': False}  # 基于物品的协同过滤
model = KNNBaseline(sim_options=sim_options)

# 拟合模型
trainset = dataset.build_full_trainset()
model.fit(trainset)

# 为指定用户(user_id=1)进行推荐
user_id = 1
items_to_recommend = list(set(df['item_id']) - set(df[df['user_id'] == user_id]['item_id']))  # 过滤掉用户已经评分过的物品
predicted_ratings = [model.predict(user_id, item).est for item in items_to_recommend]
print(type(predicted_ratings), type(items_to_recommend), predicted_ratings, items_to_recommend)
print(list(zip(items_to_recommend, predicted_ratings)))
top_items = [x for x, _ in sorted(zip(items_to_recommend, predicted_ratings), reverse=True, key=lambda ab: ab[1])][:10]

print("为用户", user_id, "推荐的前十个商品是:", top_items)
