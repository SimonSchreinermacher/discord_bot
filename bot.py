import discord
import database
import cogs.commands as cmd
import config
from discord.utils import get
from discord.ext import commands
import fileinput
from dotenv import load_dotenv
import os

intents = discord.Intents.all()
#bot = commands.Bot(command_prefix='!', description='description', intents = intents)

class Bot(commands.Bot):
	def __init__(self, database, config):
		super().__init__(command_prefix='!', description='description', intents = discord.Intents.all())
		self.database = database
		self.config = config

			
	async def on_message(self, message):
		if message.author == bot.user:
			return

		if(config.is_valid_config()[0] == 1):
			#If message is sent to the bot-commands channel, the bot interprets it as a command and ignores it, else as a normal message
			if(str(message.channel) == config.get_from_config("bot_channel")):
				await bot.process_commands(message)
				return
			(author,tag) = str(message.author).split("#")[0:2]
			
			#If the message was sent to a channel that is not responsible for handling commands, increment message count of user
			results = database.find_by_username(author, tag)
			if(len(results) == 0):
				database.add_to_user_collection(author, tag, message.author.joined_at)
			
			database.increment_message_count(author, tag)
			return

		if(message.content == "!init"):
			commands = cmd.Commands(bot)
			await commands.init(commands, message.channel)
			return


if __name__ == "__main__":
	load_dotenv()
	token = os.getenv("TOKEN")
	bot = Bot(database, config)

	bot.load_extension("cogs.commands")
	bot.run(token)
