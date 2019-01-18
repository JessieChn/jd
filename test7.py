import requests
import pymysql
header_promotion = {
    'accept':'*/*',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'zh-CN,zh;q=0.9',
    'cookie':'vip_province=104104; vip_province_name=%E5%B9%BF%E4%B8%9C%E7%9C%81; vip_city_name=%E4%B8%9C%E8%8E%9E%E5%B8%82; vip_city_code=104104119; vip_wh=VIP_NH; vip_ipver=31; mars_pid=0; _smt_uid=5c340da8.1d077571; vip_address=%257B%2522pid%2522%253A104104%252C%2522pname%2522%253A%2522%255Cu5e7f%255Cu4e1c%255Cu7701%2522%252C%2522cid%2522%253A104104119%252C%2522cname%2522%253A%2522%255Cu4e1c%255Cu839e%255Cu5e02%2522%252C%2522did%2522%253A104104119001%252C%2522dname%2522%253A%2522%255Cu839e%255Cu57ce%255Cu533a%2522%252C%2522sid%2522%253A%2522%2522%252C%2522sname%2522%253A%2522%2522%257D; VipUINFO=luc%3Aa%7Csuc%3Aa%7Cbct%3Ac_new%7Chct%3Ac_new%7Cbdts%3A0%7Cbcts%3A0%7Ckfts%3A0%7Cc10%3A0%7Crcabt%3A0%7Cp2%3A0%7Cp3%3A1%7Cp4%3A0%7Cp5%3A1; user_class=a; mars_sid=e36946cf857b59dd2240a993a1c785e7; visit_id=444A397853656C81EA329111739C1FCB; __guid=136073383.1637109775761122000.1547528597452.4211; vipte_viewed_=525768804348867%2C538776774862083%2C549970002338846%2C549970002347038%2C541293914691264; _jzqco=%7C%7C%7C%7C%7C1.2035712575.1546915240937.1547528883169.1547529342592.1547528883169.1547529342592..0.0.211.211; mars_cid=1546915238563_28adf14b5bb0834a92b98390b55da69e; monitor_count=5',
    'referer':'https://detail.vip.com/detail-100050400-541293914691264.html',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
# 打开数据库连接
db_mysql = pymysql.connect("localhost", "root", "root", "test")

import pymongo
# 连接mongodb数据库
client = pymongo.MongoClient('localhost')
# 连接到jd数据库
db = client['jd']

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 从group表中获得 distinct的 model
cursor.execute('select url  from t_item where source = "唯品会";')
# 读出来的是一个二维数组，需要把二维数组中每个元素的第一个元素拿出，就形成id了。
links = [x[0] for x in cursor.fetchall()]
for x in links:
    print(x)
    result = str(x).split('-')
    bid = result[1]
    mid = str(result[2]).replace('.html' , '')
    # print(bid + mid)
    header_promotion['referer'] = x
    response = requests.get('https://gensvr.vip.com/coupon/getAll?bid='+ bid +'&mid=' + mid,headers = header_promotion)
    print(response.text)
# accept:*/*
# accept-encoding:gzip, deflate, br
# accept-language:zh-CN,zh;q=0.9
# cookie:vip_province=104104; vip_province_name=%E5%B9%BF%E4%B8%9C%E7%9C%81; vip_city_name=%E4%B8%9C%E8%8E%9E%E5%B8%82; vip_city_code=104104119; vip_wh=VIP_NH; vip_ipver=31; mars_pid=0; _smt_uid=5c340da8.1d077571; vip_address=%257B%2522pid%2522%253A104104%252C%2522pname%2522%253A%2522%255Cu5e7f%255Cu4e1c%255Cu7701%2522%252C%2522cid%2522%253A104104119%252C%2522cname%2522%253A%2522%255Cu4e1c%255Cu839e%255Cu5e02%2522%252C%2522did%2522%253A104104119001%252C%2522dname%2522%253A%2522%255Cu839e%255Cu57ce%255Cu533a%2522%252C%2522sid%2522%253A%2522%2522%252C%2522sname%2522%253A%2522%2522%257D; VipUINFO=luc%3Aa%7Csuc%3Aa%7Cbct%3Ac_new%7Chct%3Ac_new%7Cbdts%3A0%7Cbcts%3A0%7Ckfts%3A0%7Cc10%3A0%7Crcabt%3A0%7Cp2%3A0%7Cp3%3A1%7Cp4%3A0%7Cp5%3A1; user_class=a; mars_sid=e36946cf857b59dd2240a993a1c785e7; visit_id=444A397853656C81EA329111739C1FCB; __guid=136073383.1637109775761122000.1547528597452.4211; vipte_viewed_=525768804348867%2C538776774862083%2C549970002338846%2C549970002347038%2C541293914691264; _jzqco=%7C%7C%7C%7C%7C1.2035712575.1546915240937.1547528883169.1547529342592.1547528883169.1547529342592..0.0.211.211; mars_cid=1546915238563_28adf14b5bb0834a92b98390b55da69e; monitor_count=5
# referer:https://detail.vip.com/detail-100050400-541293914691264.html
# user-agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36