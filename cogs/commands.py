from discord.ext import commands
import os

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = self.bot.database
        self.config = self.bot.config
        
        
    def get_server(self):
        server_id = os.getenv("ID")
        return self.bot.get_guild(int(server_id))
    
    
    def get_all_users(self):
        server = self.get_server()
        return server.members
    
    
    def restore_entry(self, config_entry):
        default_data = self.config.default_config()
        try:
            default_value = default_data[config_entry]
            self.config.change_config_entry(config_entry, default_value)
            response = "Config entry " + config_entry + " changed to its default value " + str(default_value) + "\n"
        except:
            response = config_entry + " is not a valid config entry!"
        return response


    @commands.command()
    async def stats(self, ctx, *args):
        response = ""
        if(self.config.get_from_config("enable_command_stats") == True):
            #Own Stats
            if(len(args) == 0):
                (author, tag) = str(ctx.author).split("#")[0:2]
                results = self.database.find_by_username(author, tag)
                if(len(results) == 0):
                    response = "User " + author + " has not sent any messages on this server"
                else:
                    player_data = results[0]
                    response = "User " + author + "#" + tag + " has sent " + str(player_data["messagesSent"]) + " messages so far"
                    
            #Stats of other member
            elif(len(args) == 1):
                split_argument = str(args[0]).split("#")
                username = split_argument[0]
                
                #If tag is included in request
                if(len(split_argument) == 2):
                    tag = split_argument[1]
                    results = self.database.find_by_username(username, tag)
                    if(len(results) == 0):
                        response = "No users in database matching full username " + username + "#" + tag
                    else:
                        player_data = results[0]
                        response = "User " + username + "#" + tag + " has sent " + str(player_data["messagesSent"]) + " messages so far"
                    
                #If tag is not included in request, all members with matching usernames will be selected
                else:
                    results = self.database.find_by_username(username)
                    if(len(results) == 0):
                        response = "No users in database matching username " + username
                    for result in results:
                        response = response + "User " + username + "#" + result["tag"] + " has sent " + str(result["messagesSent"]) + " messages so far\n"
            else:
                response = "Too many arguments given, use !stats for own stats or !stats <username> for another users stats"
        else:
            response = "This command is disabled by configuration!"
        await ctx.send(response)
        

    @commands.command()
    async def init(self,ctx):
        response = ""
        
        #CONFIG
        config_status = self.config.is_valid_config()
        if(config_status[0] == 1):
            response += "The config is already configured and ready to use\n"
        elif(config_status[0] == 0):
            response += "The config is already configured but some entries are missing. These will be automatically created with their default value:\n"
            for key in config_status[1]:
                response = response + self.restore_entry(key) + "\n"
        else:
            #Create config.json
            self.config.init_config()
            response += "Created config file with default configuration settings\n"
            
        #DATABASE
        users = self.get_all_users()
        database_status = self.database.all_users_present(users)
        #status = 1 -> All users on this server are present in the database 	status = 0 -> Some users are not present in the database
        if(database_status[0] == 1):
            response += "The database is already configured and ready to use\n"
        else:
            response += str(len(database_status[1])) + " entries are missing in the database and are now added\n"
            #Fill user database with all users currently on this server
            for user in database_status[1]:
                (username, tag) = str(user).split('#')[0:2]
                self.database.add_to_user_collection(username, tag, str(user.joined_at))
        await ctx.send(response)
        
        
    @commands.command()
    async def restoredefault(self, ctx, *args):
        response = ""
        if(len(args) == 1):
            response = self.restore_entry(args[0])
        else:
            response = "Usage: !restoredefault <ConfigEntry>"
        await ctx.send(response)
        
        
    @commands.command()
    async def listusers(self, ctx, *args):
        users = self.get_all_users()
        response = ""
        if self.config.get_from_config("enable_command_listusers"):
            show_online_only = (len(args) == 1 and str(args[0]) == "online")
                    
            if(show_online_only):
                response = "All users currently online:\n"
            else:
                response = "All users on this server:\n"
            for user in users:
                if (str(user.status) == "online" and show_online_only) or not show_online_only:
                    user_roles = ""
                    for role in user.roles:
                        if str(role) != "@everyone":
                            user_roles += str(role)
                    response = response + user.name + ", Roles: " + user_roles + ", joined on: " + str(user.joined_at) + "\n"
        else:
            response = "This command is disabled by configuration!"
        await ctx.send(response)
    
    
    @commands.command()
    async def cleardatabase(self, ctx):
        if(self.config.get_from_config("enable_command_cleardatabase")):
            users = self.database.find_all_users()
            for user in users:
                self.database.delete_from_users(user["username"], user["tag"])
            response = "Database cleared!"
        else:
            response = "This command is disabled by configuration!"
        await ctx.send(response)
        
    @commands.command()
    async def about(self, ctx):
        response = self.config.get_from_config("about_message")
        await ctx.send(response)
        


def setup(bot):
    bot.add_cog(Commands(bot))