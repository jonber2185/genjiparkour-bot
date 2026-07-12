import os
import logging
import discord
from discord import app_commands

logger = logging.getLogger(__name__)

DEV_USER_ID = int(os.getenv("DEV_USER_ID", "0"))
DEV_SECRET = os.getenv("DEV_SECRET", "")

MAX_ROWS = 50


def _is_developer(user_id: int) -> bool:
    return DEV_USER_ID != 0 and user_id == DEV_USER_ID


def is_developer():
    async def predicate(interaction: discord.Interaction) -> bool:
        return _is_developer(interaction.user.id)
    return app_commands.check(predicate)


class DBQueryModal(discord.ui.Modal, title="DB 쿼리 실행"):
    query = discord.ui.TextInput(
        label="SQL 쿼리",
        style=discord.TextStyle.paragraph,
        placeholder="SELECT * FROM users LIMIT 10;",
        required=True,
        max_length=3500,
    )
    secret = discord.ui.TextInput(
        label="보안 코드",
        style=discord.TextStyle.short,
        placeholder="보안 코드를 입력하세요",
        required=True,
        max_length=100,
    )

    async def on_submit(self, interaction: discord.Interaction):
        # 2차 방어: 개발자 본인이 아니면 무조건 차단
        if not _is_developer(interaction.user.id):
            logger.warning("DB 쿼리 시도 차단 (권한 없음): user=%s", interaction.user.id)
            await interaction.response.send_message("🚫 권한이 없습니다.", ephemeral=True)
            return

        # 3차 방어: 보안 코드 확인
        if not DEV_SECRET or self.secret.value != DEV_SECRET:
            logger.warning("DB 쿼리 시도 차단 (보안 코드 불일치): user=%s", interaction.user.id)
            await interaction.response.send_message("🚫 보안 코드가 올바르지 않습니다.", ephemeral=True)
            return

        sql = self.query.value.strip()
        logger.warning("[DB관리] 쿼리 실행: user=%s sql=%s", interaction.user.id, sql)

        from db.db_handler import db_handler

        try:
            conn = db_handler.conn
            cur = conn.cursor()
            cur.execute(sql)

            is_select = sql.lstrip()[:1].upper() in ("S", "W") and sql.lstrip().split(None, 1)[0].upper() in ("SELECT", "WITH")

            if is_select:
                rows = cur.fetchmany(MAX_ROWS)
                if not rows:
                    result_text = "(결과 없음)"
                else:
                    cols = rows[0].keys()
                    lines = [" | ".join(cols)]
                    for row in rows:
                        lines.append(" | ".join(str(row[c]) for c in cols))
                    result_text = "\n".join(lines)
                    if len(result_text) > 1900:
                        result_text = result_text[:1900] + "\n... (생략됨)"
                embed = discord.Embed(
                    title="✅ 쿼리 실행 완료",
                    description=f"```\n{result_text}\n```",
                    color=discord.Color.green(),
                )
                embed.set_footer(text=f"최대 {MAX_ROWS}행까지 표시됩니다.")
            else:
                conn.commit()
                embed = discord.Embed(
                    title="✅ 쿼리 실행 완료",
                    description=f"영향받은 행: {cur.rowcount}",
                    color=discord.Color.green(),
                )
        except Exception as e:
            logger.error("[DB관리] 쿼리 실행 실패: %s", e, exc_info=e)
            embed = discord.Embed(
                title="🚫 쿼리 실행 실패",
                description=f"```\n{e}\n```",
                color=discord.Color.red(),
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)


class DBQueryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(label="SQL 실행", style=discord.ButtonStyle.danger, emoji="🛠️")
    async def run_query(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not _is_developer(interaction.user.id):
            await interaction.response.send_message("🚫 권한이 없습니다.", ephemeral=True)
            return
        await interaction.response.send_modal(DBQueryModal())
        button.disabled = True

@app_commands.command(name="manage_db", description="개발자 전용 DB 관리 명령어")
@app_commands.default_permissions(administrator=True)
@is_developer()
async def db_admin_command(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🔒 개발자 전용 DB 관리 패널입니다. 버튼을 눌러 SQL을 입력하세요.",
        view=DBQueryView(),
        ephemeral=True,
    )
