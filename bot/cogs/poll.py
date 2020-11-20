import asyncio
import logging
import discord

from discord.ext import commands

log = logging.getLogger(__name__)


class PollCog(commands.Cog):
    """PollCog for making polls."""
    MAX_OPTIONS = 10
    MAX_REACTIONS = 240
    POLL_TIMEOUT = 60

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['p'])
    async def poll(self, ctx, *, question: str):
        """Creates a poll then polls for options."""

        messages = [ctx.message]
        options = []

        def check_message(m):
            return m.author == ctx.author and m.channel == ctx.channel and len(m.content) <= 100

        # Get up to MAX_OPTIONS
        for i in range(self.MAX_OPTIONS):
            messages.append(await ctx.send(f'Type an option or type submit to publish the poll.'))

            try:
                entry = await self.bot.wait_for('message', check=check_message, timeout=self.POLL_TIMEOUT)
            except asyncio.TimeoutError:
                break

            messages.append(entry)

            if entry.clean_content.startswith(f'submit'):
                break

            options.append((chr(0x1f1e6 + i), entry.clean_content))

        try:
            await ctx.channel.delete_messages(messages)
        except Exception as e:
            log.exception(e)
            pass

        poll = None
        embed = discord.Embed(title=question)
        try:
            for emoji, option in options:
                embed.add_field(name=f'{emoji}: {option}\t', value='0', inline=False)
            poll = await ctx.message.channel.send(embed=embed)
        except Exception as e:
            log.exception(e)
            await ctx.send(f'Failed to create poll...')

        def check_reaction(r, u):
            return r.channel == ctx.channel and r.message.id == poll.id

        # Get up to MAX_WAIT
        for i in range(self.MAX_REACTIONS):
            try:
                reaction, _ = await self.bot.wait_for('reaction_add', check=check_reaction, timeout=self.POLL_TIMEOUT)
            except asyncio.TimeoutError:
                pass

            log.debug(embed.to_dict())

        try:
            await ctx.channel.delete_messages(messages)
        except Exception as e:
            log.exception(e)
            pass

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send('Missing the question.')


def setup(bot):
    bot.add_cog(PollCog(bot))
