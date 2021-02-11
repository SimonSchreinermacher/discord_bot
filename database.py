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

#def getMessageCount(username, tag="ignore"):
    #matches = findByUsername(username, tag)
    #results = []
    #for entry in matches:
    #    results.append([entry["username"], entry["tag"], entry["messagesSent"]])
    #return results

def mockData():
    entry1 = {"username" : "DuplicateUser", "tag" : "1000", "messagesSent" : 2}
    entry2 = {"username" : "DuplicateUser", "tag" : "1001", "messagesSent" : 14}
    userCollection.insert(entry1)
    userCollection.insert(entry2)
