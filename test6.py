import  re
import datetime
import json
import random
import time
import pymysql
from items import Phone,object_to_dict,Price,SalePromotion,Opinion,Impress
import requests
from selenium import webdriver
from driver_func import pulllowfunc
from scrapy import Selector
from file import save_ids_to_mysql, readFile,writeFile,appendFile,save_info_print
import pymongo
import schedule
import re
from setting import  DB_NAME
# your_love=re.match("wh","What are you doing? who is you mate?",re.I)
# if your_love:
#     print("you are my angle")
# else:
#     print("i lose you ")

#name = 'iPhone 7 Plus 32GB 全网通'
# name = 'vivo Y81s 3G+32G 多套餐全面屏拍照神器人脸解锁分期付款大屏美颜学生老人拍照手机'
name = 'Z3 梦幻粉(6+128G) 水滴全面屏大屏智能手机'
# 先匹配ram

# your_love=re.search('([0-9]+)GB?(\+[0-9]+GB?)?',name)
# your_love=re.search('[0-9]?G?\+?[0-9]+GB?',name)
# if your_love:
#     print("you are my angle")
#     print(your_love[0])
# else:
#     print("i lose you ")


# 内存和硬盘参数的补全
def completion_ram(ram):
    ram = str(ram)
    if '其他' in ram or 'GB' in ram:
        return ram;
    elif 'G' in ram:
        return ram + 'B'
    else:
        return ram + 'GB'

print(completion_ram('8G'))

import pymongo
# 连接mongodb数据库
client = pymongo.MongoClient('localhost')
# 连接到jd数据库
db = client['jd']

# 京东详情页请求头
headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': 'oversea_jump=cn; vip_ipver=31; _smt_uid=5b6bfbab.2bc910a2; __guid=211907462.55499807891236460.1533803449303.8408; cps=adp%3Auopxvvef%3A%3A%3A%3A; vipte_viewed_=604083879%2C%2C%2C618325948; mst_csrf_key=be57ca43687b5698844555307c0fad22; vip_address=%257B%2522pid%2522%253A104104%252C%2522pname%2522%253A%2522%255Cu5e7f%255Cu4e1c%255Cu7701%2522%252C%2522cid%2522%253A104104119%252C%2522cname%2522%253A%2522%255Cu4e1c%255Cu839e%255Cu5e02%2522%252C%2522did%2522%253A104104119001%252C%2522dname%2522%253A%2522%255Cu839e%255Cu57ce%255Cu533a%2522%252C%2522sid%2522%253A%2522%2522%252C%2522sname%2522%253A%2522%2522%257D; vip_province=104104; vip_province_name=%E5%B9%BF%E4%B8%9C%E7%9C%81; vip_city_name=%E4%B8%9C%E8%8E%9E%E5%B8%82; vip_city_code=104104119; vip_wh=VIP_NH; user_class=a; VipUINFO=luc%3Aa%7Csuc%3Aa%7Cbct%3Ac_new%7Chct%3Ac_new%7Cbdts%3A0%7Cbcts%3A0%7Ckfts%3A0%7Cc10%3A0%7Crcabt%3A0%7Cp2%3A0%7Cp3%3A1%7Cp4%3A0%7Cp5%3A1; monitor_count=19; _jzqco=%7C%7C%7C%7C%7C1.510954941.1533803435681.1534914116427.1534916151068.1534914116427.1534916151068..0.0.63.63; mars_pid=0; mars_cid=1533803433469_836bd7516c39e597a76d2020c0980c9f; mars_sid=2bbf66180b0f82ad7d5b9ffec91f2509; visit_id=AD7AED38B45E2981EBAE201E5B5BD8B1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }

def parse_as_opinion_and_impress(x, date):
    # 构造函数
    opinion = Opinion()
    # 构造函数
    impress = Impress()
    # https://club.jd.com/comment/skuProductPageComments.action?productId=7834054&score=0&sortType=5&page=1&pageSize=1&isShadowSku=0&rid=0&fold=1
    response = requests.get(
        'https://sclub.jd.com/comment/productPageComments.action?&productId=' + x + '&score=0&sortType=5&page=0&pageSize=1',
        headers=headers)
    # 这个接口无论如何都是200，所以通过response.text如果没有文本的话，不会执行if语句中的内容
    # 设置默认好评、中评、差评为暂无信息，分数默认为100%
    high_number = medium_number = low_number  = '暂无信息'
    score = '100%'
    if response.text:
        obj = json.loads(response.text)
        # 评价模块：
        score = str(obj['productCommentSummary']['goodRateShow']) + '%'
        # 好评的数量
        high_number = str(obj['productCommentSummary']['goodCount'])
        # 中评的数量
        medium_number = str(obj['productCommentSummary']['generalCount'])
        # 差评的数量
        low_number = str(obj['productCommentSummary']['poorCount'])
        # 印象模块，印象标签
        for i in range(0, len(obj['hotCommentTagStatistics'])):
            # 标签名 = 标签数
            impress.impress[obj['hotCommentTagStatistics'][i]['name']] = str(obj['hotCommentTagStatistics'][i]['count'])
    impress.impress['date'] = date
    opinion._id = 'jd' + x
    opinion.id = 'jd' + x
    impress._id = 'jd' + x
    impress.id = 'jd' + x
    opinion.opinion = {
        'high_number': high_number,
        'medium_number': medium_number,
        'low_number': low_number,
        'score': score,
        'date': date
    }
    #print(impress.impress) 要这样打印才可以
    res = {
        'opinion': opinion,
        'impress': impress
    }
    return res


def save_to_mongo_as_a_array(table_name, _id_property, id_property, array_name, array_value):
    if db[table_name].find_one({'_id': {'$regex':_id_property}},{'_id':1}) == None:
        # print('+++++++++++++')
        db[table_name].insert({'_id': _id_property, 'id': id_property , array_name: []})
        db[table_name].find_one_and_update({'_id': {'$regex':_id_property}},
                                           {'$push': {array_name: array_value}},
                                           upsert=True)
    else:
        result = db[table_name].find_one({'_id': _id_property}, {array_name: {'$slice': -1}})
        if result is not None and result[array_name][0]['date'] != array_value['date']:
            # result.prices[0].date != '2019-01-10'
            # print(result[array_name][0]['date'])
            db[table_name].find_one_and_update({'_id': {'$regex': _id_property}},
                                               {'$push': {array_name: array_value}},
                                               upsert=True)


phone = db['phone'].find_one({'model':'三星galaxynote9'})
# 通过型号获得手机后，需要修改的字段有 _id, id , name , url ,ram ,rom
#db['test'].insert(phone)
print(phone)
impress_id = str(phone['_id']).replace('jd','')
date = datetime.datetime.now().strftime('%Y-%m-%d')
# 获得他原来的_id , 通过_id可以通过京东的印象爬虫和好评率爬虫
# 读出来的是一个二维数组，需要把二维数组中每个元素的第一个元素拿出，就形成id了。
res = parse_as_opinion_and_impress(impress_id, date)
print(res['opinion'].__dict__)
#save_to_mongo_as_a_array('opinions', res['opinion']._id, res['opinion'].id, 'opinion_value',
#                         res['opinion'].opinion)
print('{\'id\': \'' + str(res['impress'].id) + '\', \'impress\': ' + str(res['impress'].impress) + '}')
#save_to_mongo_as_a_array('impresses', res['opinion']._id, res['impress'].id, 'impress_value',
#                         res['impress'].impress)
res['impress'].impress.clear()