from file import save_ids_to_mysql
import pymongo

links = ['100000015158','100000015166']
# save_ids_to_mysql('test' , 't_id_pool' , links , '京东')

# 连接mongodb数据库
client = pymongo.MongoClient('localhost')
# 连接到jd数据库
db = client['jd']
result = db['prices'].find_one({'id' : 'jd100000015158'},{'prices' : {'$slice' : -1}})
print(result)