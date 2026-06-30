import discord
from discord import app_commands
from db.services import code_service, code_autocomplete_service
from ..utils import code_autocomplete


@app_commands.command(name="코드삭제", description="등록된 겐지 파쿠르 코드를 삭제합니다.")
@app_commands.rename(code="코드")
@app_commands.describe(code="삭제할 코드 (5자리)")
@app_commands.autocomplete(code=code_autocomplete)
@app_commands.default_permissions(administrator=True)
async def delete_code_command(interaction: discord.Interaction, code: str):
    await interaction.response.defer(ephemeral=True)

    code_service.delete_code(code.upper())
    code_autocomplete_service.load_memory()

    embed = discord.Embed(
        title="🗡️ 코드 삭제 성공",
        description="코드가 성공적으로 삭제되었습니다!",
        color=discord.Color.green(),
    )
    await interaction.followup.send(embed=embed, ephemeral=True)