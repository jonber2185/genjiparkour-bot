import discord
from discord import app_commands
from db.services import clear_service
from ..utils import code_autocomplete
from errors import errors


@app_commands.command(name="클리어취소", description="인증된 클리어를 취소합니다.")
@app_commands.rename(user="유저", code="코드")
@app_commands.describe(user="유저", code="코드")
@app_commands.autocomplete(code=code_autocomplete)
@app_commands.default_permissions(administrator=True)
async def clear_cancel_command(
    interaction: discord.Interaction,
    user: discord.Member,
    code: str
):
    await interaction.response.defer(ephemeral=True)

    if len(code) < 5:
        raise errors.DBError.DataValidationError("코드는 5글자 이상이어야 합니다.")
    
    code = code.upper()
    clear_info = clear_service.get_clear_user(code=code, user_id=user.id) 
    if clear_info is None:
        raise errors.DBError.DataValidationError(f"**{user.display_name}**님은 `{code}`를 깬 기록이 없습니다.")
    
    ### 삭제 로직
    old_tier, new_tier = clear_service.cancel_clear(clear_info)

    if old_tier != new_tier:
        old_role = discord.utils.get(interaction.guild.roles, name=old_tier)
        new_role = discord.utils.get(interaction.guild.roles, name=new_tier)

        if old_role and old_role in user.roles:
            await user.remove_roles(old_role)
        if new_role:
            await user.add_roles(new_role)

    await interaction.followup.send(embed=discord.Embed(
        title="👍 클리어 기록이 삭제되었습니다.",
        description=(
            f"**유저:** {user.mention}\n"
            f"**맵 코드:** `{code}`\n"
            f"**기록:** {clear_info.clear_time:.2f}초\n"
        ),
        color=discord.Color.green(),
    ), ephemeral=True)
