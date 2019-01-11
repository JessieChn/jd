import datetime
import json
import random
import time

from items import Phone,object_to_dict,Price,SalePromotion,Opinion,Impress
import requests
from selenium import webdriver
from driver_func import pulllowfunc
from scrapy import Selector
from file import readFile,writeFile,appendFile,save_info_print
import pymongo
import schedule
import re

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

crawl_day_in_week = [0, 1, 2, 3, 4, 5, 6]

not_found_list = []

#index_page_head = 'https://search.jd.com/search?keyword=%E8%87%AA%E8%90%A5%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&lastprice=0-70&vt=2&cid2=653&cid3=655&ev=3753_172%7C%7C1097%7C%7C173%7C%7C2007%7C%7C76033%5E&stock=1&page='
#index_page_head = 'https://search.jd.com/search?keyword=%E8%87%AA%E8%90%A5%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&lastprice=0-70&vt=2&cid2=653&cid3=655&ev=3753_172%7C%7C1097%7C%7C173%7C%7C2007%7C%7C76033%5E&page='
index_page_head = 'https://search.jd.com/search?keyword=%E8%87%AA%E8%90%A5%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&cid2=653&cid3=655&page='
index_page_tail = '&click=0'
detail_page_head = 'https://item.jd.com/'
detail_page_tail = '.html'

client = pymongo.MongoClient('localhost')
db = client['jd3']


def crawl_list_page_save_as_ids():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(index_page_head + '1' + index_page_tail)
    page_number = driver.find_element_by_xpath('//div[@id="J_bottomPage"]/span[@class="p-skip"]/em/b').text
    links = []
    print(page_number)
    for i in range(1,int(page_number)+1):
    #for i in range(1, 2):
        driver.get(index_page_head + str(2*i-1) + index_page_tail)
        btn = driver.find_element_by_xpath('//div[@id="logo-2014"]/a')
        pulllowfunc(btn, 20)
        time.sleep(1)
        pulllowfunc(btn, 20)
        time.sleep(1)
        selector = Selector(text=driver.page_source)
        links = links + selector.xpath('//li[@class="gl-item"]//li[@class="ps-item"]/a/img/@data-sku').extract()
    save_info_print(links)
    driver.close()

def remove_brackets(str):
    str = re.sub(u"\\(.*?\\)|\\（.*?）", "", str)
    return str

def crawl_detail_page_save_as_mongo():
    localtime = time.localtime(time.time())
    #driver = webdriver.Chrome()
    for retry in range(0, 5):
        if retry == 0:
            links = readFile('./IDS')
            #links = ['6600258', '8992531', '5911916']
            #links = ['2868435', '100000287145', '100000287113', '100000177784', '2868393', '100000177750', '100000287133']
            #links = ['6600258']
        else:
            links = readFile('./IDS_REST')
        print('retry times :' + str(retry))
        print(links)
        not_found_list.clear()
        for x in links:
            try:
                date = datetime.datetime.now().strftime('%Y-%m-%d')
                if db['phone'].find_one({'id': 'jd' + x}, {'id': 1}) is None:
                    response = requests.get(detail_page_head + x + detail_page_tail,headers = headers)
                    #print(driver.page_source)
                    selector = Selector(text=response.text)
                    phone = parse_as_phone(x, selector)
                    print(phone.__dict__)
                    db['phone'].insert(phone.__dict__)
                price = parse_as_price(x, date)
                print(price.__dict__)
                save_to_mongo_as_a_array('prices', price._id, price.id,'prices', price.price)
                sale_promotion = parse_as_sale_promotion(x, date)
                print(sale_promotion.__dict__)
                save_to_mongo_as_a_array('sale_promotions', sale_promotion._id, sale_promotion.id, 'sale_promotion', sale_promotion.sale_promotion)
                if localtime.tm_wday in crawl_day_in_week:
                    res = parse_as_opinion_and_impress(x, date)
                    print(res['opinion'].__dict__)
                    save_to_mongo_as_a_array('opinions', res['opinion']._id ,res['opinion'].id, 'opinion_value', res['opinion'].opinion)
                    print('{\'id\': \'' + str(res['impress'].id) + '\', \'impress\': ' + str(res['impress'].impress) + '}')
                    save_to_mongo_as_a_array('impresses', res['opinion']._id , res['impress'].id, 'impress_value', res['impress'].impress)
                    res['impress'].impress.clear()
            except Exception as e:
                not_found_list.append(x)
                print(str(x) + ' : ' + str(e))
        writeFile('./IDS_REST',not_found_list)


def parse_as_phone(x, selector):
    phone = Phone()
    # 1. id
    phone._id = 'jd' + x
    phone.id = 'jd' + x
    # 2. name
    name = selector.xpath('//div[@class="sku-name"]//text()').extract()
    phone.name = name[len(name)-1].strip()
    phone.extra_message = remove_brackets(str(phone.name)).replace(' ','').lower()
    # 3.url
    phone.url = detail_page_head + x + detail_page_tail
    # 4.source
    phone.source = '京东'
    # 5.shop
    shop_url = selector.xpath('//div[@class="mt"]/h3/a/@href').extract_first()
    shop_name = selector.xpath('//div[@class="mt"]/h3/a/text()').extract_first()
    phone.shop = {
        'shop_name': shop_name if shop_name!=None else '暂无信息',
        'shop_url': shop_url if shop_url!=None else '暂无信息'
    }
    # 6 thumb_pic
    phone.thumb_pic = [str(z).replace('54x54', '430x430') for z in
        selector.xpath('//div[@id="spec-list"]/ul/li/img/@src').extract()]
    # 7 detail_pic
    #phone.detail_url = selector.xpath('//div[@id="J-detail-content"]//img/@data-lazyload').extract()
    response = requests.get('https://cd.jd.com/description/channel?skuId='+x+'&mainSkuId='+x+'&cdn=2',headers = headers)
    obj = json.loads(response.text)
    if obj['content'] != None:
        selector2 = Selector(text=obj['content'])
        phone.detail_url = selector2.xpath('.').re('background-image:url\((.*)\)}')
        phone.detail_url = phone.detail_url + selector2.xpath('.').re('data-lazyload="(.*?)"')
    # 8 video_url
    vid = selector.xpath('//div[@id="v-video"]/@data-vu').extract_first()
    phone.video_url = '暂无信息'
    if vid != None:
        response = requests.get('https://c.3.cn/tencent/video_v3?vid='+vid,
                                headers=headers)
        obj = json.loads(response.text)
        if obj != {}:
            phone.video_url = obj['playUrl']

    # 8 hot_spot
    hot_spot = selector.xpath('//ul[@class="parameter2 p-parameter-list"]').re('热点：(.*?)</li>')
    phone.hot_spot = []
    if len(hot_spot) != 0 :
        phone.hot_spot = hot_spot[0].split('，')
    # 9 brand model cpu ram rom memory_card max_men_sup screen_size resolution f_camera r_camera battery figer
    table_th = selector.xpath('//div[@data-tab="item"]//dl/dt/text()').extract()
    table_tr = selector.xpath('//div[@data-tab="item"]//dl/dd[not(@class="Ptable-tips")]/text()').extract()
    property_i_need = ['品牌', '型号', 'CPU型号', 'RAM', 'ROM', '存储卡', '最大存储扩展容量', '主屏幕尺寸（英寸）','分辨率','前置摄像头','后置摄像头','电池容量（mAh）','指纹识别']
    phone.r_camera = phone.f_camera = phone.screen_size = phone.battery = phone.pack_list = phone.brand = phone.model = phone.ram = phone.rom = phone.cpu = phone.memory_card = phone.max_mem_sup = phone.resolution = phone.figer = '暂无信息'
    for i in range(0, len(table_th)):
        if table_th[i] in property_i_need:
            if table_th[i] == '品牌':
                phone.brand = remove_brackets(table_tr[i])
            if table_th[i] == '型号':
                phone.model = remove_brackets(str(table_tr[i])).replace(' ','')
            if table_th[i] == 'RAM':
                phone.ram = table_tr[i]
            if table_th[i] == 'ROM':
                phone.rom = table_tr[i]
            if table_th[i] == 'CPU型号':
                phone.cpu = remove_brackets(table_tr[i])
            if table_th[i] == '存储卡':
                phone.memory_card = table_tr[i]
            if table_th[i] == '最大存储扩展容量':
                phone.max_mem_sup = table_tr[i]
            if table_th[i] == '分辨率':
                phone.resolution = remove_brackets(table_tr[i]).replace('x','*')
            if table_th[i] == '指纹识别':
                phone.figer = table_tr[i]
            # if table_th[i] == '包装清单':
            #     phone.pack_list = table_tr[i]
            if table_th[i] == '电池容量（mAh）':
                phone.battery = remove_brackets(table_tr[i]).replace('mAh','')
            if table_th[i] == '主屏幕尺寸（英寸）':
                phone.screen_size = remove_brackets(str(table_tr[i])).replace('英寸','').replace('”','')
            if table_th[i] == '前置摄像头':
                phone.f_camera = remove_brackets(str(table_tr[i])).replace('像素','').replace('；',' ').replace('+',' ')
            if table_th[i] == '后置摄像头':
                phone.r_camera = remove_brackets(str(table_tr[i])).replace('像素','').replace('；',' ').replace('+',' ')
    #phone.pack_list = selector.xpath('//div[@class="package-list"]/p/text()').extract()[0]
    pack_list = ''
    if selector.xpath('//div[@class="package-list"]/p/text()').extract():
        pack_list = str(selector.xpath('//div[@class="package-list"]/p/text()').extract()[0]).replace('\n','')
    else:
        pack_list = str(selector.xpath('//div[@class="package-list"]//text()').extract()[3]).replace('\n','')
    phone.pack_list = pack_list
    phone.description = ''
    return phone

# https://c0.3.cn/stock?skuId=8245366&cat=9987,653,655&area=1_72_2799_0&extraParam={%22originid%22:%221%22}
def parse_as_price(x, date):
    price = Price()
    price_value = ''
    response = requests.get('http://p.3.cn/prices/mgets?skuIds=' + x + '&pdtk=&pduid')
    if 'error' not in response.text:
        obj = json.loads(response.text)
        if obj != {}:
            print((obj[0]['p']))
            if obj[0]['p'] == '-1.00':
                price_value = '无货'
            else:
                price_value = obj[0]['p'] #+ '(有货)'
    price.id =  str(random.randint(10000,99999)) + 'jd' + x
    price._id = 'jd' + x
    price.price = {
        'price_value': price_value,
        'date': date
    }
    return price

def parse_as_sale_promotion(x , date):
    sale_promotion = SalePromotion()
    promotion_list = []
    response = requests.get('https://cd.jd.com/promotion/v2?skuId='+ x +'&area=1_72_4137_0&cat=9987%2C653%2C655',
                            headers=headers)
    if response.status_code == 200:
        obj = json.loads(response.text)
        if obj['skuCoupon'] != []:
            for i in range(0, len(obj['skuCoupon'])):
                promotion_list.append(
                    '满' + str(obj['skuCoupon'][i]['quota']) + '减' + str(obj['skuCoupon'][i]['discount']))
        # 即使没有pickOneTag这个属性，这样写也不会报错
        if obj['prom']['pickOneTag']:
            for i in range(0, len(obj['prom']['pickOneTag'])):
                promotion_list.append(
                    '[' + obj['prom']['pickOneTag'][i]['name'] + '] ' + obj['prom']['pickOneTag'][i]['content'])
        # 赠品
        if obj['prom']['tags'] != []:
            for i in range(0, len(obj['prom']['tags'])):
                if obj['prom']['tags'][i]['code'] != '1':
                    if obj['prom']['tags'][i]['code'] == '10':
                        for j in range(0, len(obj['prom']['tags'][i]['gifts'])):
                            # promotion_list.append(obj['prom']['tags']['gifts'][j]['nm'])
                            promotion_list.append('[赠品]' + obj['prom']['tags'][i]['gifts'][j]['nm'])
                    else:
                        promotion_list.append(
                            '[' + obj['prom']['tags'][i]['name'] + ']' + obj['prom']['tags'][i]['content'])
        #print(promotion_list)
        sale_promotion._id = 'jd' + x
        sale_promotion.id = 'jd' + x
        sale_promotion.sale_promotion = {
            'sale_promotion_value' : promotion_list,
            'date' : date
        }
        return sale_promotion


# https://sclub.jd.com/comment/productPageComments.action?&productId=7834054&score=0&sortType=5&page=0&pageSize=10
def parse_as_opinion_and_impress(x, date):
    opinion = Opinion()
    impress = Impress()
    # https://club.jd.com/comment/skuProductPageComments.action?productId=7834054&score=0&sortType=5&page=1&pageSize=1&isShadowSku=0&rid=0&fold=1
    response = requests.get(
        'https://sclub.jd.com/comment/productPageComments.action?&productId=' + x + '&score=0&sortType=5&page=0&pageSize=1',
        headers=headers)
    # 这个接口无论如何都是200，所以通过response.text如果没有文本的话，不会执行if语句中的内容
    high_number = medium_number = low_number  = '暂无信息'
    score = '100%'
    if response.text:
        obj = json.loads(response.text)
        score = str(obj['productCommentSummary']['goodRateShow']) + '%'
        high_number = str(obj['productCommentSummary']['goodCount'])
        medium_number = str(obj['productCommentSummary']['generalCount'])
        low_number = str(obj['productCommentSummary']['poorCount'])
        for i in range(0, len(obj['hotCommentTagStatistics'])):
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
        print('+++++++++++++')
        db[table_name].insert({'_id': _id_property, 'id': id_property})
    db[table_name].find_one_and_update({'_id': {'$regex':_id_property}},
                                       {'$push': {array_name: array_value}},
                                       upsert=True)





# schedule.every().day.at("14:48").do(crawl_list_page_save_as_ids)
# schedule.every().day.at("14:49").do(crawl_detail_page_save_as_mongo)
# while True:
#     schedule.run_pending()
    # time.sleep(1)
crawl_list_page_save_as_ids()
crawl_detail_page_save_as_mongo()
