import logging
import discord
from discord import app_commands
from .errors import AppError

logger = logging.getLogger(__name__)


async def on_app_command_error(interaction: discord.Interaction, orig_error: Exception):
    if isinstance(orig_error, AppError):
        embed = discord.Embed(
            title="😞 요청 실패",
            description=orig_error.message,
            color=discord.Color.red(),
        )
    elif isinstance(orig_error, app_commands.errors.MissingPermissions):
        perms = ", ".join(orig_error.missing_permissions)
        embed = discord.Embed(
            title="🛡️ 권한 부족",
            description=f"권한이 필요합니다: `{perms}`",
            color=discord.Color.orange(),
        )
    elif isinstance(orig_error, app_commands.errors.CommandOnCooldown):
        embed = discord.Embed(
            title="⌛ 쿨타임 제한",
            description=f"{orig_error.retry_after:.1f}초 후에 다시 시도해 주세요.",
            color=discord.Color.gold(),
        )
    else:
        source = interaction.command.name if interaction.command else "button/view"
        logger.error("(%s): %s", source, orig_error, exc_info=orig_error)
        embed = discord.Embed(
            title="🚫 시스템 오류",
            description="봇 내부에서 알 수 없는 에러가 발생했습니다. 개발자에게 문의해 주세요.",
            color=discord.Color.dark_red(),
        )

    if interaction.response.is_done():
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed, ephemeral=True)