from discord.ext import commands


def get_prefix(bot, message):
    """A callable Prefix for our bot. Edit this to allow per server prefixes."""
    prefixes = ['!']

    return commands.when_mentioned_or(*prefixes)(bot, message)
