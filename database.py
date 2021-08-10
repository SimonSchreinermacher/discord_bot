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

def addToUserCollection(username, tag, joined_at):
    entry = {"username" : username, "tag" : tag, "Joined at": joined_at, "messagesSent" : 0}
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

def allUsersPresent(users):
    missingUsers = []
    returnValue = 1
    for user in users:
        (username, tag) = str(user).split('#')[0:2]
        if len(findByUsername(username, tag)) == 0:
            missingUsers.append(user)
            returnValue = 0
    return(returnValue, missingUsers)