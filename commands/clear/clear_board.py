import discord
from discord import app_commands
from db.entities import ClearEntity, TierEntity
from db.services import clear_service
from ..utils import get_user_by_id, code_autocomplete
from .clear_board_pagination_view import PaginationView
from errors import errors


def _medal(idx: int) -> str:
    return {0: "🥇", 1: "🥈", 2: "🥉"}.get(idx, f"{idx + 1}.")


@app_commands.command(name="클리어보드", description="유저들의 티어를 확인합니다.")
@app_commands.rename(code="코드", clear_user="유저")
@app_commands.describe(code="조회할 코드", clear_user="조회할 유저")
@app_commands.autocomplete(code=code_autocomplete)
async def clear_board_command(
    interaction: discord.Interaction,
    code: str = None,
    clear_user: discord.Member = None,
):
    if code is not None and clear_user is not None:
        raise errors.DBError.DataValidationError("조건은 **최대 한개**까지 입력 가능합니다.")

    await interaction.response.defer(ephemeral=True)

    if code is not None:
        await _send_code_board(interaction, code.upper())
    elif clear_user is not None:
        await _send_user_board(interaction, clear_user)
    else:
        await _send_top_board(interaction)


async def _send_code_board(interaction: discord.Interaction, code: str):
    clear_list: list[ClearEntity] = clear_service.get_clear_users(code)

    embed = discord.Embed(title=f"🏆 **`{code}`** 클리어 현황", color=discord.Color.green())

    if not clear_list:
        embed.description = "클리어한 유저가 없습니다."
    else:
        for idx, cl in enumerate(clear_list):
            user_obj = await get_user_by_id(interaction, cl.user_id)
            user_display = user_obj.display_name if user_obj else f"퇴장한 유저 #{cl.user_id}"
            embed.add_field(
                name=f"**{_medal(idx)} {user_display}**",
                value=f"> 기록: **`{cl.clear_time}`**초",
                inline=False,
            )

    await interaction.followup.send(embed=embed, ephemeral=True)


async def _send_user_board(interaction: discord.Interaction, clear_user: discord.Member):
    t = clear_service.get_user_tier(user_id=clear_user.id)

    clear_infos = clear_service.get_user_clears(clear_user.id)

    embed = discord.Embed(
        title=f"👏 {clear_user.display_name}님의 클리어 현황",
        description=f"**티어: `{t.tier}`**\n",
        color=discord.Color.green(),
    )

    if not clear_infos:
        await interaction.followup.send(
            embed=embed.add_field(name="*아직 클리어한 맵이 없습니다.*", value=""), 
            ephemeral=True
        )
        return
    
    view = PaginationView(data_list=clear_infos, default_embed=embed, per_page=10)
    msg = await interaction.followup.send(embed=view.make_embed(), view=view, ephemeral=True)
    view.message = msg


async def _send_top_board(interaction: discord.Interaction):
    clear_list: list[TierEntity] = clear_service.get_users_tier()

    embed = discord.Embed(title="🏆 TOP 10", color=discord.Color.green())

    if not clear_list:
        embed.description = "클리어한 유저가 없습니다."
    else:
        for idx, cl in enumerate(clear_list):
            user_obj = await get_user_by_id(interaction, cl.user_id)
            user_display = user_obj.mention if user_obj else "(퇴장한 유저)"
            embed.add_field(
                name="",
                value=(
                    f"**{_medal(idx)} {user_display}** `{cl.tier}`\n"
                    f"> Easy: {cl.easy_count}\n"
                    f"> Medium: {cl.medium_count}\n"
                    f"> Hard: {cl.hard_count}\n"
                    f"> VeryHard: {cl.veryhard_count}\n"
                    f"> Extreme: {cl.extreme_count}\n"
                    f"> Hell: {cl.hell_count}"
                ),
                inline=False,
            )

    await interaction.followup.send(embed=embed, ephemeral=True)