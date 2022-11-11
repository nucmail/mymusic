#@Time : 2021/12/31 8:49
# Thanks to Siraj Raval for this module
'''两种推荐算法：基于物品相似度和对于新用户的冷启动'''
import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix
import math as mt
from scipy.sparse.linalg import *  # used for matrix multiplication
from scipy.sparse.linalg import svds
from scipy.sparse import csc_matrix
# Class for Popularity based Recommender System model
# 计算统计返回歌曲表中每首歌的被听次数，用于新用户（解决冷启动）
class popularity_recommender_py():
    def __init__(self):
        self.train_data = None
        self.user_id = None
        self.item_id = None
        self.popularity_recommendations = None

    def create(self, train_data, user_id, item_id):
        self.train_data = train_data
        self.user_id = user_id
        self.item_id = item_id  # 进行分类的指标：可以选择 歌曲名 歌手 年份 等等
        train_data_grouped = train_data.groupby([self.item_id]).agg(
            {self.user_id: 'count'}).reset_index()  # 计算按分类指标的播放次数
        train_data_grouped.rename(columns={self.user_id: 'score'}, inplace=True)
        train_data_sort = train_data_grouped.sort_values(['score', self.item_id], ascending=[0, 1])  # 对计算结果进行排序
        train_data_sort['Rank'] = train_data_sort['score'].rank(ascending=0, method='first')
        self.popularity_recommendations = train_data_sort.head(10)  # 返回前十名推荐歌曲作为推荐结果

    def recommend(self):  # 得到一个包含被推荐用户，歌曲id，得分，排名的数据框
        return self.popularity_recommendations['song_id']


# 基于用户的歌曲相似度进行推荐（基于用户的协同过滤算法）返回的是推荐歌曲的dataFrame
class user_similarity_recommender_py():

    def __init__(self):
        self.train_data = None
        self.user_id = None
        self.user_title = None  # user_id
        self.item_title = None
        self.ans_user_set = {}

    def create(self, train_data, user_title, item_title, user_id):  # 构造对象
        self.user_title = user_title
        self.train_data = train_data
        self.item_title = item_title
        self.user_id = user_id  # 待推荐用户id

    def get_all_user_train_data(self):  # 获取training data中的所有用户id
        all_users = list(self.train_data[self.user_title].unique())
        return all_users

    def get_user_items(self, user):  # 获取user用户听过的所有歌的列表
        user_data = self.train_data[self.train_data[self.user_title] == user]  # user这个用户都听了哪几首歌
        user_items = list(user_data[self.item_title].unique())
        return user_items

    def get_similarity_users(self):  # 获取前十个相似的用户
        all_users = self.get_all_user_train_data()  # 得到所有用户
        song_user = set(self.get_user_items(self.user_id))  # 得到待推荐用户听过的歌
        lis = []
        for i in all_users:  # 对于数据集中的每一个用户
            l = []
            song_i = set(self.get_user_items(i))
            songs_intersection = song_i.intersection(song_user)  # 计算这两名用户听过歌曲的交集
            if len(songs_intersection) != 0:
                songs_union = song_i.union(song_user)  # 计算这两名用户听过歌曲的并集
                score = float(len(songs_intersection)) / float(len(songs_union))  # 计算这两名用户的相似度
                l.append(i)
                l.append(score)
                lis.append(l)
        lis.sort(key=lambda x: x[1], reverse=True)  # 按相似度对用户进行排序
        ans = []
        return lis
        for i in range(0, min(5, len(lis))):
            ans.append(lis[i][0])  # 得到前五名用户的user_id
        return ans

    def get_ans(self):  # 得到推荐的前十首歌曲id
        ini_songs = self.get_user_items(self.user_id)
        users = self.get_similarity_users()  # 得到与被推荐用户最相似的前五名用户的id
        columns = ['similary_users', 'songs']
        ans = []
        for i in users:  # 对于每一个推荐结果用户
            recommend_user = i[0]
            songs = self.get_user_items(recommend_user)  # 得到推荐结果用户听过的所有歌
            for recommend_song in songs:
                if recommend_song not in ini_songs and recommend_song not in ans:  # 如果这首歌没被推荐过，待推荐用户也没有听过
                    ans.append(recommend_song)
                    if len(ans) == 10:  # 限制返回的歌曲数量
                        return ans


# Class for Item similarity based Recommender System model
# 基于歌曲的受众相似度进行推荐（基于物品的协同过滤算法）返回的是推荐歌曲的dataFrame
class item_similarity_recommender_py():
    def __init__(self):
        self.train_data = None
        self.user_id = None
        self.item_id = None
        self.cooccurence_matrix = None
        self.songs_dict = None
        self.rev_songs_dict = None
        self.item_similarity_recommendations = None
        self.dic = {}

    def create(self, train_data, user_id, item_id):
        self.train_data = train_data
        self.user_id = user_id
        self.item_id = item_id
        self.get_my_dic()

    def get_user_items(self, user):
        user_data = self.train_data[self.train_data[self.user_id] == user]  # user这个用户都听了哪几首歌
        user_items = list(user_data[self.item_id].unique())
        return user_items

    def get_item_users(self, item):
        item_data = self.train_data[self.train_data[self.item_id] == item]
        item_users = set(item_data[self.user_id].unique())
        return item_users

    def get_all_items_train_data(self):
        all_items = list(self.train_data[self.item_id].unique())
        # print("all_items:",all_items)
        return all_items

    def get_my_dic(self):  # 得到每首歌的听众字典
        user_id = self.train_data[self.user_id]
        song_title = self.train_data[self.item_id]
        for i in song_title:
            self.dic[i] = []
        lis = []
        j = 0
        for i in song_title:
            self.dic[i].append(user_id[j])
            j += 1

    def construct_cooccurence_matrix(self, user_songs, all_songs):  # 构造相似度矩阵
        cooccurence_matrix = np.matrix(np.zeros(shape=(len(user_songs), len(all_songs))), float)
        for i in range(0, len(all_songs)):  # 遍历所有的歌
            users_i = set(self.dic[all_songs[i]])  # 取出听过这一首歌的用户
            for j in range(0, len(user_songs)):  # 遍历待推荐用户听过的所有歌
                users_j = set(self.dic[user_songs[j]])  # 取出听过这一首歌的用户
                users_intersection = users_i.intersection(users_j)
                if len(users_intersection) != 0:
                    users_union = users_i.union(users_j)
                    cooccurence_matrix[j, i] = float(len(users_intersection)) / float(
                        len(users_union))  # 用Jacccard相似系数作为衡量相似度
                else:
                    cooccurence_matrix[j, i] = 0
        return cooccurence_matrix

    def generate_top_recommendations(self, user, cooccurence_matrix, all_songs, user_songs):
        user_sim_scores = cooccurence_matrix.sum(axis=0) / float(cooccurence_matrix.shape[0])
        # 每首歌总得分为这首歌与user_songs中所有歌相似度的平均值
        user_sim_scores = np.array(user_sim_scores)[0].tolist()  # 得到每首歌的推荐下标
        sort_index = sorted(((e, i) for i, e in enumerate(list(user_sim_scores))), reverse=True)  # 将歌曲按总相似度进行排序
        columns = ['user_id', 'song', 'score', 'rank']
        df = pd.DataFrame(columns=columns)  # 构造一个DataFrame类型暂时存储推荐结果
        rank = 1  # 限制返回的歌曲数量
        for i in range(0, len(sort_index)):  # 遍历推荐列表
            if ~np.isnan(sort_index[i][0]) and all_songs[sort_index[i][1]] not in user_songs and rank <= 10:
                # 如果这首歌待推荐用户没有听过，并且推荐下标在10以内
                df.loc[len(df)] = [user, all_songs[sort_index[i][1]], sort_index[i][0], rank]  # 将这首歌的信息存入df
                rank = rank + 1
        ans = list(df['song'])  # 返回推荐的歌曲名列表
        return ans

    def recommend(self, user):  # 得到推荐的十首歌曲id
        user_songs = self.get_user_items(user)  # 得到待推荐用户听过的所有的歌
        all_songs = self.get_all_items_train_data()  # 得到数据集中所有的歌名
        cooccurence_matrix = self.construct_cooccurence_matrix(user_songs, all_songs)  # 计算得到相似度矩阵
        recommendations = self.generate_top_recommendations(user, cooccurence_matrix, all_songs,
                                                            user_songs)  # 得到推荐的歌曲名列表
        return recommendations


# SVD分解预测用户的评分 返回值类型还需处理
class SVD():
    def __init__(self):
        self.User_id = None
        self.uTest = None
        self.train_data = None
        self.user_id = None
        self.mt_candidate = None
        self.small_set = None
        self.K = None
        self.MAX_UID = None
        self.MAX_PID = None
        self.urm = None

    def create(self, train_data, user_id):
        self.train_data = train_data
        self.User_id = user_id
        # self.user_id = user_id

    def process_data(self):
        self.small_set = self.train_data
        user_codes = self.small_set.user_id.drop_duplicates().reset_index()  # 得到所有的用户，去除重复值
        song_codes = self.small_set.song_id.drop_duplicates().reset_index()  # 得到所有的歌id，去除重复值
        user_codes.rename(columns={'index': 'user_index'}, inplace=True)
        song_codes.rename(columns={'index': 'song_index'}, inplace=True)
        song_codes['so_index_value'] = list(song_codes.index)
        user_codes['us_index_value'] = list(user_codes.index)
        self.small_set = pd.merge(self.small_set, song_codes, how='left')
        self.small_set = pd.merge(self.small_set, user_codes, how='left')
        us_ids = user_codes['user_id']
        us_index_values = user_codes['us_index_value']
        for i in range(len(us_ids)):
            if us_ids[i] == self.User_id:
                self.uTest = us_index_values[i]
                break
            if self.uTest != None:
                break
        self.mat_candidate = self.small_set[['us_index_value', 'so_index_value', 'fractional_play_count']]

    def get_data_sparse(self):
        data_array = self.mat_candidate.fractional_play_count.values
        row_array = self.mat_candidate.us_index_value.values
        col_array = self.mat_candidate.so_index_value.values

        data_sparse = coo_matrix((data_array, (row_array, col_array)), dtype=float)
        self.K = 250
        self.urm = data_sparse
        self.MAX_PID = self.urm.shape[1]
        self.MAX_UID = self.urm.shape[0]

    def compute_svd(self, urm, K):  # 进行矩阵分解，返回U、S、Vt三个矩阵
        U, s, Vt = svds(urm, K)
        dim = (len(s), len(s))
        S = np.zeros(dim, dtype=np.float32)
        for i in range(0, len(s)):
            S[i, i] = mt.sqrt(s[i])
        U = csc_matrix(U, dtype=np.float32)  # 用来进行稀疏矩阵的压缩
        S = csc_matrix(S, dtype=np.float32)
        Vt = csc_matrix(Vt, dtype=np.float32)
        return U, S, Vt

    def compute_estimated_matrix(self, urm, U, S, Vt, K, test):
        rightTerm = S * Vt  # 对于每一个用户 U * S * Vt 得到的是他的坐标
        max_recommendation = 250
        estimatedRatings = np.zeros(shape=(self.MAX_UID, self.MAX_PID), dtype=np.float16)
        recomendRatings = np.zeros(shape=(self.MAX_UID, max_recommendation), dtype=np.float16)
        userTest = self.uTest
        prod = U[userTest, :] * rightTerm
        estimatedRatings[userTest, :] = prod.todense()  # 得到用户U的预测评分列表
        recomendRatings[userTest, :] = (-estimatedRatings[userTest, :]).argsort()[:max_recommendation]  # 将评分表进行排序
        # 将计算结果按评分排序后返回
        return recomendRatings

    def get_ans(self):
        self.process_data()
        self.get_data_sparse()
        U, S, Vt = self.compute_svd(self.urm, self.K)
        uTest_recommended_items = self.compute_estimated_matrix(self.urm, U, S, Vt, self.K, True)
        user = self.uTest
        ans_lis = []
        for i in uTest_recommended_items[user, 0:10]:  # 得到前十个评分最高的歌曲信息
            song_details = self.small_set[self.small_set.so_index_value == i].drop_duplicates('so_index_value')[
                ['song_id']]
            ans_lis.append(list(song_details['song_id'])[0])  # 将歌曲名添加至答案列表中
        return ans_lis