import discord
from discord import app_commands
from db.services import code_service, code_autocomplete_service
from .. import utils


@app_commands.command(name="코드수정", description="등록된 겐지 파쿠르 코드를 수정합니다.")
@app_commands.rename(
    code="코드",
    map_name="맵",
    difficulty="난이도",
    description="설명",
    creator="제작자",
)
@app_commands.describe(
    code="기존 코드 (5자리)",
    map_name="새로운 맵 검색 (예: 왕, 할리)",
    difficulty="새로운 난이도 선택",
    description="(예: 앉콩맵, 벽캔맵)",
    creator="새로운 제작자",
)
@app_commands.autocomplete(code=utils.code_autocomplete)
@app_commands.autocomplete(map_name=utils.map_autocomplete)
@app_commands.autocomplete(creator=utils.creator_autocomplete)
@app_commands.choices(difficulty=utils.DIFFICULTY_CHOICES)
@app_commands.default_permissions(administrator=True)
async def update_code_command(
    interaction: discord.Interaction,
    code: str,
    map_name: str = None,
    difficulty: str = None,
    description: str = None,
    creator: str = None,
):
    await interaction.response.defer(ephemeral=True)

    updates = {
        k: v for k, v in {
            "map_name":   map_name,
            "difficulty": difficulty,
            "description": description,
            "creator":    creator,
        }.items() if v is not None
    }
    code_service.update_code(code=code, updates=updates)
    code_autocomplete_service.load_memory()

    lines = [f"> 코드 : **{code}**"]
    if map_name:   lines.append(f"> 맵 : {map_name}")
    if difficulty: lines.append(f"> 난이도 : {difficulty}")
    if description: lines.append(f"> 설명 : {description}")
    if creator:    lines.append(f"> 제작자 : {creator}")

    embed = discord.Embed(
        title="🔨 코드 수정 성공",
        description="코드가 성공적으로 수정되었습니다!",
        color=discord.Color.green(),
    )
    embed.add_field(name="수정 내용", value="\n".join(lines), inline=False)
    await interaction.followup.send(embed=embed, ephemeral=True)