import discord
from discord import app_commands
from discord.ext import commands
from .handler import on_app_command_error as handle_error


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.on_error = self.on_app_command_error

    async def on_app_command_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ):
        await handle_error(interaction, getattr(error, "original", error))


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))