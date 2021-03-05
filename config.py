import json

def initConfig():
    #No config options yet, will be added when new functionalities are added
    data = {

    }
    with open("config.json", "w+") as jsonfile:
        json.dump(data, jsonfile, indent = 4)

def loadConfigEntries():
    data = {}
    with open("config.json", "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
    return data

def getFromConfig(entry):
    data = loadConfigEntries()
    return data[entry]

def changeConfigEntry(entry, newvalue):
    data = loadConfigEntries()
    data[entry] = newvalue
    with open("config.json", "w") as jsonfile:
        json.dump(data, jsonfile, indent=4)