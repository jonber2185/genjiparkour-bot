import discord
from discord import app_commands
from db.services import map_service, map_autocomplete_service


@app_commands.command(name="맵추가", description="새로운 맵을 등록합니다.")
@app_commands.rename(map_name="맵")
@app_commands.describe(map_name="맵 이름")
@app_commands.default_permissions(administrator=True)
async def add_map_command(interaction: discord.Interaction, map_name: str):
    await interaction.response.defer(ephemeral=True)

    map_service.add_map(map_name)
    map_autocomplete_service.load_memory()

    embed = discord.Embed(
        title="✅ 맵 추가 완료",
        description=f"맵 **{map_name}**이/가 성공적으로 등록되었습니다!",
        color=discord.Color.green(),
    )
    await interaction.followup.send(embed=embed, ephemeral=True)