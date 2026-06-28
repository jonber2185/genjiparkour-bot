import discord
from discord import app_commands
from db.services import code_service
from .. import utils
from .pagination_view import PaginationView


@app_commands.command(name="코드조회", description="등록된 겐지 파쿠르 코드를 조회합니다.")
@app_commands.rename(map_name="전장", difficulty="난이도", creator="제작자", code="코드")
@app_commands.describe(
    map_name="맵 검색 (예: 왕, 할리)",
    difficulty="난이도 선택",
    creator="제작자",
    code="코드",
)
@app_commands.autocomplete(map_name=utils.map_autocomplete)
@app_commands.autocomplete(creator=utils.creator_autocomplete)
@app_commands.autocomplete(code=utils.code_autocomplete)
@app_commands.choices(difficulty=utils.DIFFICULTY_CHOICES)
async def show_codes_command(
    interaction: discord.Interaction,
    map_name: str = None,
    difficulty: str = None,
    creator: str = None,
    code: str = None,
):
    await interaction.response.defer(ephemeral=True)

    codes = code_service.get_codes(
        user_id=interaction.user.id,
        map_name=map_name,
        difficulty=difficulty,
        creator=creator,
        code=code,
    )

    if not codes:
        await interaction.followup.send(
            embed=discord.Embed(
                title="📂 코드 목록",
                description="등록된 코드가 없습니다.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )
        return

    view = PaginationView(data_list=codes, per_page=10)
    msg = await interaction.followup.send(embed=view.make_embed(), view=view, ephemeral=True)
    view.message = msg