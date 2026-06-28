import discord
from discord import app_commands
from db.services import map_service, map_autocomplete_service
from ..utils import map_autocomplete


@app_commands.command(name="맵수정", description="맵 이름을 수정합니다.")
@app_commands.rename(current_map_name="기존맵", new_map_name="새맵")
@app_commands.describe(current_map_name="기존 맵 이름", new_map_name="새로운 맵 이름")
@app_commands.autocomplete(current_map_name=map_autocomplete)
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(manage_channels=True)
async def edit_map_command(
    interaction: discord.Interaction,
    current_map_name: str,
    new_map_name: str,
):
    await interaction.response.defer(ephemeral=True)

    map_service.update_map(current_map_name, new_map_name)
    map_autocomplete_service.load_memory()

    embed = discord.Embed(
        title="✂️ 맵 수정 완료",
        description=f"맵 **{current_map_name}**이/가 **{new_map_name}**으로 변경되었습니다.",
        color=discord.Color.green(),
    )
    await interaction.followup.send(embed=embed, ephemeral=True)