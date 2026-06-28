import discord
from discord import app_commands
from db.services import anonymous_blocked_user_service as blocked_user_service
from ..utils import send_dm, get_user_by_id
from errors import errors


@app_commands.command(name="익명차단", description="유저의 익명 채팅 사용을 차단합니다.")
@app_commands.rename(block_user="차단", unblock_user="차단해제", show_list="명단")
@app_commands.describe(
    block_user="차단할 유저",
    unblock_user="차단해제할 유저",
    show_list="명단 보기 (True 설정)",
)
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(manage_channels=True)
async def block_anonymous_command(
    interaction: discord.Interaction,
    block_user: discord.Member = None,
    unblock_user: discord.Member = None,
    show_list: bool = False,
):
    if not any([block_user, unblock_user, show_list]):
        raise errors.DBError.DataValidationError("`차단`, `차단해제`, `명단` 중 **최소 하나 이상**은 입력해야 합니다.")

    await interaction.response.defer(ephemeral=True)

    embeds = []

    if block_user:
        if block_user.id == interaction.user.id:
            raise errors.DBError.WrongApproach("자기 자신은 차단할 수 없습니다.")
        if block_user.bot:
            raise errors.DBError.WrongApproach("봇은 차단할 수 없습니다.")
        blocked_user_service.block_user(user_id=block_user.id, is_blocked=True)
        embed = discord.Embed(
            title="🚫 익명 사용 차단 완료",
            description=(
                f"**대상:** {block_user.mention} #{block_user.id}\n\n"
                f"> 이제 해당 유저는 이 서버에서 `/익명채팅` 명령어를 사용할 수 없습니다."
            ),
            color=discord.Color.orange(),
        )
        embed = await send_dm(user=block_user, embed=embed)
        embeds.append(embed)

    if unblock_user:
        blocked_user_service.block_user(user_id=unblock_user.id, is_blocked=False)
        embed = discord.Embed(
            title="👍 차단해제 완료",
            description=(
                f"**대상:** {unblock_user.mention} #{unblock_user.id}\n\n"
                f"> 이제 해당 유저는 이 서버에서 `/익명채팅` 명령어를 사용할 수 있습니다."
            ),
            color=discord.Color.blue(),
        )
        embed = await send_dm(user=unblock_user, embed=embed)
        embeds.append(embed)

    if show_list:
        embeds.append(await _build_block_list_embed(interaction))

    await interaction.followup.send(embeds=embeds, ephemeral=True)


async def _build_block_list_embed(interaction: discord.Interaction) -> discord.Embed:
    user_ids = blocked_user_service.get_list()

    lines = []
    for user_id in user_ids:
        user = await get_user_by_id(interaction, user_id)
        if user is None:
            lines.append(f"> (퇴장한 유저) #{user_id}")
            continue
        lines.append(f"> {user.mention} `{user_id}`")

    return discord.Embed(
        title="📋 차단 명단",
        description="\n".join(lines) if lines else "차단된 유저가 없습니다.",
        color=discord.Color.light_grey(),
    )