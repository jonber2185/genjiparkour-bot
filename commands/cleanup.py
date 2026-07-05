import os
from dotenv import load_dotenv
import discord
from discord.ext import tasks, commands
import logging
from db.services import user_service

load_dotenv()
SERVER_ID = os.getenv("DISCORD_SERVER_ID")
logger = logging.getLogger(__name__)


class CleanupCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cleanup_users.start()

    def cog_unload(self):
        self.cleanup_users.cancel()

    @tasks.loop(minutes=3)
    async def cleanup_users(self):
        logger.warning("청소 시작")
        
        try:
            guild = self.bot.get_guild(int(SERVER_ID))
            if not guild:
                logger.error("서버를 찾을 수 없습니다. SERVER_ID를 확인하세요.")
                return
        
            user_ids = user_service.get_all_users()
            delete_user_ids = []
            for user_id in user_ids:
                member = guild.get_member(user_id)
                if member is None: delete_user_ids.append(user_id)

            if delete_user_ids:
                logger.info(f"{len(delete_user_ids)}명 유저 삭제")
                user_service.delete_users(delete_user_ids)
        except Exception as e:
            logger.error(f"유저 삭제 중 오류 발생: {e}")
        finally:
            logger.warning("청소 종료")

    @cleanup_users.before_loop
    async def before_cleanup_users(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(CleanupCog(bot))