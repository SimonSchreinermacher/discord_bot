import json

#This method holds the default values for all configuration options
#It is used for initializing the config value and restoring entries, if they get deleted from the config.json
def defaultConfig():
    #DO NOT EDIT THIS DICTIONARY WHILE IN PRODUCTION
    data = {
        
    }
    return data

def initConfig():
    data = defaultConfig()
    with open("config.json", "w+") as jsonfile:
        json.dump(data, jsonfile, indent = 4)

def loadConfigEntries():
    data = {}
    try:
        with open("config.json", "r") as jsonfile:
            data = json.load(jsonfile)
            jsonfile.close()
        return data
    except:
        print("Config not initialized yet!")

def getFromConfig(entry):
    data = loadConfigEntries()
    if(data != None):
        try:
            #If entry exists in config
            return data[entry]
        except:
            #Entry does not exist in config, check if it exists in default configuration
            print("Not found in config, trying to restore from default config...")
            defaultData = defaultConfig()
            try:
                #If entry does not exist in config, but exists in default configuration (happens by manually deleting entries from config.json)
                changeConfigEntry(entry, defaultData[entry])
                print("Argument was not found in config, but in default configuration, restored the entry in config.json to its default value")
                return defaultData[entry]
            except:
                #If entry neither exists in config, nor default configuration, in this case, the given entry argument is not a valid configuration option 
                print("Not found in default config, this configuration option does not exist")
                return ""

def changeConfigEntry(entry, newvalue):
    data = loadConfigEntries()
    if(data != None):
        defaultData = defaultConfig()
        if(entry in defaultData.keys()):
            data[entry] = newvalue
            with open("config.json", "w") as jsonfile:
                json.dump(data, jsonfile, indent=4)

changeConfigEntry("s", "t")