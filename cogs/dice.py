import logging
import random

from discord.ext import commands

log = logging.getLogger(__name__)


class DiceCog(commands.Cog):
    """DiceCog for rolling dice."""
    DICE_LIMIT = 250

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['r'])
    async def roll(self, ctx, *, roll: str):
        """Rolls dice. Expected format '(#)d#'."""

        try:
            # Extract number of dice and dice max
            num_dice = 1
            dice_val = None
            try:
                roll = roll.split('d')
                log.info(roll)
                if len(roll) == 2 and roll[0] != '':
                    num_dice = int(roll[0])
                    dice_val = int(roll[1])
                else:
                    dice_val = int(roll[1])
            except Exception as e:
                log.exception(e)
                await ctx.send(f'Format has to be either d# or #d# {ctx.message.author.mention}.')
                return

            if num_dice > self.DICE_LIMIT:
                await ctx.send(f'I only have two processors {ctx.message.author.mention}...')

            if num_dice == 0:
                await ctx.send(f'That would be 0 {ctx.message.author.mention}...')

            # Roll the dice
            rolls = []
            for r in range(num_dice):
                rolls.append(random.randint(1, dice_val))

            if num_dice > 1:
                await ctx.send(f'{ctx.message.author.mention} :game_die:\nResult: {sum(rolls)}\t\t'
                               f'From: {", ".join(str(r) for r in rolls)}')
            else:
                await ctx.send(f'{ctx.message.author.mention} :game_die:\nResult: {sum(rolls)}')

        except Exception as e:
            log.exception(e)
            return


def setup(bot):
    bot.add_cog(DiceCog(bot))
