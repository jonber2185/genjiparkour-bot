import os
import discord
from dotenv import load_dotenv
from ._log_view import AnonymousLogView
import logging
from errors import errors

logger = logging.getLogger(__name__)

load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))


def format_anonymous_content(content: str) -> str:
    return f"{content}\n> -# 이 메시지는 익명으로 작성되었습니다. '/익명채팅'"


async def send_anonymous_content(action, content: str) -> discord.Message:
    try:
        return await action(
            content=format_anonymous_content(content),
            allowed_mentions=discord.AllowedMentions.none(),
        )
    except discord.HTTPException as e:
        logger.error("익명 메시지 전송 실패: %s", e)
        raise errors.MessageError.SendFailedError()


def success_embed() -> discord.Embed:
    return discord.Embed(
        title="🤫 전송 완료",
        description="익명 메시지가 성공적으로 전송되었습니다!\n\n-# 모든 메시지는 기록이 남습니다.",
        color=discord.Color.green(),
    )


async def send_anonymous_log(
    interaction: discord.Interaction,
    title: str,
    content: str,
    sent_message: discord.Message,
):
    log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
    if log_channel is None:
        log_channel = await interaction.guild.fetch_channel(LOG_CHANNEL_ID)

    log_embed = discord.Embed(
        title=title,
        description=(
            f"> 사용자: {interaction.user.mention} #{interaction.user.id}\n"
            f"> 사용 채널: {interaction.channel}\n"
            f"> 메시지: {content}"
        ),
        color=discord.Color.dark_purple(),
    )
    view = AnonymousLogView(jump_url=sent_message.jump_url)
    await log_channel.send(embed=log_embed, view=view, allowed_mentions=discord.AllowedMentions.none())