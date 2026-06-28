from discord.ext import commands
from .add_code import add_code_command
from .show_codes import show_codes_command
from .update_code import update_code_command
from .delete_code import delete_code_command


class CodeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(show_codes_command)
        self.bot.tree.add_command(add_code_command)
        self.bot.tree.add_command(update_code_command)
        self.bot.tree.add_command(delete_code_command)


async def setup(bot):
    await bot.add_cog(CodeCog(bot))