import discord
from discord import app_commands
from db.services import code_service, code_autocomplete_service
from .. import utils

@app_commands.command(name="코드등록", description="새로운 겐지 파쿠르 코드를 등록합니다.")
@app_commands.rename(
    code="코드",
    map_name="맵",
    difficulty="난이도",
    creator="제작자",
    cp="단계",
    description="추가설명",
    guide="가이드",
)
@app_commands.describe(
    code="코드 (5자리)",
    map_name="맵 검색 (예: 왕, 할리)",
    difficulty="난이도 선택",
    creator="(옵션에 없으면 직접 입력 후 엔터)",
    cp="(예: 100)",
    description="(예: 앉콩맵, 벽캔맵)",
    guide="가이드 링크",
)
@app_commands.autocomplete(map_name=utils.map_autocomplete)
@app_commands.autocomplete(creator=utils.creator_autocomplete)
@app_commands.choices(difficulty=utils.DIFFICULTY_CHOICES)
@app_commands.default_permissions(administrator=True)
async def add_code_command(
    interaction: discord.Interaction,
    code: str,
    map_name: str,
    difficulty: str,
    creator: str,
    cp: int = None,
    description: str = None,
    guide: str = None,
):
    await interaction.response.defer(ephemeral=True)

    code = code.upper()
    creator = creator.upper()

    code_service.add_code(
        code=code,
        map_name=map_name,
        difficulty=difficulty,
        creator=creator,
        cp=cp,
        description=description,
        guide=guide,
    )
    code_autocomplete_service.load_memory()

    lines = [
        f"> 코드 : **{code}**",
        f"> 맵 : {map_name}",
        f"> 난이도 : {difficulty}",
        f"> 제작자 : {creator}",
    ]
    if cp:          lines.append(f"> 체크포인트 : {cp}cp")
    if description: lines.append(f"> 설명 : {description}")
    if guide:       lines.append(f"> 가이드 : {guide}")

    embed = discord.Embed(
        title="✍️ 코드 추가 성공",
        description="코드가 성공적으로 등록되었습니다!\n\n" + "\n".join(lines),
        color=discord.Color.green(),
    )
    await interaction.followup.send(embed=embed, ephemeral=True)