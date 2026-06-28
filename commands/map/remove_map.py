import discord
from discord import app_commands
from db.services import map_service, map_autocomplete_service, code_autocomplete_service
from ..utils import map_autocomplete


@app_commands.command(name="맵삭제", description="맵을 삭제합니다.")
@app_commands.rename(map_name="맵")
@app_commands.describe(map_name="맵 이름")
@app_commands.autocomplete(map_name=map_autocomplete)
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(manage_channels=True)
async def remove_map_command(interaction: discord.Interaction, map_name: str):
    await interaction.response.defer(ephemeral=True)

    map_service.delete_map(map_name)
    map_autocomplete_service.load_memory()
    code_autocomplete_service.load_memory()

    embed = discord.Embed(
        title="❎ 맵 삭제 완료",
        description=f"맵 **{map_name}**이/가 삭제되었습니다.",
        color=discord.Color.green(),
    )
    await interaction.followup.send(embed=embed, ephemeral=True)