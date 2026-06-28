import discord
from discord import app_commands
from db.services import anonymous_blocked_user_service as blocked_user_service
from errors import errors
from ._anonymous import send_anonymous_content, success_embed, send_anonymous_log


@app_commands.command(name="익명답장", description="익명으로 메시지를 답장합니다.")
@app_commands.rename(message_id="메세지_id", content="메세지")
@app_commands.describe(
    message_id="답장할 메시지의 ID를 입력하세요. (메시지 우클릭 -> ID 복사)",
    content="답장할 내용을 입력하세요."
)
@app_commands.checks.cooldown(1, 3.0, key=lambda i: i.user.id)
async def anonymous_reply_command(
    interaction: discord.Interaction,
    message_id: str,
    content: app_commands.Range[str, 1, 1900]
):
    await interaction.response.defer(ephemeral=True)

    if not content.strip():
        raise errors.DBError.WrongApproach("공백만으로는 메시지를 보낼 수 없습니다.")

    if blocked_user_service.is_blocked(user_id=interaction.user.id):
        raise errors.AuthError.UserBlockedError("익명답장에서 차단되셨습니다. 관리자에게 문의하세요.")

    try:
        target_message = await interaction.channel.fetch_message(int(message_id))
    except (discord.NotFound, ValueError):
        raise errors.MessageError.MessageNotFoundError("해당 메시지 ID를 찾을 수 없습니다. ID를 다시 확인해 주세요.")
    except discord.Forbidden:
        raise errors.AuthError.ForbiddenError("봇이 이 채널의 메시지를 읽을 권한이 없습니다.")

    sent_message = await send_anonymous_content(target_message.reply, content)
    await send_anonymous_log(interaction, "익명답장 기능이 사용되었습니다.", content, sent_message)
    await interaction.followup.send(embed=success_embed(), ephemeral=True)