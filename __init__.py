import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.logger import init_logger
from utils.prefix_util import get_prefix

init_logger(logging.DEBUG)
log = logging.getLogger(__name__)

# Credentials
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('DISCORD_ID')

extensions = ['cogs.owner', 'cogs.dice']

bot = commands.Bot(command_prefix=get_prefix, description='The Elder Brain')


if __name__ == '__main__':
    log.info(TOKEN)
    for extension in extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""
    log.info(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

bot.run(TOKEN, bot=True, reconnect=True)
