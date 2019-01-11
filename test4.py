import pymysql
import time
import datetime

localtime = time.localtime(time.time())
print(localtime)

date = datetime.datetime.now().strftime('%Y-%m-%d')
print(date)

# 打开数据库连接
db = pymysql.connect("localhost", "root", "root", "test")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 插入语句
# sql = """INSERT INTO t_group(name,
#          ram, rom, model, brand,default_id)
#          VALUES ('小米 红米Note5 全网通版 4GB+64GB 黑色 移动联通电信4G手机 双卡双待 拍照手机',
#                 '4GB',
#                 '64GB',
#                 '红米Note5',
#                 '小米',
#                 'jd6600258')"""
# sql = 'select * from t_group where ram = %s and rom = %s and model = %s;'
sql = 'insert into t_item (id, name, url, source , group_id) values ( "%s",  "%s" , "%s" , "%s" , "%s")' % ('JD123456','2','3','4' ,'5')

try:
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    # ret1 = cursor.rowcount
    # print(ret1)
except Exception as e:
    # 如果发生错误则回滚
    print(e)
    db.rollback()

# 关闭数据库连接
db.close()
# 插入数据
# 'insert into t_group (name, ram, rom, model, brand, default_id) values( "%s",  "%s" , "%s" , "%s" , "%s" , "%s" )' % (phone.name, phone.ram , phone.rom , phone.model , phone.brand , phone.id)
# 京东价格api , 莞城API
# https://c0.3.cn/stock?skuId=7003191&cat=9987,653,655&area=19_1655_4255_0
# 名字
# https://c.3.cn/recommend?callback=jQuery3880339&sku=100001726192&cat=9987%2C653%2C655&area=19_1655_4255_0&methods=suitv2&count=6&_=1547019611266
# 有没有货
# https://c0.3.cn/stocks?callback=jQuery4384413&type=getstocks&skuIds=8514625%2C6600260%2C6600262%2C6600258%2C6600236%2C6600238%2C7834054%2C6813717%2C6600214%2C8302186%2C6813715%2C6600240%2C8302184%2C8514651%2C6600216&area=19_1655_4255_0&_=1547022013426
# 6600262

# 下架商品 7293056
# 有没有货简洁版 https://c0.3.cn/stocks?type=getstocks&skuIds=7293056&area=19_1655_4255_0&_=1547022013426
# 下架商品API返回的是无货