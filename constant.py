
# todo nltk 需要处理网络问题才能下载，这里先复制下来写死
stop_words = {'they', 'them', "you're", "should've", 'm', 'its', "didn't", 'if', "haven't", 'we', 'shouldn', 'i', 'will', 'yours', "don't", 'ourselves', 'is', 'before', 'off', "shan't", 'who', "doesn't", 'll', 'was', 'more', 'shan', "isn't", 'further', "mightn't", 'until', 'than', 'be', 'o', 'yourself', 'did', "weren't", 'here', 'there', 'through', "you've", 'up', 'as', 'then', 'my', 'weren', 'own', 'it', 'me', 'do', 'haven', "mustn't", 'couldn', 'd', 'won', 'about', "wouldn't", 'each', 'hers', 'any', 'between', 'aren', 'itself', 'an', 'against', 'of', 'can', 'doing', 'all', 'ours', 'being', 'don', 'she', 'over', "won't", 'hadn', 'their', 'mustn', 'to', 'most', 'too', 't', 'when', 'yourselves', 're', 'but', "shouldn't", "that'll", 'once', 'he', 'just', 'those', 'again', 'myself', 'not', 'has', 'had', 'your', 'from', 'very', 'his', 'few', 'with', 'other', 'that', 'him', "couldn't", 'are', 'wouldn', 'because', 'both', 'whom', 'didn', 'while', 'mightn', 'after', 'out', 'under', 'now', 'wasn', 'theirs', 'what', 'these', 'and', 'himself', 'were', 'themselves', 'below', 'nor', 'how', 'at', 'so', "hasn't", 'or', "you'll", 'doesn', 'same', 'should', 'during', 'where', 'her', 'why', 'hasn', 'the', 'only', 'am', 'ma', 's', 'on', 've', 'for', 'our', 'ain', 'down', 'in', 'which', 'into', "hadn't", 'needn', 'a', 'isn', 'by', "she's", "you'd", "wasn't", 'does', "needn't", 'no', 'above', 'some', "aren't", 'herself', 'this', 'having', 'such', 'have', "it's", 'y', 'been', 'you'}

JWT_TOKEN_EXPIRE_TIME = 3600 * 24 * 365 * 99
JWT_ALGORITHM = 'HS256'
JWT_HEADER_KEY = 'GoodsSearch-Token'
SEARCH_CACHE_TIME = 10
EMBEDDING_CACHE_TIME = 3600 * 24 * 365 * 99
