import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
discordDatabase = client["discord_database"]

userCollection = discordDatabase["users"]

def findByUsername(username, tag="ignore"):
    if(tag == "ignore"):
        results = list(userCollection.find({"username" : username}))
        return results
    else:
        results = list(userCollection.find({"username" : username, "tag" : tag}))
        return results

def findAllUsers():
    results = list(userCollection.find())
    return results

def addToUserCollection(username, tag):
    entry = {"username" : username, "tag" : tag, "messagesSent" : 0}
    identicalUsers = findByUsername(username, tag)
    if(len(identicalUsers) == 0):
        userCollection.insert(entry)

def deleteFromUsers(username, tag):
    entry = {"username" : username, "tag" : tag}
    userCollection.delete_one(entry)

def incrementMessageCount(username, tag):
    result = userCollection.find({"username" : username, "tag" : tag})
    for entry in result:
        oldMessageCount = entry["messagesSent"]
        update = { "$set" : {"messagesSent" : oldMessageCount + 1}}
        userCollection.update_one(entry, update)