import discord
import database
import commands as cmd
import config
from discord.utils import get
from discord.ext import commands
import fileinput
from dotenv import load_dotenv
import os

intents = discord.Intents.all()
#bot = commands.Bot(command_prefix='!', description='description', intents = intents)

class Bot(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix='!', description='description', intents = discord.Intents.all())

			
	async def on_message(self, message):
		if message.author == bot.user:
			return

		if(config.isValidConfig()[0] == 1):
			#If message is sent to the bot-commands channel, the bot interprets it as a command and ignores it, else as a normal message
			if(str(message.channel) == config.getFromConfig("bot_channel")):
				await bot.process_commands(message)
				return
			(author,tag) = str(message.author).split("#")[0:2]
			
			#If the message was sent to a channel that is not responsible for handling commands, increment message count of user
			results = database.findByUsername(author, tag)
			if(len(results) == 0):
				database.addToUserCollection(author, tag, message.author.joined_at)
			
			database.incrementMessageCount(author, tag)
			return

		if(message.content == "!init"):
			commands = cmd.Commands(bot)
			await commands.init(commands, message.channel)
			return



load_dotenv()
token = os.getenv("TOKEN")
bot = Bot()

bot.load_extension("commands")
bot.run(token)
