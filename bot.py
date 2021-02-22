import discord
import database
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
	return response


@bot.event
async def on_message(message):
	if message.author == bot.user:
		return

	messageParts = message.content.split(" ")
	command = messageParts[0]
	args = messageParts[1:]
	response = ""
	(author,tag) = str(message.author).split("#")[0:2]

	if(command == "!stats"):
		response = command_stats(author, tag, args, message)
		await message.channel.send(response)
		return

	#If no commands match user message, increase message count by one (bot commands should not count towards message count)
	#If user is not in database, add them before incrementing their counter
	results = database.findByUsername(author, tag)
	if(len(results) == 0):
		database.addToUserCollection(author, tag)
	
	database.incrementMessageCount(author, tag)

load_dotenv()
token = os.getenv("TOKEN")
bot.run(token)