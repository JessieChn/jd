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
from setting import DB_NAME


# 唯品会请求头
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'vip_province=104104; vip_province_name=%E5%B9%BF%E4%B8%9C%E7%9C%81; vip_city_name=%E4%B8%9C%E8%8E%9E%E5%B8%82; vip_city_code=104104119; vip_wh=VIP_NH; vip_ipver=31; mars_pid=0; _smt_uid=5c340da8.1d077571; __guid=156497070.4162290785011181000.1546915264393.8486; vip_address=%257B%2522pid%2522%253A104104%252C%2522pname%2522%253A%2522%255Cu5e7f%255Cu4e1c%255Cu7701%2522%252C%2522cid%2522%253A104104119%252C%2522cname%2522%253A%2522%255Cu4e1c%255Cu839e%255Cu5e02%2522%252C%2522did%2522%253A104104119001%252C%2522dname%2522%253A%2522%255Cu839e%255Cu57ce%255Cu533a%2522%252C%2522sid%2522%253A%2522%2522%252C%2522sname%2522%253A%2522%2522%257D; user_class=a; VipUINFO=luc%3Aa%7Csuc%3Aa%7Cbct%3Ac_new%7Chct%3Ac_new%7Cbdts%3A0%7Cbcts%3A0%7Ckfts%3A0%7Cc10%3A0%7Crcabt%3A0%7Cp2%3A0%7Cp3%3A1%7Cp4%3A0%7Cp5%3A1; vipAc=405fadd5fb3d3440e0954db466aef623; mars_sid=2feb3388c3aa3b5042113484507d1f56; visit_id=1B440318908C0842691A173D77891F32; monitor_count=17; vipte_viewed_=2151166325%2C540239772668123%2C540239772672219%2C540239773077723%2C646959378; _jzqco=%7C%7C%7C%7C%7C1.2035712575.1546915240937.1547428450905.1547429363407.1547428450905.1547429363407..0.0.55.55; mars_cid=1546915238563_28adf14b5bb0834a92b98390b55da69e',
    'Host':'detail.vip.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

# 活动请求头,注意reference要替换
header_promotion = {
    'accept':'*/*',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'zh-CN,zh;q=0.9',
    'cookie':'vip_province=104104; vip_province_name=%E5%B9%BF%E4%B8%9C%E7%9C%81; vip_city_name=%E4%B8%9C%E8%8E%9E%E5%B8%82; vip_city_code=104104119; vip_wh=VIP_NH; vip_ipver=31; mars_pid=0; _smt_uid=5c340da8.1d077571; vip_address=%257B%2522pid%2522%253A104104%252C%2522pname%2522%253A%2522%255Cu5e7f%255Cu4e1c%255Cu7701%2522%252C%2522cid%2522%253A104104119%252C%2522cname%2522%253A%2522%255Cu4e1c%255Cu839e%255Cu5e02%2522%252C%2522did%2522%253A104104119001%252C%2522dname%2522%253A%2522%255Cu839e%255Cu57ce%255Cu533a%2522%252C%2522sid%2522%253A%2522%2522%252C%2522sname%2522%253A%2522%2522%257D; VipUINFO=luc%3Aa%7Csuc%3Aa%7Cbct%3Ac_new%7Chct%3Ac_new%7Cbdts%3A0%7Cbcts%3A0%7Ckfts%3A0%7Cc10%3A0%7Crcabt%3A0%7Cp2%3A0%7Cp3%3A1%7Cp4%3A0%7Cp5%3A1; user_class=a; mars_sid=e36946cf857b59dd2240a993a1c785e7; visit_id=444A397853656C81EA329111739C1FCB; __guid=136073383.1637109775761122000.1547528597452.4211; vipte_viewed_=525768804348867%2C538776774862083%2C549970002338846%2C549970002347038%2C541293914691264; _jzqco=%7C%7C%7C%7C%7C1.2035712575.1546915240937.1547528883169.1547529342592.1547528883169.1547529342592..0.0.211.211; mars_cid=1546915238563_28adf14b5bb0834a92b98390b55da69e; monitor_count=5',
    'referer':'https://detail.vip.com/detail-100050400-541293914691264.html',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

# 京东详情页请求头
jd_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': 'oversea_jump=cn; vip_ipver=31; _smt_uid=5b6bfbab.2bc910a2; __guid=211907462.55499807891236460.1533803449303.8408; cps=adp%3Auopxvvef%3A%3A%3A%3A; vipte_viewed_=604083879%2C%2C%2C618325948; mst_csrf_key=be57ca43687b5698844555307c0fad22; vip_address=%257B%2522pid%2522%253A104104%252C%2522pname%2522%253A%2522%255Cu5e7f%255Cu4e1c%255Cu7701%2522%252C%2522cid%2522%253A104104119%252C%2522cname%2522%253A%2522%255Cu4e1c%255Cu839e%255Cu5e02%2522%252C%2522did%2522%253A104104119001%252C%2522dname%2522%253A%2522%255Cu839e%255Cu57ce%255Cu533a%2522%252C%2522sid%2522%253A%2522%2522%252C%2522sname%2522%253A%2522%2522%257D; vip_province=104104; vip_province_name=%E5%B9%BF%E4%B8%9C%E7%9C%81; vip_city_name=%E4%B8%9C%E8%8E%9E%E5%B8%82; vip_city_code=104104119; vip_wh=VIP_NH; user_class=a; VipUINFO=luc%3Aa%7Csuc%3Aa%7Cbct%3Ac_new%7Chct%3Ac_new%7Cbdts%3A0%7Cbcts%3A0%7Ckfts%3A0%7Cc10%3A0%7Crcabt%3A0%7Cp2%3A0%7Cp3%3A1%7Cp4%3A0%7Cp5%3A1; monitor_count=19; _jzqco=%7C%7C%7C%7C%7C1.510954941.1533803435681.1534914116427.1534916151068.1534914116427.1534916151068..0.0.63.63; mars_pid=0; mars_cid=1533803433469_836bd7516c39e597a76d2020c0980c9f; mars_sid=2bbf66180b0f82ad7d5b9ffec91f2509; visit_id=AD7AED38B45E2981EBAE201E5B5BD8B1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }


# 连接mongodb数据库
client = pymongo.MongoClient('localhost')
# 连接到jd数据库
db = client['jd']

# 打开mysql数据库连接
mysql_db = pymysql.connect("localhost", "root", "root", DB_NAME)
# 使用cursor()方法获取操作游标
cursor = mysql_db.cursor()

# 唯品会详情页的链接头
detail_page_head = 'https://detail.vip.com/detail-'
# 唯品会详情页的链接尾
detail_page_tail = '.html'

# 内存和硬盘参数的补全
def completion_ram(ram):
    # 把ram转化成字符串类型
    ram = str(ram)
    # 如果ram中包含'其他' 或者 包含'GB'，就直接return
    if '其他' in ram or 'GB' in ram:
        return ram;
    # 或者如果只包含G没有包含B，就加B后return
    elif 'G' in ram:
        return ram + 'B'
    # 或者没有包含GB也没有包含B，因此只有数字，就加GB后return
    else:
        return ram + 'GB'


def parse_as_opinion_and_impress(x, date):
    # 构造函数
    opinion = Opinion()
    # 构造函数
    impress = Impress()
    # https://club.jd.com/comment/skuProductPageComments.action?productId=7834054&score=0&sortType=5&page=1&pageSize=1&isShadowSku=0&rid=0&fold=1
    response = requests.get(
        'https://sclub.jd.com/comment/productPageComments.action?&productId=' + x + '&score=0&sortType=5&page=0&pageSize=1',
        headers=jd_headers)
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


# 唯品会详情页爬取
def crawl_detail_page_save_as_mongo():
    # 获得当前时间
    # 结构 time.struct_time(tm_year=2019, tm_mon=1, tm_mday=8, tm_hour=15, tm_min=50, tm_sec=27, tm_wday=1, tm_yday=8, tm_isdst=0) wday ： 0到 6
    localtime = time.localtime(time.time())
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    # 从group表中获得 distinct的 model
    cursor.execute('select distinct model from t_group;')
    # 读出来的是一个二维数组，需要把二维数组中每个元素的第一个元素拿出，就形成id了。
    links = [x[0] for x in cursor.fetchall()]
    # 类似这样 ['酷派酷玩7c', '华为麦芒7', 'vivoy81s', '努比亚z18', '华为荣耀8xmax']
    print(links)
    # links = ['360n7']
    # 循环遍历手机型号
    for x in links:
        # 异常处理，保存数据库的时候如果主键重复了代码不会停止，而是继续遍历
        try:
            # 保存原来的x为temp_x
            temp_x = x;
            # 唯品会搜索的坑1：搜索'华为荣耀'的时候搜索不了，要改为'荣耀'
            if '华为荣耀' in str(x):
                x = str(x).replace('华为荣耀','荣耀')
            # 唯品会搜索的坑2：搜索'max'且连在一起的时候搜索不了，要加个空格
            if 'max' in str(x):
                x = str(x).replace('max', ' max')
            # 请求唯品会搜索链接，获得响应
            response = requests.get('https://category.vip.com/suggest.php?keyword='+ x +'&cid_2_show=136582')
            # print(response.text)
            # 把响应体传入选择器的构造函数中
            selector = Selector(text=response.text)
            # print(selector.xpath('.').re('"products":(.*?)}\);'))
            # 打印下循环元素
            print(x)
            # 用正则匹配获得搜索的结果，用if xxx 的方式不存在的话也不会报错
            if selector.xpath('.').re('"products":(.*?)}\);')[0]:
                search_result = selector.xpath('.').re('"products":(.*?)}\);')[0]
                # 打印搜索结果
                # print(search_result)
                # 将匹配的json字符串转换为一个对象（这个对象是个数组）
                search_result_array = json.loads(search_result)
                # 当数组不为空时
                if search_result_array != []:
                    # 当数组不为空时，对数组进行循环遍历
                    for y in search_result_array:
                        # 获得当前数组第n个元素的type属性（注意经过观察，tpye为0时为有货，type为1时为无货）
                        sold = y['type']
                        # 当sold为0时，表示有货
                        if sold == 0:
                            # 需要注意的属性：
                            # 价格 : price_info.vipshop_price ,
                            # url :  brand_id + product_id
                            # name : product_name ,
                            # v_spu_id : 类似： 22313221757980672
                            # 对ID进行赋值，另外头加上vip
                            id = 'vip' + y['v_spu_id']
                            # 对skuid进行赋值
                            skuid = y['v_spu_id']
                            # 对name进行赋值
                            name = y['product_name']
                            # 对price进行赋值
                            price = y['price_info']['vipshop_price']
                            # 对链接进行拼接赋值
                            url = detail_page_head + y['brand_id'] + '-' + y['product_id'] + detail_page_tail
                            # 对链接进行请求并获得响应
                            response = requests.get(url , headers)
                            # print(response.text)
                            # 对源头进行赋值
                            source = '唯品会'
                            # 对详情页的响应体传入选择器的构造函数中
                            selector2 = Selector(text=response.text)
                            # 获得了详情页表格的table的th信息
                            table_th = selector2.xpath('//table[contains(@class,"dc-table")]//th/text()').extract()
                            # 获得了详情页表格的table的td信息d
                            table_tr = selector2.xpath('//table[contains(@class,"dc-table")]//td/text()').extract()
                            # 对ram rom进行默认赋值，默认为’其他‘
                            ram = rom = '其他'
                            # 如果'运行内存' 存在于 th 中时
                            if '运行内存：' in table_th:
                                # index函数找到 ‘运行内存’ 所在的下标，然后传入数组内获得ram的值
                                ram = table_tr[table_th.index('运行内存：')]
                                # 同理
                                rom = table_tr[table_th.index('机身内存：')]
                            # 然而这样获得的ram、rom普遍存在问题：
                            # 当手机是苹果的一些旧型号手机，ram为：不详
                            # 有些手机的ram 为 XG以下
                            # 有些手机的ram 为 4G/6G
                            # 有些手机的表格根本就没有 ram
                            # rom同理
                            # 下面的代码是对混扎的数据进行处理
                            # 如果 表格的 ram 中带有 ‘/’
                            if '/' in ram:
                                # 用split函数对'/'字符进行分割，并获得头个元素赋值到ram
                                ram = str(ram).split('/')[0]
                            # 或者（运行这一步说明没有斜杠）ram中带有‘不详’，‘以下’ 或者 ‘iphone’ '飞利浦' 在名字中时
                            elif '不详' in ram or '以下' in ram or '飞利浦' in name or 'iPhone' in name:
                                # 为什么不能一开始就保持默认赋值‘其他’？ 因为他们都是在表格内存在值的，且值不为其他
                                ram = '其他'
                            # 通过re表达式查找 商品名字中带有
                            # 内存信息的元素： 同样数据过于复杂：
                            # 可能的形式：
                            # (1)6GB + 128GB
                            # (2)6G + 128GB
                            # (3)6+ 128G
                            # (4)6+128GB
                            # (5)64GB
                            # (6)说明信息都没有
                            # 第一个字符匹配0-9 长度为0或1
                            # 第二个字符匹配G 长度为0或1
                            # 第三个字符匹配+号 要加斜杠 长度为0或1
                            # 第四个字符匹配0-9号 长度为1至n
                            # 第五个字符匹配G 长度为1
                            # 第六个字符匹配B 长度为0到1
                            if re.search('[0-9]?G?\+?[0-9]+GB?', name):
                                # 获得匹配的字符串
                                result = re.search('[0-9]?G?\+?[0-9]+GB?', name)[0]
                                # print(result)
                                # 如果匹配的ram + rom中带有 + 号
                                if '+' in result:
                                    # 按加号进行分割，并把第一个元素赋给ram
                                    ram = str(result).split('+')[0]
                                    # 按加号进行分割，并把第二个元素赋给rom
                                    rom = str(result).split('+')[1]
                            # 为什么上面赋值了rom 下面还要赋值rom ?
                            # 因为有的手机的名字中不带内存和硬盘的
                            # 比如：A7X4G全面屏手机AI智慧美颜拍照手机分期语音唤醒
                            if '/' in rom:
                                rom = str(rom).split('/')[0]
                            if '以下' in rom:
                                rom = '其他'
                            # 补全ram 和 rom
                            ram = completion_ram(ram)
                            rom = completion_ram(rom)
                            # print(ram , rom ,name, price , id , skuid , url , source )
                            # 直接插入ID池，有相同ID不同URL的就进行更新。
                            # 判断是否有ID相同的数据段，有就更新，没有就插入
                            cursor.execute('select * from t_id_pool where id = "%s" ' % (id))
                            # 获得的元组相当于java中的list,获得元组中的第一个元素(id)
                            if cursor.rowcount == 1:
                                # 第三个元素是url
                                data_base_url = cursor.fetchone()[2]
                                # 如果当前的url和数据库的url不一样，那么需要更新
                                if data_base_url != url:
                                    # print(data_base_url)
                                    # 注意这只是修改了某个字段
                                    # 更新了t_id_pool中的url，item表中的url也需要跟着改
                                    cursor.execute(
                                        'update t_id_pool set url = "%s" where id = "%s"' % (url , id))
                                    cursor.execute(
                                        'update t_item set url = "%s" where id = "%s"' % (url , id))
                                    mysql_db.commit()
                            # rowcount 为 0 说明数据库中没有该ID，需要去插入到ID池和ITEM表，并同时对group字段进行赋值。
                            elif cursor.rowcount == 0:
                                # 插入到ID池
                                cursor.execute(
                                    'insert into t_id_pool (id, skuid, url, source) values( "%s",  "%s" , "%s" , "%s" )' % (
                                    id, skuid, url, source))
                                mysql_db.commit()
                                # 插入完ID池再插入item表，由于item中有group_i字段，需要找一个组的数据。
                                # 查一下，旧的model加上ram加上rom从group表中筛选是否存在
                                # 荣耀8Xmax 4GB 128GB本来没有
                                cursor.execute('select * from t_group where model = "%s" and ram = "%s" and rom = "%s" ' % (temp_x , ram , rom))

                                # 如果为1说明已经有这个组了
                                if cursor.rowcount == 1:
                                    # 获得第0个属性，ID
                                    group_id = cursor.fetchone()[0]
                                    # print(group_id)
                                    # 插入到item表
                                    cursor.execute(
                                        'insert into t_item (id, name, url, source , group_id) values( "%s",  "%s" , "%s" , "%s" , "%s")' % (
                                            id, name, url, source , group_id))
                                    mysql_db.commit()
                                # 如果为0，说明还没有这个组
                                elif cursor.rowcount == 0 and '未知' not in ram:
                                    # 查找brand
                                    cursor.execute(
                                        'select brand from t_group where model = "%s" ' % (temp_x))
                                    brand = cursor.fetchone()[0]
                                    # 创建一个组，再插入item
                                    cursor.execute(
                                        'insert into t_group (name, ram , rom, model ,brand ,default_id ) values( "%s",  "%s" , "%s" , "%s" , "%s" , "%s")' % (
                                            name, ram , rom , temp_x , brand , id))
                                    mysql_db.commit()
                                    cursor.execute(
                                        'insert into t_item (id, name , url, source ,group_id ) values( "%s",  "%s" , "%s" , "%s" , "%s")' % (
                                            id , name , url , source , group_id))
                                    mysql_db.commit()
                                    # 在mysql中插入了组，同理也要在mongodb中插入组
                                    phone = db['phone'].find_one({'model':temp_x})
                                    # 通过型号获得手机后，需要修改的字段有 _id, id , name , url ,ram ,rom
                                    phone['_id'] = id
                                    phone['id'] = id
                                    phone['name'] = name
                                    phone['url'] = url
                                    phone['ram'] = ram
                                    phone['rom'] = rom
                                    db['phone'].insert(phone)
                            #保存 价格 和 活动：
                            # 价格
                            price_value = {
                                'price_value': price,
                                'date': date
                            }
                            save_to_mongo_as_a_array('prices', id, id, 'prices',price_value)
                            # 活动
                            #print(url)
                            header_promotion['referer'] = url
                            promotion_response = requests.get('https://gensvr.vip.com/coupon/getAll?bid=' + y['brand_id'] + '&mid=' + y['product_id'],
                                                     headers=header_promotion)
                            print(promotion_response.text)
                            promotion_obj = json.loads(promotion_response.text)
                            if promotion_obj['coupons'] != []:
                                sale_promotion = {
                                    'sale_promotion_value': [promotion_obj['coupons'][0]['buy'] + '元券可领'],
                                    'date': date
                                }
                            else:
                                sale_promotion = {
                                    'sale_promotion_value': [],
                                    'date': date
                                }
                            # 有没有活动都需要插入
                            save_to_mongo_as_a_array('sale_promotions', id, id, 'sale_promotion', sale_promotion)
                            # 提交到数据库执行
                            mysql_db.commit()
        except Exception as e:
            print(e)
    cursor.execute('select model, default_id from t_group where default_id like "%vip%";')
    for x in cursor.fetchall():
        # 型号
        print(x[0])
        # id
        print(x[1])
        phone = db['phone'].find_one({'model': x[0]})
        print(phone)
        res = parse_as_opinion_and_impress(str(phone['_id']).replace('jd', ''), date)
        print(res['opinion'].__dict__)
        save_to_mongo_as_a_array('opinions', x[1], x[1], 'opinion_value',
                                 res['opinion'].opinion)
        print('{\'id\': \'' + str(x[1]) + '\', \'impress\': ' + str(
            res['impress'].impress) + '}')
        save_to_mongo_as_a_array('impresses', x[1], x[1], 'impress_value',
                                 res['impress'].impress)
        res['impress'].impress.clear()


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


crawl_detail_page_save_as_mongo()