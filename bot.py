import discord
import database
from discord.utils import get
import fileinput
from dotenv import load_dotenv
import os

bot = discord.Client()


def getDB(file):
	content = {}
	with open(file) as f:
		for line in f:
			(key, val) = line.split("|")
			content[key] = val
	return content

def addCountToUser(file, username):
	#print("Username:" + username)
	dbfile = open(file, "r")
	content = ""
	found = False
	for line in dbfile:
		(user, amount) = line.split("|")
		if(user == username):
			newamount = int(amount) + 1
			content += username + "|" + str(newamount)
			found = True
		else:
			content += line
	if (found == False):
		content += username + "|" + str(1)

	#print(content)
	dbfile.close()

	dbfile = open(file, "w")
	dbfile.write(content)
	dbfile.close()

def searchForUser(file, user):
	user = user.split("#")[0] #in case someone uses full name (USERNAME#ID)
	dbfile = open(file, "r")
	for line in dbfile:
		(name, amount) = line.split("|")
		name = name.split("#")[0]
		if(name == user):
			return amount
	return 0



@bot.event
async def on_message(message):
	
	results = database.findAllUsers()
	for user in results:
		print(user)
	print("=====")
	if message.author == bot.user:
		return

	messageParts = message.content.split(" ")
	command = messageParts[0]
	args = messageParts[1:]
	response = ""

	if(command == "!stats"):

		#Own Stats
		if(len(args) == 0):
			(author,tag) = str(message.author).split("#")[0:2]
			results = database.findByUsername(author, tag)
			if(len(results) == 0):
				database.addToUserCollection(author, tag)
				response = "User" + author + "has not sent any messages on this server"
			else:
				playerData = results[0]
				response = "User "+ author+ " has sent "+ str(playerData["messagesSent"]) + " messages so far."

		#Stats of other member
		elif(len(args) == 1):
			messageAmount = searchForUser("db.txt", str(args[0]))
			splitArgument = str(args[0]).split("#")
			username = splitArgument[0]

			#If tag is included in request
			if(len(splitArgument) == 2):
				tag = splitArgument[1]
				results = database.findByUsername(username, tag)
				if(len(results) == 0):
					response = "User " + username + "#" + tag + " has not sent any messages on this server"
				else:
					playerData = results[0]
					response = "User "+ username+ "#" + tag +  " has sent "+ str(playerData["messagesSent"]) + " messages so far."

			#If tag is not included in request
			else:
				results = database.findByUsername(username)
				if(len(results) == 0):
					response = "No users in database matching username " + username
				for result in results:
					response = response + "User " + username + "#" + result["tag"] + " has sent " + str(result["messagesSent"]) + " messages so far\n"
		else:
			response = "Too many arguments given, use !stats for own stats or !stats <username> for another users stats"
		await message.channel.send(response)
		return

	addCountToUser("db.txt", str(message.author))

load_dotenv()
token = os.getenv("TOKEN")
bot.run(token)