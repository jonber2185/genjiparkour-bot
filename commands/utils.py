import discord
from discord import app_commands
from db.enums import Difficulty
from db.services import map_autocomplete_service, code_autocomplete_service


async def map_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    try:
        maps = map_autocomplete_service.get_suggestions(current)
        choices = [
            app_commands.Choice(name=m, value=m)
            for m in maps
        ][:25]
        await interaction.response.autocomplete(choices)
    except (discord.NotFound, discord.HTTPException):
        return []


async def code_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    try:
        codes = code_autocomplete_service.get_code_suggestions(current)
        choices = [
            app_commands.Choice(name=f"{code['code']} ({code['map_name']})", value=code['code'])
            for code in codes
        ][:25]
        await interaction.response.autocomplete(choices)
    except (discord.NotFound, discord.HTTPException):
        return []


special_creators = {
    "MANTA": "💙",
    "뽈롱뽈롱뽀로로": "🐧",
    "SUNTREE": "🌞🌳",
    "DOLCE": "💪🧹",
    "엄준식화이팅": "🕵️"
}

async def creator_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    try:
        creators = code_autocomplete_service.get_creators_suggestions(current)
        sorted_creators = sorted(creators, key=lambda x: '&' in x)

        choices = []
        for creator in sorted_creators:
            if len(choices) >= 25: break
            name = creator
            value = creator
            if creator in special_creators:
                name = f"{special_creators[creator]} {creator}"
            choices.append(app_commands.Choice(name=name, value=value))

        await interaction.response.autocomplete(choices)
    except (discord.NotFound, discord.HTTPException):
        return []


DIFFICULTY_CHOICES = [app_commands.Choice(name=d.value, value=d.value) for d in Difficulty]


async def get_user_by_id(
    interaction: discord.Interaction,
    user_id: int,
) -> discord.Member | None:
    member = interaction.guild.get_member(user_id)
    if member is None:
        try:
            member = await interaction.guild.fetch_member(user_id)
        except discord.NotFound:
            pass
    return member


async def send_dm(
    user: discord.Member, 
    embed = discord.Embed,
) -> discord.Embed:
    try:
        await user.send(embed=embed)
    except discord.Forbidden:
        embed.set_footer(text=f"⚠️ 로그는 삭제되었으나, **{user.name}** 님이 DM을 차단하여 사유를 전달하지 못했습니다.")
    return embed