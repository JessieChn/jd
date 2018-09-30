# import re
# def remove_brackets(str):
#     str = re.sub(u"\\(.*?\\)|\\（.*?）", "", str)
#     return str
#
# #s="我是一个人(中国人)aaa[真的]bbbb{确定}"
# #a = re.sub(u"\\(.*?\\)", "", s)
# s = '三星（SAMSUNG）'
# s = remove_brackets(s)
# print(s)
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["jd3"]
mycol = mydb["phone"]
# result = mycol.aggregate([{'$match':{'id':{"$regex":'6035574'}}},{'$project': {"name": 1}}])
# result = mycol.aggregate([{'$sample':{'size': 20}},{'$project': {"name": 1}}])
# result = mycol.aggregate([{'$sample':{'size': 20}},{'$project': {"name": 1}}])
# for x in result:
#     print(x)

mycol2 = mydb["prices"]
# for x in mycol2.find(
#         {
#             'prices':{
#                 '$elemMatch':{
#                     'price_value':{
#                         '$regex':'有货'
#                     }
#                 }
#             }
#         },
#         {
#             'prices':{
#                 "$slice":-1
#             }
#         }):
#     print(x)
result = mycol2.aggregate([
    {'$match':{'prices':{'$elemMatch':{'price_value':{'$regex':'.'},'date':'2018-09-27'}}}},  #任意一天有货就可以上
    #{'$sample': {'size': 20}},
    {'$project':{'id':1,'price':{'$slice':['$prices.price_value',-1]}}},  #注意这个price_value
    {'$sort':{'id':1}}, #注意顺序，要先sort再skip
    {'$skip':1},
    {'$limit':10},
])
l1 = []
for x in result:
    obj = dict(mycol.find_one({'_id':x['_id']},{'_id':1,'name':1,'ram':1,'rom':1,'source':1,'thumb_pic':{'$slice':1}}))
    obj.update(dict(x).items())
    d3 = {}
    d3.update(dict(x).items())
    d3.update(obj.items())
    l1.append(d3)

print(l1)

#y = [x['_id'] for x in result]
#print(y)#找出手机

# result2 = mycol.find({'_id':{'$in':y}},{'_id':1,'name':1,'ram':1,'rom':1,'source':1,'thumb_pic':{'$slice':1}})
# for z in result2:
#     print(z)



# result = mycol2.aggregate([
#     {'$sample': {'size': 1000}}
#     #,{'$project':{'id':1,'newPrice':{'$arrayElemAt':['$prices.price_value',-1]}}}  #注意这个price_value
#     ,{'$project':{'id':1,'newPrice':{'$slice':['$prices.price_value',-5]}}}  #注意这个price_value
# ])
# for x in result:
#     print(x)
    #if x['newPrice'] == '无货或者本地区暂不销售':
    #    mycol2.delete_one({'id':x['id']})

# for x in mycol.find({ "_id": { "$regex": "jd5438529" }}, {"_id": 1, "name": 1,"ram":1,"rom":1,"source":1,"thumb_pic":{"$slice":-1}}):
#     print(x)
# for x in mycol.find({}, {"_id": 1, "name": 1,"ram":1,"rom":1,"source":1,"thumb_pic":{"$slice":-1}}):
#     print(x)