import discord
from discord import app_commands
from db.services import anonymous_blocked_user_service as blocked_user_service
from errors import errors
from ._anonymous import send_anonymous_content, success_embed, send_anonymous_log


@app_commands.command(name="익명채팅", description="사용된 채널에 익명으로 메시지를 전송합니다.")
@app_commands.rename(content="익명_메시지")
@app_commands.describe(content="보낼 내용을 입력하세요.")
@app_commands.checks.cooldown(1, 3.0, key=lambda i: i.user.id)
async def anonymous_chat_command(
    interaction: discord.Interaction,
    content: app_commands.Range[str, 1, 1900],
):
    await interaction.response.defer(ephemeral=True)

    if not content.strip():
        raise errors.DBError.WrongApproach("공백만으로는 메시지를 보낼 수 없습니다.")

    if blocked_user_service.is_blocked(user_id=interaction.user.id):
        raise errors.AuthError.UserBlockedError("익명채팅에서 차단되셨습니다. 관리자에게 문의하세요.")

    sent_message = await send_anonymous_content(interaction.channel.send, content)
    await send_anonymous_log(interaction, "익명채팅 기능이 사용되었습니다.", content, sent_message)
    await interaction.followup.send(embed=success_embed(), ephemeral=True)