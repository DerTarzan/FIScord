import aiofiles
import discord

from base.logger import Logger
from base.config import BotConfig

class Utilities:
    def __init__(self):
        self.config = BotConfig()
        self.logger = Logger(__name__).get_logger()

    def is_token_valid(self) -> bool:
        token = self.config.TOKEN
        return len(token) == 59

    @staticmethod
    async def ban_bot(bot) -> bool:
        try:
            await bot.ban(reason="Bot-Verbot")
        except Exception as e:
            return False

    async def load_streams_names(self):
        streams = []
        async with aiofiles.open(self.config.STREAMS_PATH, mode='r', encoding='utf-8') as file:
            content = await file.read()
            import json
            streams = json.loads(content)
            for stream in streams:
                stream.append("name")
        return streams

    async def check_bot_channel(self, ctx: discord.ApplicationContext) -> bool:
        if ctx.channel.id != self.config.BOT_CHANNEL_ID:
            await ctx.respond(f"Dieser Befehl kann nur im <#{self.config.BOT_CHANNEL_ID}> Kanal verwendet werden.", ephemeral=True)
            return False
        return True


    async def load_streams_url(self):
        streams = []
        async with aiofiles.open(self.config.STREAMS_PATH, mode='r', encoding='utf-8') as file:
            content = await file.read()
            import json
            streams = json.loads(content)
            for stream in streams:
                stream.append("url")
        return streams

