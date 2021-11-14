import json

#This method holds the default values for all configuration options
#It is used for initializing the config value and restoring entries, if they get deleted from the config.json
def default_config():
    #DO NOT EDIT THIS DICTIONARY WHILE IN PRODUCTION
    data = {
        "bot_channel" : "bot-commands",
        "enable_command_stats" : True,
        "enable_command_listusers": True,
        "enable_command_cleardatabase": True
    }
    return data

#Returns 1, if config file exists and all entries are set, 0 if file exists, but keys are missing, -1 if file doesnt exist
def is_valid_config():
    default_data = default_config()
    try:
        with open("config.json", "r") as jsonfile:
            data = json.load(jsonfile)
            missing_keys = []
            return_value = 1
            for key in default_data.keys():
                if key not in data.keys():
                    missing_keys.append(key)
                    return_value = 0
            return (return_value, missing_keys)
    except:
        return (-1, list(default_data.keys()))

def init_config():
    data = default_config()
    with open("config.json", "w+") as jsonfile:
        json.dump(data, jsonfile, indent = 4)

def load_config_entries():
    data = {}
    try:
        with open("config.json", "r") as jsonfile:
            data = json.load(jsonfile)
            jsonfile.close()
        return data
    except:
        print("Config not initialized yet!")

def get_from_config(entry):
    data = load_config_entries()
    if(data != None):
        try:
            #If entry exists in config
            return data[entry]
        except:
            #Entry does not exist in config, check if it exists in default configuration
            print("Not found in config, trying to restore from default config...")
            default_data = default_config()
            try:
                #If entry does not exist in config, but exists in default configuration (happens by manually deleting entries from config.json)
                change_config_entry(entry, default_data[entry])
                print("Argument was not found in config, but in default configuration, restored the entry in config.json to its default value")
                return default_data[entry]
            except:
                #If entry neither exists in config, nor default configuration, in this case, the given entry argument is not a valid configuration option 
                print("Not found in default config, this configuration option does not exist")
                return ""

def change_config_entry(entry, new_value):
    data = load_config_entries()
    if(data != None):
        default_data = default_config()
        if(entry in default_data.keys()):
            data[entry] = new_value
            with open("config.json", "w") as jsonfile:
                json.dump(data, jsonfile, indent=4)