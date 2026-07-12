import discord
from discord import app_commands
from db.entities import CodeEntity
from db.services import code_service
from .. import utils
from .pagination_view import PaginationView


RAND_CHOICES = [app_commands.Choice(name="클리어 맵 포함", value="include"), app_commands.Choice(name="클리어 맵 제외", value="exclude")]

@app_commands.command(name="코드조회", description="등록된 겐지 파쿠르 코드를 조회합니다.")
@app_commands.rename(map_name="전장", difficulty="난이도", creator="제작자", code="코드", rand="랜덤추천")
@app_commands.describe(
    map_name="맵 검색 (예: 왕, 할리)",
    difficulty="난이도 선택",
    creator="제작자",
    code="코드",
    rand="랜덤 추천 여부"
)
@app_commands.autocomplete(map_name=utils.map_autocomplete)
@app_commands.choices(difficulty=utils.DIFFICULTY_CHOICES)
@app_commands.autocomplete(creator=utils.creator_autocomplete)
@app_commands.autocomplete(code=utils.code_autocomplete)
@app_commands.choices(rand=RAND_CHOICES)
async def show_codes_command(
    interaction: discord.Interaction,
    map_name: str = None,
    difficulty: str = None,
    creator: str = None,
    code: str = None,
    rand: str = None,
):
    await interaction.response.defer(ephemeral=True)

    if code is not None:
        code_info = code_service.get_code(code)
        await _send_code_status(interaction, code_info)
        return

    codes = code_service.get_codes(
        user_id=interaction.user.id,
        map_name=map_name,
        difficulty=difficulty,
        creator=creator,
        rand=rand,
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
    
    if rand is not None:
        await _send_code_status(interaction, codes[0])
        return

    view = PaginationView(data_list=codes, per_page=10)
    msg = await interaction.followup.send(embed=view.make_embed(), view=view, ephemeral=True)
    view.message = msg


async def _send_code_status(interaction: discord.Interaction, code_info: CodeEntity):
    if code_info is None:
        description = f"코드에 대한 정보가 없습니다."
    else:
        clear_time = f"*#{code_info.clear_time}초*" if code_info.clear_time else ""
        lines = [
            f"> 코드 : **`{code_info.code}` {clear_time}**",
            f"> 전장: {code_info.map_name}",
            f"> 난이도: {code_info.difficulty.value}",
        ]
        if code_info.cp:          lines.append(f"> 체크포인트 : {code_info.cp}cp")
        if code_info.description: lines.append(f"> 설명 : {code_info.description}")
        lines.append(f"> 제작자 : {code_info.creator}")
        if code_info.guide:       lines.append(f"> [가이드]({code_info.guide})")
        description = "\n".join(lines)

    await interaction.followup.send(
        embed=discord.Embed(
            title="📂 코드 조회",
            description=description,
            color=discord.Color.green(),
        ),
        ephemeral=True,
    )