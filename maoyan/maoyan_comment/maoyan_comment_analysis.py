'''
glob:电影评论分析
'''

import csv
import numpy as np
import pandas as pd




def read_csv():
    # content = ''
    # 读文件
    comment = pd.read_csv(r'E:\spider\spider\maoyan\maoyan_comment_4.csv')
    # print(comment.info())
    # 缺失值并不多，所以删除含有缺失值的行
    comment.dropna()
    # 去重
    comment.drop_duplicates(['nickName', 'cityName'], inplace=True)
    # print(comment.info())
    cityName = comment.loc[:, 'cityName'].value_counts()
    # cityName.dropna()
    print(cityName)
    score = comment.loc[:, 'score'].value_counts()
    print(score)
    # i = 0
    # for row in reader:
    #     if i != 0:
    #         nickName.append(row[0])
    #         cityName.append(row[1])
    #         score.append(row[2])
    #         content = content + row[3]
    #         startTime.append(row[4])
    #         # print(row)
    #     i = i + 1
    # print('一共有：' + str(i - 1) + '个')
    # return content

read_csv()
