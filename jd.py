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

# index页进行的筛选：keyword : 自营手机 ， 商品类别 ： 手机 ， 京东物流 : true , 仅显示有货 : true , 地理位置  : #
# index页的连接头
index_page_head = 'https://search.jd.com/search?keyword=%E8%87%AA%E8%90%A5%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&cid2=653&cid3=655&stock=1&wtype=1&page='
# index页的链接尾
index_page_tail = '&s=338&click=3'
# 详情页的链接头
detail_page_head = 'https://item.jd.com/'
# 详情页的链接尾
detail_page_tail = '.html'

# 连接mongodb数据库
client = pymongo.MongoClient('localhost')
# 连接到jd数据库
db = client['jd']

# 打开mysql数据库连接
mysql_db = pymysql.connect("localhost", "root", "root", DB_NAME)
# 使用cursor()方法获取操作游标
cursor = mysql_db.cursor()


crawl_day_in_week = [0, 1, 2, 3, 4, 5, 6]

# 用来装载没有找到的商品
not_found_list = []


# 去除括号的函数，用于数据清洗。
def remove_brackets(str):
    str = re.sub(u"\\(.*?\\)|\\（.*?）", "", str)
    return str

# 爬取主页的商品链接，并将链接字符串保存到文件 ids_jd中
def crawl_list_page_save_as_ids():
    # 打开Chrome浏览器
    driver = webdriver.Chrome()
    # 将浏览器窗口设置为最大值
    driver.maximize_window()
    # 将主页的头和尾进行拼接，打开第一页
    driver.get(index_page_head + '1' + index_page_tail)
    # 通过xpath将 页数 爬取
    page_number = driver.find_element_by_xpath('//div[@id="J_bottomPage"]/span[@class="p-skip"]/em/b').text
    # 存放商品ID的数组
    links = []
    # 打印共有多少页
    print(page_number)
    for i in range(1, int(page_number)+1):
        # 2*i-1获得超链接中的page参数（京东超链接的坑）
        driver.get(index_page_head + str(2*i-1) + index_page_tail)
        # 通过xpath表达式获得了logo当中的a标签（可以用来拖下来）
        btn = driver.find_element_by_xpath('//div[@id="logo-2014"]/a')
        # 下拉
        pulllowfunc(btn, 20)
        time.sleep(1)
        pulllowfunc(btn, 20)
        time.sleep(1)
        # 传入浏览器当前的源代码，获得一个选择器对象。
        selector = Selector(text=driver.page_source)
        # 通过xpath获得JD的skuid并添加到links
        links = links + selector.xpath('//li[@class="gl-item"]//li[@class="ps-item"]/a/img/@data-sku').extract()
    # 调用函数保存IDS到指定文件。
    # save_info_print('./IDS_JD', links)
    save_ids_to_mysql(DB_NAME, 't_id_pool', links, '京东')
    # 关闭浏览器
    driver.close()


# 详情页爬取
def crawl_detail_page_save_as_mongo():
    # 获得当前时间
    # 结构 time.struct_time(tm_year=2019, tm_mon=1, tm_mday=8, tm_hour=15, tm_min=50, tm_sec=27, tm_wday=1, tm_yday=8, tm_isdst=0) wday ： 0到 6
    localtime = time.localtime(time.time())
    # 获得当前的时间，并将它转换成这种格式 ： 2019-01-08
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    # 重试5次
    for retry in range(0, 5):
        if retry == 0:
            # 如果是重试的第一次，那么从IDS_JD文件中获得IDS并赋值到links
            # links = readFile('./IDS_JD')
            # 如果是重试的第一次，那么数据库中获得IDS并赋值到links
            cursor.execute('select skuid from t_id_pool where source = %s;'
                           , ['京东'])
            # 读出来的是一个二维数组，需要把二维数组中每个元素的第一个元素拿出，就形成id了。
            links = [x[0] for x in cursor.fetchall()]
        else:
            # 如果是不是重试的第一次，那么从IDS_JD_REST文件中获得IDS并赋值到links
            links = readFile('./IDS_JD_REST')
        # 打印重试的次数
        print('retry times :' + str(retry))
        # 打印IDS数组
        print(links)
        # 清空没有找到的IDS
        not_found_list.clear()
        # 循环从IDS中获得ID，并进行相应的操作
        for x in links:
            try:
                # 如果jd数据库中没有找到这个ID的商品那么，就进行下面的操作
                # if db['phone'].find_one({'id': 'jd' + x}, {'id': 1}) is None:
                # 将详情页的头和尾和ID进行拼接，并设置请求头，发送请求并获得响应
                response = requests.get(detail_page_head + x + detail_page_tail, headers=headers)
                #print(driver.page_source) # 打印网页源代码
                # 将响应的文本传入，获得一个选择器对象。
                selector = Selector(text=response.text)
                # 传入手机的ID和选择器对象，对详情页的手机信息进行解析，获得一个手机对象。
                phone = parse_as_phone(x, selector)
                # 打印手机对象
                print(phone.__dict__)
                # 执行sql语句，从mysql group表中按型号、内存、硬盘来查找是否有结果
                cursor.execute('select * from t_group where ram = %s and rom = %s and model = %s;'
                               , [phone.ram, phone.rom, phone.model])
                # 有结果的话（结果为1），说明已经分配到组了，
                ret1 = cursor.rowcount
                # print(ret1)
                # 数据库中没有该组：
                if ret1 is 0:
                    # print('没有组' + phone.id)
                    # 插入组，default_id是第一个进组的item
                    cursor.execute('insert into t_group (name, ram, rom, model, brand, default_id) values( "%s",  "%s" , "%s" , "%s" , "%s" , "%s" )' % (phone.name, phone.ram , phone.rom , phone.model , phone.brand , phone.id))
                    # 提交到数据库执行
                    mysql_db.commit()
                    # 按道理来讲，mysql和mongodb的组是一致的，保存该组到mongodb
                    db['phone'].insert(phone.__dict__)
                # 有没有组都需要对item表进行插入
                # 从group表中获得组的ID
                cursor.execute('select id from t_group where ram = %s and rom = %s and model = %s;'
                               , [phone.ram, phone.rom, phone.model])
                group_id = cursor.fetchone()[0]
                # print(group_id)
                # 从item表中按ID获得结果
                cursor.execute('select id from t_item where id = %s;'
                               , [phone.id])
                ret2 = cursor.rowcount
                # 结果不为0，说明item已经插入过了
                # 结果为0，说明item没有插入
                if ret2 is 0:
                    # 插入item
                    cursor.execute('insert into t_item (id, name, url, source , group_id) values ( "%s",  "%s" , "%s" , "%s" , "%s")' % (phone.id , phone.name , phone.url , '京东' , group_id))
                    mysql_db.commit()
                # 京东价格爬虫
                price = parse_as_price(x, date)
                print(price.__dict__)
                # tableName : prices , _id : _id , id : id , arrayName : prices , arrayValue: price.price
                save_to_mongo_as_a_array('prices', price._id, price.id,'prices', price.price)
                # 京东活动爬虫
                sale_promotion = parse_as_sale_promotion(x, date)
                print(sale_promotion.__dict__)
                save_to_mongo_as_a_array('sale_promotions', sale_promotion._id, sale_promotion.id, 'sale_promotion', sale_promotion.sale_promotion)
            except Exception as e:
                # 如果发生错误则回滚
                mysql_db.rollback()
                not_found_list.append(x)
                print(str(x) + ' : ' + str(e))
        writeFile('./IDS_JD_REST',not_found_list)

        # parse_as_opinion_and_impress()
    # 印象标签和好评率就不再retry了
    # cursor.execute('select skuid from t_id_pool where source = %s;'
    #                , ['京东'])
    # links = [x[0] for x in cursor.fetchall()]
    # 从group表中获得所有以jd开头的skuid
    cursor.execute('select default_id from t_group where default_id like %s;'
                   , ['%jd%'])
    # 读出来的是一个二维数组，需要把二维数组中每个元素的第一个元素拿出，就形成id了。
    links = [x[0].replace('jd', '') for x in cursor.fetchall()]
    print(links)
    for x in links:
        res = parse_as_opinion_and_impress(x, date)
        print(res['opinion'].__dict__)
        save_to_mongo_as_a_array('opinions', res['opinion']._id, res['opinion'].id, 'opinion_value',
                                 res['opinion'].opinion)
        print('{\'id\': \'' + str(res['impress'].id) + '\', \'impress\': ' + str(res['impress'].impress) + '}')
        save_to_mongo_as_a_array('impresses', res['opinion']._id, res['impress'].id, 'impress_value',
                                 res['impress'].impress)
        res['impress'].impress.clear()



# 传入手机的ID和选择器，解析回一个手机对象。
def parse_as_phone(x, selector):
    # 构造函数，定义一个手机对象
    phone = Phone()
    # 1. id
    # 设置手机对象的_id 和 id 都是 jd + id
    phone._id = 'jd' + x
    phone.id = 'jd' + x
    # 2. name
    # 获得详情页中的商品名字，这里源代码有多余的空格，需要去清洗一下
    name = selector.xpath('//div[@class="sku-name"]//text()').extract()
    # 由于上面你的extract函数是获得了一个数组，需要去获取数组中最后得元素，并通过strip函数去除空格和换行符号
    phone.name = name[len(name)-1].strip()
    # description 和 extra_message 删除算了。
    # phone.extra_message = remove_brackets(str(phone.name)).replace(' ','').lower()
    # 3.url
    # 拼接url
    phone.url = detail_page_head + x + detail_page_tail
    # 4 thumb_pic
    # 通过xpath获得所有的缩略图的路径的数组，并通过for循环将数组内的每一个对象都设置为长度和宽度为430的图片
    phone.thumb_pic = [str(z).replace('54x54', '430x430') for z in
        selector.xpath('//div[@id="spec-list"]/ul/li/img/@src').extract()]
    # 5 detail_pic
    # 通过请求连接，并进行解析，获得详情图片
    # 首先获得请求的响应
    response = requests.get('https://cd.jd.com/description/channel?skuId='+x+'&mainSkuId='+x+'&cdn=2',headers = headers)
    # 将text传入，通过json转换成一个对象
    obj = json.loads(response.text)
    # 如果对象的content属性不为None
    if obj['content'] != None:
        # 把content属性中的内容传进选择器对象2中
        selector2 = Selector(text=obj['content'])
        # 有两种类型的详情图片，下面是第一种
        # 通过正则表达式匹配 “background-image:url\((.*)\)}” ，其中\(匹配 ( ,  (.*) 贪婪匹配内容
        phone.detail_url = selector2.xpath('.').re('background-image:url\((.*)\)}')
        # 有两种类型的详情图片，下面是第二种，数组的添加
        phone.detail_url = phone.detail_url + selector2.xpath('.').re('data-lazyload="(.*?)"')
    # 6 video_url
    # 获得id为v-video的div的 data-vu 的属性值，如：13224757，并赋值到vid
    vid = selector.xpath('//div[@id="v-video"]/@data-vu').extract_first()
    # 设置没有视频时的内容
    phone.video_url = '暂无信息'
    if vid != None:
        # 当vid不为空的时候，发送请求获得json数据，转换成obj对象
        response = requests.get('https://c.3.cn/tencent/video_v3?vid='+vid,
                                headers=headers)
        obj = json.loads(response.text)
        if obj != {}:
            # 当obj对象不为空时，将playUrL属性赋值到video_url中
            phone.video_url = obj['playUrl']
    # 7 hot_spot
    # 通过xpath 和 正则匹配 来匹配热点
    hot_spot = selector.xpath('//ul[@class="parameter2 p-parameter-list"]').re('热点：(.*?)</li>')
    phone.hot_spot = []
    # 当热点结果数组长度不为0时。
    if len(hot_spot) != 0 :
        # 把数组第一个元素按‘，’分割并赋值到hot_spot中
        phone.hot_spot = hot_spot[0].split('，')
    # 规格与包装目录下：
    # 8 brand model cpu ram rom memory_card max_men_sup screen_size resolution f_camera r_camera battery figer
    # 获得属性的名称的数组
    table_th = selector.xpath('//div[@data-tab="item"]//dl/dt/text()').extract()
    # 获得属性的名称的值的数组
    table_tr = selector.xpath('//div[@data-tab="item"]//dl/dd[not(@class="Ptable-tips")]/text()').extract()
    # 表格中存在并且是我需要的属性
    property_i_need = ['品牌', '型号', 'CPU型号', 'RAM', 'ROM', '存储卡', '最大存储扩展容量', '主屏幕尺寸（英寸）','分辨率','前置摄像头','后置摄像头','电池容量（mAh）','指纹识别']
    # 统一赋值为默认值 ‘暂无信息’
    phone.r_camera = phone.f_camera = phone.screen_size = phone.battery = phone.pack_list = phone.brand = phone.model = phone.ram = phone.rom = phone.cpu = phone.memory_card = phone.max_mem_sup = phone.resolution = phone.figer = '暂无信息'
    # 按循环从0到th的长度减一
    for i in range(0, len(table_th)):
        # 如果属性的名称在我需要的属性当中时：
        if table_th[i] in property_i_need:
            if table_th[i] == '品牌':
                phone.brand = remove_brackets(table_tr[i]).replace(' ','')
            #if table_th[i] == '型号':
            #    phone.model = remove_brackets(str(table_tr[i])).replace(' ','')
            if table_th[i] == 'RAM':
                phone.ram = table_tr[i].replace(' ','')
            if table_th[i] == 'ROM':
                phone.rom = table_tr[i].replace(' ','')
            if table_th[i] == 'CPU型号':
                phone.cpu = remove_brackets(table_tr[i]).replace(' ','')
            if table_th[i] == '存储卡':
                phone.memory_card = table_tr[i]
            if table_th[i] == '最大存储扩展容量':
                phone.max_mem_sup = table_tr[i].replace(' ','')
            if table_th[i] == '分辨率':
                # 分辨率统一用*号
                phone.resolution = remove_brackets(table_tr[i]).replace('x','*')
            if table_th[i] == '指纹识别':
                phone.figer = table_tr[i]
            # if table_th[i] == '包装清单':
            #     phone.pack_list = table_tr[i]
            if table_th[i] == '电池容量（mAh）':
                # 电池容量统一 去括号加去mAh , 4000mAh （typ）/3900mAh (min) -》  3340/3240
                phone.battery = remove_brackets(table_tr[i]).replace('mAh','')
            if table_th[i] == '主屏幕尺寸（英寸）':
                # 屏幕尺寸 统一 5.99英寸 -》 5.99
                phone.screen_size = remove_brackets(str(table_tr[i])).replace('英寸','').replace('”','')
            if table_th[i] == '前置摄像头':
                # 前置摄像头 后置摄像头 统一 去掉像素两字
                phone.f_camera = remove_brackets(str(table_tr[i])).replace('像素','').replace('；',' ').replace('+',' ')
            if table_th[i] == '后置摄像头':
                phone.r_camera = remove_brackets(str(table_tr[i])).replace('像素','').replace('；',' ').replace('+',' ')
    pack_list = ''
    # pack_list有两种
    if selector.xpath('//div[@class="package-list"]/p/text()').extract():
        pack_list = str(selector.xpath('//div[@class="package-list"]/p/text()').extract()[0]).replace('\n','')
    else:
        pack_list = str(selector.xpath('//div[@class="package-list"]//text()').extract()[3]).replace('\n','')
    phone.pack_list = pack_list
    if phone.brand == ('暂无信息' or '其他'):
        phone.brand = remove_brackets(str(selector.xpath('//ul[@id="parameter-brand"]/li/@title').extract_first()))
    # phone.description = ''
    phone.model = selector.xpath('//ul[@class="parameter2 p-parameter-list"]').re('商品名称：(.*?)</li>')[0].replace(' ','').lower()
    return phone


# 京东价格API：
# https://c0.3.cn/stock?skuId=8245366&cat=9987,653,655&area=1_72_2799_0&extraParam={%22originid%22:%221%22}
def parse_as_price(x, date):
    price = Price()
    price_value = ''
    # 发送请求
    # response = requests.get('http://p.3.cn/prices/mgets?skuIds=' + x + '&pdtk=&pduid')
    response = requests.get('http://p.3.cn/prices/mgets?skuIds=J_' + x)
    # [{"op": "2199.00", "m": "9999.00", "id": "J_100000015158", "p": "1999.00"}]
    # 其中 op是指原价， m 不知道是什么 ， p是现价 ， id是 ID.
    # 响应体中不包含error
    if 'error' not in response.text:
        obj = json.loads(response.text)
        # 不为空的时候
        if obj != {}:
            # print((obj[0]['p']))
            # 京东为-1时代表无货
            if obj[0]['p'] == '-1.00':
                price_value = '无货'
            else:
                price_value = obj[0]['p'] #+ '(有货)'
    # price.id =  str(random.randint(10000,99999)) + 'jd' + x
    price.id = 'jd' + x
    price._id = 'jd' + x
    price.price = {
        'price_value': price_value,
        'date': date
    }
    return price


# 京东活动爬虫方法，传入skuid和时间date
def parse_as_sale_promotion(x , date):
    # 构造函数
    sale_promotion = SalePromotion()
    # 创建一个list来存储活动
    promotion_list = []
    # 京东活动API：需要注意的属性：quan(买了以后返回什么券), prom.tags(赠品，限购) , prom.pickOneTag(满减) , skuCoupon(满减)
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
        if obj['quan'] != {}:
            promotion_list.append(obj['quan']['title'])
        #print(promotion_list)
        sale_promotion._id = 'jd' + x
        sale_promotion.id = 'jd' + x
        sale_promotion.sale_promotion = {
            'sale_promotion_value' : promotion_list,
            'date' : date
        }
        return sale_promotion


# 京东好评率和印象标签的API，应该要分到组下面
# https://sclub.jd.com/comment/productPageComments.action?&productId=7834054&score=0&sortType=5&page=0&pageSize=10
# 需要注意的属性： hotCommentTagStatistics:印象标签,productCommentSummary:好评率, comments : 评论
# 传入组的ID和时间
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





# schedule.every().day.at("14:48").do(crawl_list_page_save_as_ids)
# schedule.every().day.at("14:49").do(crawl_detail_page_save_as_mongo)
# while True:
#     schedule.run_pending()
    # time.sleep(1)



#crawl_list_page_save_as_ids()
crawl_detail_page_save_as_mongo()
