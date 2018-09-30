from file import readFile
# list = readFile('./IDS')
# print(list)
# print(list.index(''))
# list.pop(list.index(''))
# print(list)
import requests
headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            #'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            #'Cookie': 'vip_rip=116.4.96.176; vip_address=%257B%2522pname%2522%253A%2522%255Cu5e7f%255Cu4e1c%255Cu7701%2522%252C%2522cname%2522%253A%2522%255Cu4e1c%255Cu839e%255Cu5e02%2522%252C%2522pid%2522%253A%2522104104%2522%252C%2522cid%2522%253A%2522104104119%2522%257D; vip_province=104104; vip_province_name=%E5%B9%BF%E4%B8%9C%E7%9C%81; vip_city_name=%E4%B8%9C%E8%8E%9E%E5%B8%82; vip_city_code=104104119; vip_wh=VIP_NH; tmp_mars_cid=1534914454497_8ac46d9fe282f7264af661180b9e7fa8; user_class=a; VipUINFO=luc%3Aa%7Csuc%3Aa%7Cbct%3Ac_new%7Chct%3Ac_new%7Cbdts%3A0%7Cbcts%3A0%7Ckfts%3A0%7Cc10%3A0%7Crcabt%3A0%7Cp2%3A0%7Cp3%3A1%7Cp4%3A0%7Cp5%3A0; mars_pid=0; mars_sid=adf0574a77646139736e54c9d1025ef5; visit_id=953C3ABEC5402D7B77D53B7CA27E44E4; _smt_uid=5b7cef99.2c01d95d; _jzqco=%7C%7C%7C%7C%7C1.1771330350.1534914457476.1534914659747.1534914707213.1534914659747.1534914707213.0.0.0.18.18; mars_cid=1534914454497_8ac46d9fe282f7264af661180b9e7fa8',
            'Cookie': 'oversea_jump=cn; vip_ipver=31; _smt_uid=5b6bfbab.2bc910a2; __guid=211907462.55499807891236460.1533803449303.8408; cps=adp%3Auopxvvef%3A%3A%3A%3A; vipte_viewed_=604083879%2C%2C%2C618325948; mst_csrf_key=be57ca43687b5698844555307c0fad22; vip_address=%257B%2522pid%2522%253A104104%252C%2522pname%2522%253A%2522%255Cu5e7f%255Cu4e1c%255Cu7701%2522%252C%2522cid%2522%253A104104119%252C%2522cname%2522%253A%2522%255Cu4e1c%255Cu839e%255Cu5e02%2522%252C%2522did%2522%253A104104119001%252C%2522dname%2522%253A%2522%255Cu839e%255Cu57ce%255Cu533a%2522%252C%2522sid%2522%253A%2522%2522%252C%2522sname%2522%253A%2522%2522%257D; vip_province=104104; vip_province_name=%E5%B9%BF%E4%B8%9C%E7%9C%81; vip_city_name=%E4%B8%9C%E8%8E%9E%E5%B8%82; vip_city_code=104104119; vip_wh=VIP_NH; user_class=a; VipUINFO=luc%3Aa%7Csuc%3Aa%7Cbct%3Ac_new%7Chct%3Ac_new%7Cbdts%3A0%7Cbcts%3A0%7Ckfts%3A0%7Cc10%3A0%7Crcabt%3A0%7Cp2%3A0%7Cp3%3A1%7Cp4%3A0%7Cp5%3A1; monitor_count=19; _jzqco=%7C%7C%7C%7C%7C1.510954941.1533803435681.1534914116427.1534916151068.1534914116427.1534916151068..0.0.63.63; mars_pid=0; mars_cid=1533803433469_836bd7516c39e597a76d2020c0980c9f; mars_sid=2bbf66180b0f82ad7d5b9ffec91f2509; visit_id=AD7AED38B45E2981EBAE201E5B5BD8B1',
            #'Host': 'category.vip.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
import json
from scrapy import Selector
# response = requests.get('https://cd.jd.com/description/channel?skuId=7834054&mainSkuId=7834054&cdn=2',headers = headers)
# print(response.text)
# import json
# obj = json.loads(response.text)
# from scrapy import Selector
# selector = Selector(text=obj['content'])
# result = selector.xpath('.').re('background-image:url\((.*)\)}')
# print(result)
# response = requests.get('https://c.3.cn/tencent/video_v3?vid=111111')
# obj = json.loads(response.text)
# if obj != {}:
#     print(obj['playUrl'])
# response = requests.get('http://p.3.cn/prices/mgets?skuIds=8992531')
# if 'error' not in response.text:
#     obj = json.loads(response.text)
#     if obj != {}:
#         print(obj[0]['p'])


# promotion_list = []
# response = requests.get('https://cd.jd.com/promotion/v2?skuId=7348369&area=1_72_4137_0&cat=9987%2C653%2C655',headers = headers)
# if response.status_code == 200:
#     obj = json.loads(response.text)
#     if obj['skuCoupon'] != []:
#         for i in range(0, len(obj['skuCoupon'])):
#             promotion_list.append('满' + str(obj['skuCoupon'][i]['quota']) + '减' + str(obj['skuCoupon'][i]['discount']))
#     # 即使没有pickOneTag这个属性，这样写也不会报错
#     if obj['prom']['pickOneTag']:
#         for i in range(0, len(obj['prom']['pickOneTag'])):
#             promotion_list.append('[' + obj['prom']['pickOneTag'][i]['name'] + '] ' + obj['prom']['pickOneTag'][i]['content'])
#     # 赠品
#     if obj['prom']['tags'] != []:
#         for i in range(0, len(obj['prom']['tags'])):
#             if obj['prom']['tags'][i]['code'] != '1':
#                 if obj['prom']['tags'][i]['code'] == '10':
#                     for j in range(0, len(obj['prom']['tags'][i]['gifts'])):
#                         #promotion_list.append(obj['prom']['tags']['gifts'][j]['nm'])
#                         promotion_list.append('[赠品]' + obj['prom']['tags'][i]['gifts'][j]['nm'])
#                 else:
#                     promotion_list.append('[' + obj['prom']['tags'][i]['name'] + ']' + obj['prom']['tags'][i]['content'])
#     print(promotion_list)

#https://club.jd.com/comment/skuProductPageComments.action?productId=7834054&score=0&sortType=5&page=1&pageSize=1&isShadowSku=0&rid=0&fold=1
response = requests.get('https://sclub.jd.com/comment/productPageComments.action?&productId=7834054&score=0&sortType=5&page=0&pageSize=1',headers = headers)
#这个接口无论如何都是200，所以通过response.text如果没有文本的话，不会执行if语句中的内容
if response.text:
    obj = json.loads(response.text)
    # score = str(obj['productCommentSummary']['goodRateShow']) + '%'
    # high_number = str(obj['productCommentSummary']['goodCount'])
    # medium_number = str(obj['productCommentSummary']['generalCount'])
    # low_number = str(obj['productCommentSummary']['poorCount'])
    # print(score)
    #obj = json.loads(response.text)
    #print(obj)

    impress = {}
    for i in range(0,len(obj['hotCommentTagStatistics'])):
        impress[obj['hotCommentTagStatistics'][i]['name']] = obj['hotCommentTagStatistics'][i]['count']
    print(impress)
#                  表名               字段名                   字段名       值
# db.getCollection('prices').find({'prices': { $elemMatch:{'price_value':'-1.00(有货)'}}})
# db.getCollection('prices').find({'prices': { $elemMatch:{'date':'2018-08-28'}}})

# price = parse_as_price('5357336',datetime.datetime.now().strftime('%Y-%m-%d'))
# save_to_mongo_as_a_array('prices', price.id, 'prices', price.price)