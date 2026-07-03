import io
import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from PIL import Image
from db.services import code_service
from ._log_view import ClearLogView
from ..utils import code_autocomplete
from errors import errors

load_dotenv()
CLEAR_CHANNEL_ID = int(os.getenv("CLEAR_CHANNEL_ID"))


@app_commands.command(name="클리어인증", description="클리어를 인증하여 티어를 갱신하세요.")
@app_commands.rename(code="코드", clear_time="기록", screenshot="이미지")
@app_commands.describe(code="코드", clear_time="클리어 타임 (예: 405.12)", screenshot="클리어 완료 스크린샷")
@app_commands.autocomplete(code=code_autocomplete)
async def clear_authentication_command(
    interaction: discord.Interaction,
    code: str,
    clear_time: float,
    screenshot: discord.Attachment,
):
    await interaction.response.defer(ephemeral=True)

    if screenshot.content_type and not screenshot.content_type.startswith("image/"):
        raise errors.DBError.DataValidationError("이미지 파일만 업로드할 수 있습니다.")
    if len(code) < 5:
        raise errors.DBError.DataValidationError("코드는 5글자 이상이어야 합니다.")

    code = code.upper()
    code_info = code_service.get_code(code)
    if code_info is None:
        raise errors.DBError.DataValidationError(f"{code}는 없는 코드입니다.")

    log_channel = interaction.guild.get_channel(CLEAR_CHANNEL_ID)
    if log_channel is None:
        log_channel = await interaction.guild.fetch_channel(CLEAR_CHANNEL_ID)

    log_embed = discord.Embed(
        title="클리어 인증 요청",
        description=(
            f"**맵 코드:** `{code}`\n"
            f"난이도: `{code_info.difficulty.value}`\n"
            f"**기록:** {clear_time:.2f}초\n"
            f"**유저:** {interaction.user.mention} #{interaction.user.id}"
        ),
        color=discord.Color.green(),
    )
    log_embed.set_thumbnail(url=screenshot.url)
    cropped_file = await crop_image(screenshot)
    log_embed.set_image(url=f"attachment://{cropped_file.filename}")
    await log_channel.send(
        file=cropped_file,
        embed=log_embed,
        view=ClearLogView(),
        allowed_mentions=discord.AllowedMentions.none(),
    )

    embed = discord.Embed(
        title="✅ 요청 접수",
        description=(
            f"**맵 코드:** `{code}`\n"
            f"**기록:** {clear_time:.2f}초\n"
            f"**유저:** {interaction.user.mention} #{interaction.user.id}"
        ),
        color=discord.Color.green(),
    )
    embed.set_image(url=screenshot.url)
    await interaction.followup.send(embed=embed, ephemeral=True)


async def crop_image(screenshot: discord.Attachment) -> discord.File:
    image_bytes = await screenshot.read()

    img = Image.open(io.BytesIO(image_bytes))
    width, height = img.size

    if width > 450 or height > 300:
        cropped_img = img.crop((0, 0, 450, 300))
    else:
        cropped_img = img.crop((0, 0, width, height))
    
    output_buffer = io.BytesIO()
    cropped_img.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    file = discord.File(fp=output_buffer, filename="cropped_screenshot.png")

    return file