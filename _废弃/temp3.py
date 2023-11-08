from surprise import Dataset
from surprise import Reader
from surprise import KNNWithMeans
from surprise.model_selection import train_test_split
import pandas as pd


# 初始数据
data = {
    'user_id': [1, 1, 2, 2, 3, 4, 5],
    'item_id': ['a', 'b', 'b', 'c', 'a', 'e', 'f'],
    'rating': [5, 3, 2, 4, 1, 5, 0]
}

# 将数据加载到Surprise的Dataset中
reader = Reader(rating_scale=(1, 5))
df = pd.DataFrame(data)
dataset = Dataset.load_from_df(df[['user_id', 'item_id', 'rating']], reader)
print(dataset.df)

# 使用基于物品的协同过滤算法
sim_options = {
    'name': 'cosine',  # 使用余弦相似度
    'user_based': False  # 基于物品
}
knn = KNNWithMeans(sim_options=sim_options)

# 在整个数据集上训练模型
trainset = dataset.build_full_trainset()
knn.fit(trainset)

# 预测用户1的推荐商品
user_id = 1
items_to_predict = ['a', 'b', 'c', 'f']  # 所有可能的物品
predictions = [knn.predict(user_id, item) for item in items_to_predict]

# 打印预测结果
for pred in predictions:
    print(f"预测用户{user_id}对物品{pred.iid}的评分为: {pred.est}")
