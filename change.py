import pymongo
import re

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.tanzhao
collection = db.school_copy1
collection1 = db.school1
#
# myquery = {"curriculum1": "10000"}
# newvalues = {"$set": {"alexa": "12345"}}
#
# collection.update_one(myquery, newvalues)

# 输出修改后的  "sites"  集合
for x in collection.find():
    for k in x:
        x[k] = re.sub('\s|[\r\n]', '', str(x[k]))
        x[k] = re.sub('见招生简章', '', str(x[k]))
    del x['_id']
    collection1.insert_one(x)
    # collection.update_many({"_id": x.get('_id')}, {"$set": x})

    # print(i)
    # z=collection.find_one({"_id": i.get('_id')})

# for x in collection.find():
#     print(x)
# x = collection.find()[0].get("curriculum1")
# print(re.sub('\s|[\r\n]', '', x))
# print(x)
