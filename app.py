import os
import logging
from dotenv import load_dotenv
import discord
from discord.ext import commands
from db.db_handler import db_handler
from db.services import map_autocomplete_service, code_autocomplete_service

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
SERVER_ID = os.getenv("DISCORD_SERVER_ID")

logger = logging.getLogger(__name__)


class GenjiParkourBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = False
        intents.presences = False
        intents.members = True
        super().__init__(command_prefix=commands.when_mentioned, intents=intents)

    async def setup_hook(self):
        db_handler.connect()

        # init autocomplete
        map_autocomplete_service.load_memory()
        code_autocomplete_service.load_memory()

        from commands.anonymous._log_view import AnonymousLogView
        from commands.clear._log_view import ClearLogView
        self.add_view(AnonymousLogView(jump_url="https://discord.com"))
        self.add_view(ClearLogView())

        extensions = [
            ("commands.map",       "MapCommands"),
            ("commands.code",      "CodeCommands"),
            ("commands.anonymous", "AnonymousCommands"),
            ("commands.clear",     "ClearCommands"),
            ("errors.base",        "에러핸들러"),
            ("commands.cleanup",   "청소"),
        ]
        for ext, label in extensions:
            await self.load_extension(ext)
            logger.info("%s 로드 완료", label)

    async def on_ready(self):
        logger.info("로그인 -> %s", self.user.name)
        try:
            guild = discord.Object(id=int(SERVER_ID))
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            logger.info("command %d개 동기화 완료", len(synced))
        except Exception as e:
            logger.error("명령어 동기화 실패: %s", e)

    async def close(self):
        db_handler.close()
        await super().close()


if __name__ == "__main__":
    if not TOKEN or not SERVER_ID:
        logger.error("TOKEN 또는 SERVER_ID가 설정되지 않았습니다. .env를 확인하세요.")
    else:
        bot = GenjiParkourBot()
        bot.run(TOKEN)