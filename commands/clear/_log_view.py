import os
from dataclasses import dataclass
from dotenv import load_dotenv
import discord
from discord import ui
from db.entities import ClearEntity
from db.services import clear_service
from ._rejection_modal import RejectModal
from ..utils import get_user_by_id
from errors.handler import on_app_command_error as handle_error

load_dotenv()
CLEAR_PUB_CHANNEL_ID = int(os.getenv("CLEAR_PUB_CHANNEL_ID"))


@dataclass
class ClearLogContent:
    map_code: str
    clear_time: float
    user_info: discord.Member
    img_url: str


class ClearLogView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="👎 반려", style=discord.ButtonStyle.danger, custom_id="fixed_clear_rejection")
    async def reject_button_callback(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(RejectModal(view=self, message=interaction.message))

    @ui.button(label="👍 승인", style=discord.ButtonStyle.success, custom_id="fixed_clear_approve")
    async def approve_button_callback(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer(ephemeral=True)

        content = await self._get_content(interaction)

        old_tier, new_tier = clear_service.clear_code(ClearEntity(
            code=content.map_code.upper(),
            user_id=content.user_info.id,
            clear_time=content.clear_time,
        ))

        clear_pub_channel = interaction.guild.get_channel(CLEAR_PUB_CHANNEL_ID)
        if clear_pub_channel is None:
            clear_pub_channel = await interaction.guild.fetch_channel(CLEAR_PUB_CHANNEL_ID)

        await clear_pub_channel.send(
            embed=discord.Embed(
                title=f"👍 **{content.user_info.display_name}** 님이 **`{content.map_code}`**를 클리어했습니다.",
                description=(
                    f"**기록: {content.clear_time:.2f}초**\n"
                    f"**유저:** {content.user_info.mention}\n"
                    f"**인증자:** {interaction.user.mention}"
                ),
                color=discord.Color.green(),
            ).set_image(url=content.img_url), 
            allowed_mentions=discord.AllowedMentions.none()
        )

        if old_tier != new_tier:
            old_role = discord.utils.get(interaction.guild.roles, name=old_tier)
            new_role = discord.utils.get(interaction.guild.roles, name=new_tier)

            if old_role and old_role in content.user_info.roles:
                await content.user_info.remove_roles(old_role)
            if new_role:
                await content.user_info.add_roles(new_role)

            await clear_pub_channel.send(
                embed=discord.Embed(
                    title="🏆 티어 승급!",
                    description=f"🎉 {content.user_info.mention} 님이 **{new_tier}** 티어로 승급하였습니다.",
                    color=discord.Color.gold(),
                ), 
                allowed_mentions=discord.AllowedMentions.none()
            )

        await interaction.message.delete()
        await interaction.followup.send(embed=discord.Embed(
            title="👍 요청이 정상적으로 처리되었습니다.",
            description=(
                f"**맵 코드:** `{content.map_code}`\n"
                f"**기록:** {content.clear_time:.2f}초\n"
                f"**유저:** {content.user_info.mention}\n"
                f"**인증자:** {interaction.user.mention}"
            ),
            color=discord.Color.green(),
        ).set_image(url=content.img_url), ephemeral=True)

    async def _get_content(self, interaction: discord.Interaction) -> ClearLogContent:
        lines = [
            line.replace("*", "")
            for line in interaction.message.embeds[0].description.split("\n")
        ]
        map_code  = lines[0].replace("`", "").split("맵 코드: ", 1)[-1]
        clear_time = float(lines[3].replace("초", "").split("기록: ", 1)[-1])
        user_id   = lines[4].split("유저: ", 1)[-1].split("#")[-1]
        user_info = await get_user_by_id(interaction=interaction, user_id=int(user_id))

        return ClearLogContent(
            map_code=map_code,
            clear_time=clear_time,
            user_info=user_info,
            img_url=interaction.message.embeds[0].image.url,
        )

    async def on_error(self, interaction: discord.Interaction, error: Exception, item: ui.Item):
        await handle_error(interaction, error)