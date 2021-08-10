import discord
import database
import config
from discord.utils import get
import fileinput
from dotenv import load_dotenv
import os

intents = discord.Intents.all()
bot = discord.Client(intents = intents)

def getServer():
	server_id = os.getenv("ID")
	return bot.get_guild(int(server_id))

def getAllUsers():
	server = getServer()
	return server.members

def command_stats(author, tag, args, message):
	response = ""

	if(config.getFromConfig("enable_command_stats") == True):
		#Own Stats
		if(len(args) == 0):
			results = database.findByUsername(author, tag)
			if(len(results) == 0):
				response = "User" + author + "has not sent any messages on this server"
			else:
				playerData = results[0]
				response = "User "+ author+ " has sent "+ str(playerData["messagesSent"]) + " messages so far."

		#Stats of other member
		elif(len(args) == 1):
			splitArgument = str(args[0]).split("#")
			username = splitArgument[0]

			#If tag is included in request
			if(len(splitArgument) == 2):
				tag = splitArgument[1]
				results = database.findByUsername(username, tag)
				if(len(results) == 0):
					response = "No users in database matching full username " + username + "#" + tag
				else:
					playerData = results[0]
					response = "User "+ username+ "#" + tag +  " has sent "+ str(playerData["messagesSent"]) + " messages so far."

			#If tag is not included in request, all members with matching username will be selected
			else:
				results = database.findByUsername(username)
				if(len(results) == 0):
					response = "No users in database matching username " + username
				for result in results:
					response = response + "User " + username + "#" + result["tag"] + " has sent " + str(result["messagesSent"]) + " messages so far\n"
		else:
			response = "Too many arguments given, use !stats for own stats or !stats <username> for another users stats"
	else:
		response = "This command is disabled by configuration!"
	return response

def command_init():
	response = ""
	configStatus = config.isValidConfig()
	if(configStatus[0] == 1):
		response = "This bot is already initialized and ready to use"
	elif(configStatus[0] == 0):
		response = "This bot is already initialized, but there values missing for the following entries:\n"
		for key in configStatus[1]:
			response = response + key + "\n"
		response = response + "It is strongly recommended to use !restoredefault for all missing entries to make sure, the bot works as intended"
	else:
		#Create config.json
		config.initConfig()
		response = "Created config file with default configuration settings"

		#Fill user database with all users currently on this server
		users = getAllUsers()
		for user in users:
			(username, tag) = str(user).split('#')[0:2]
			database.addToUserCollection(username, tag, str(user.joined_at))
	return response

def command_restoredefault(args):
	if(len(args) == 1):
		defaultData = config.defaultConfig()
		try:
			configEntry = args[0]
			defaultValue = defaultData[configEntry]
			config.changeConfigEntry(configEntry, defaultValue)
			response = "Config entry " + configEntry + " changed to its default value " + str(defaultValue)
			return response
		except:
			response = configEntry + " is not a valid config entry!"
			return response
	else:
		response = "Usage: !restoredefault <ConfigEntry>"
		return response

def command_listusers(args):
	users = getAllUsers()
	response = ""

	if(config.getFromConfig("enable_command_listusers") == True):

		#Get all users
		if(len(args) == 0):
			response = "All users on this server:\n"
			for user in users:
				user_roles = ""
				for role in user.roles:
					if str(role) != "@everyone":
						user_roles = user_roles + str(role)
				response = response + user.name + ", Roles: " + user_roles + ", joined on: " + str(user.joined_at) + "\n"
		
		elif(len(args) == 1):
			#Get all users that are currently online
			if(str(args[0]) == "online"):
				response = "All users currently online:\n"
				for user in users:
					if(str(user.status) == "online"):
						user_roles = ""
						for role in user.roles:
							if str(role) != "@everyone":
								user_roles = user_roles + str(role)
						response = response + user.name + ", Roles: " + user_roles + ", joined on: " + str(user.joined_at) + "\n"
	else:
		response = "This command is disabled by configuration!"
	return response

def command_cleardatabase():
	if(config.getFromConfig("enable_command_cleardatabase") == True):
		users = database.findAllUsers()
		for user in users:
			database.deleteFromUsers(user["username"], user["tag"])
		return "Database cleared!"
	else:
		return "This command is disabled by configuration!"


def handle_commands(message):
	messageParts = message.content.split(" ")
	command = messageParts[0]
	args = messageParts[1:]
	response = ""
	(author,tag) = str(message.author).split("#")[0:2]

	if(command == "!init"):
		response = command_init()
		return response

	if(command == "!restoredefault"):
		response = command_restoredefault(args)
		return response

	if(command == "!stats"):
		response = command_stats(author, tag, args, message)
		return response

	if(command == "!listusers"):
		response = command_listusers(args)
		return response

	if(command == "!cleardatabase"):
		response = command_cleardatabase()
		return response

	return "No commands matching " + command
		
@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	if message.content.split(" ")[0] == "!init":
		response = command_init()
		await message.channel.send(response)
		return
	#If message is sent to the bot-commands channel, the bot interprets it as a command, else as a normal message
	if(config.isValidConfig()[0] == 1):
		if(str(message.channel) == config.getFromConfig("bot_channel")):
			response = handle_commands(message)
			await message.channel.send(response)
			return

		(author,tag) = str(message.author).split("#")[0:2]
		
		#If the message was sent to a channel that is not responsible for handling commands, increment message count of user
		results = database.findByUsername(author, tag)
		if(len(results) == 0):
			database.addToUserCollection(author, tag, message.author.joined_at)
		
		database.incrementMessageCount(author, tag)

load_dotenv()
token = os.getenv("TOKEN")
bot.run(token)