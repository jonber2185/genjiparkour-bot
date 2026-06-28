import discord
from discord import ui
from db.services import anonymous_blocked_user_service as blocked_user_service
from ..utils import get_user_by_id, send_dm
from errors import errors
from errors.handler import on_app_command_error as handle_error


class AnonymousLogView(ui.View):
    def __init__(self, jump_url: str):
        super().__init__(timeout=None)
        self.add_item(ui.Button(
            label="메시지 따라가기",
            style=discord.ButtonStyle.link,
            url=jump_url,
        ))

    @ui.button(label="작성자 차단", style=discord.ButtonStyle.danger, custom_id="fixed_log_block_btn")
    async def block_button_callback(self, interaction: discord.Interaction, button: ui.Button):
        if not interaction.user.guild_permissions.manage_channels:
            raise errors.AuthError.ForbiddenError("관리자만 유저를 차단할 수 있습니다.")
        if not interaction.message.embeds:
            raise errors.DBError.WrongApproach("로그 정보를 읽을 수 없습니다.")
        
        await interaction.response.defer(ephemeral=True)

        first_line = interaction.message.embeds[0].description.split("\n", 1)[0]
        user_id_str = first_line.split("#")[-1].strip()
        block_user = await get_user_by_id(interaction, int(user_id_str))

        if block_user is None:
            raise errors.DBError.WrongApproach("디스코드에서 찾을 수 없는 유저입니다.")
        if block_user.bot:
            raise errors.DBError.WrongApproach("봇은 차단할 수 없습니다.")
        if block_user.id == interaction.user.id:
            raise errors.DBError.WrongApproach("자기 자신은 차단할 수 없습니다.")

        blocked_user_service.block_user(user_id=block_user.id, is_blocked=True)

        embed = discord.Embed(
            title="🚫 익명 사용 차단 완료",
            description=(
                f"**대상:** {block_user.mention}\n\n"
                f"> 이제 해당 유저는 이 서버에서 `/익명채팅` 명령어를 사용할 수 없습니다."
            ),
            color=discord.Color.orange(),
        )

        embed = await send_dm(user=block_user, embed=embed)
        await interaction.followup.send(embed=embed, ephemeral=True)

        button.disabled = True
        button.label = "차단 완료됨"
        await interaction.message.edit(view=self)

    async def on_error(self, interaction: discord.Interaction, error: Exception, item: discord.ui.Item):
        await handle_error(interaction, error)