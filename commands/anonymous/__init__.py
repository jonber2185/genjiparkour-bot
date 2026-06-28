from discord.ext import commands
from .chat_anonymous import anonymous_chat_command
from .block_anonymous import block_anonymous_command
from .reply_anonymous import anonymous_reply_command


class AnonymousCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(anonymous_chat_command)
        self.bot.tree.add_command(block_anonymous_command)
        self.bot.tree.add_command(anonymous_reply_command)


async def setup(bot):
    await bot.add_cog(AnonymousCog(bot))