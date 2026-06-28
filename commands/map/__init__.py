from discord.ext import commands
from .add_map import add_map_command
from .edit_map import edit_map_command
from .remove_map import remove_map_command


class MapCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(add_map_command)
        self.bot.tree.add_command(edit_map_command)
        self.bot.tree.add_command(remove_map_command)


async def setup(bot):
    await bot.add_cog(MapCog(bot))