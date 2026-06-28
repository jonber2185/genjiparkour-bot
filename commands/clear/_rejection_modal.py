import discord
from discord import ui
from typing import TYPE_CHECKING
from ..utils import send_dm
from errors import errors

if TYPE_CHECKING:
    from ._log_view import ClearLogView, ClearLogContent


class RejectModal(ui.Modal, title="❌ 클리어 인증 반려"):
    reason_input = ui.TextInput(
        label="반려 사유를 입력해주세요",
        style=discord.TextStyle.paragraph,
        placeholder="예: 클리어타임 불일치 / 인증 스크린샷 불일치",
        required=True,
        max_length=200,
    )

    def __init__(self, view: "ClearLogView", message: discord.Message):
        super().__init__()
        self.view = view
        self.message = message

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        try:
            await interaction.channel.fetch_message(self.message.id)
        except discord.NotFound:
            raise errors.MessageError.MessageNotFoundError("원본 메시지가 이미 처리되었습니다.")

        content: "ClearLogContent" = await self.view._get_content(interaction)

        await interaction.message.delete()

        embed = discord.Embed(
            title="👎 클리어 인증이 반려되었습니다",
            description=(
                f"**맵 코드:** `{content.map_code}`\n"
                f"**기록:** {content.clear_time:.2f}초\n"
                f"**유저:** {content.user_info.mention}\n"
                f"**인증자:** {interaction.user.mention}"
            ),
            color=discord.Color.red(),
        )
        embed.set_image(url=content.img_url)
        embed.add_field(name="✍️ 반려 사유", value=f"```{self.reason_input.value}```", inline=False)

        embed = await send_dm(user=content.user_info, embed=embed)
        await interaction.followup.send(embed=embed, ephemeral=True)