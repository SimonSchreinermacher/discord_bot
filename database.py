import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
discord_database = client["discord_database"]

user_collection = discord_database["users"]

def find_by_username(username, tag="ignore"):
    if(tag == "ignore"):
        results = list(user_collection.find({"username" : username}))
        return results
    else:
        results = list(user_collection.find({"username" : username, "tag" : tag}))
        return results

def find_all_users():
    results = list(user_collection.find())
    return results

def add_to_user_collection(username, tag, joined_at):
    entry = {"username" : username, "tag" : tag, "Joined at": joined_at, "messagesSent" : 0}
    identical_users = find_by_username(username, tag)
    if(len(identical_users) == 0):
        user_collection.insert(entry)

def delete_from_users(username, tag):
    entry = {"username" : username, "tag" : tag}
    user_collection.delete_one(entry)

def increment_message_count(username, tag):
    result = user_collection.find({"username" : username, "tag" : tag})
    for entry in result:
        old_message_count = entry["messagesSent"]
        update = { "$set" : {"messagesSent" : old_message_count + 1}}
        user_collection.update_one(entry, update)

def all_users_present(users):
    missing_users = []
    return_value = 1
    for user in users:
        (username, tag) = str(user).split('#')[0:2]
        if len(find_by_username(username, tag)) == 0:
            missing_users.append(user)
            return_value = 0
    return(return_value, missing_users)