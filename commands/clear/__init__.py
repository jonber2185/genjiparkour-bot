from discord.ext import commands
from .clear_board import clear_board_command
from .clear_authentication import clear_authentication_command
from .clear_cancel import clear_cancel_command


class ClearCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(clear_board_command)
        self.bot.tree.add_command(clear_authentication_command)
        self.bot.tree.add_command(clear_cancel_command)


async def setup(bot):
    await bot.add_cog(ClearCog(bot))