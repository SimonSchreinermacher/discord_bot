import discord
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
	print("Username:" + username)
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

	print(content)
	dbfile.close()

	dbfile = open(file, "w")
	dbfile.write(content)
	dbfile.close()


@bot.event
async def on_message(message):
	if message.author == bot.user:
		return

	addCountToUser("db.txt", str(message.author))
	
	#await message.channel.send(message.content)


#TODO: Add .env to gitignore
load_dotenv()
token = os.getenv("TOKEN")
bot.run(token)