import pymongo

if __name__ == '__main__':
    print("welcome to pymongo")
    client= pymongo.MongoClient("mongodb://localhost:27017/")
    print(client)
    db = client['NikChat']
    collection = db['friendsystem_friendrequest']
    one = collection.find_one({"is_active": True})
    print(one['is_active'])