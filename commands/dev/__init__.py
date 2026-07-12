from discord.ext import commands
from .db_admin import db_admin_command


class DevCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(db_admin_command)


async def setup(bot):
    await bot.add_cog(DevCog(bot))
