#coding:utf-8
from pymongo import MongoClient
from redis import Redis
import json

# 创建redis数据库链接
redis_cli = Redis('172.16.123.128',6379,0)

# 创建mongodb数据库链接
mongo_cli = MongoClient('127.0.0.1',27017)
db = mongo_cli['Tianqi']
col = db['tianqi']

while True:
    source, data = redis_cli.blpop(['tianqi:items'])
    # print (source)
    # print (data)
    str_data = data.decode()
    dict_data = json.loads(str_data)
    print (dict_data)
    col.insert(dict_data)

