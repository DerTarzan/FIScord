import os
import asyncio
import random

import discord

from base.logger import Logger
from base.config import BotConfig
from base.utils.utilities import Utilities


logger = Logger(__name__).get_logger()


class Bot(discord.Bot):
    def __init__(self):
        self.config = BotConfig()
        self.utils = Utilities()
        super().__init__(intents=discord.Intents.all())

    def load_cogs(self, directory: str, is_root: bool = True) -> None:
        if is_root:
            logger.info("📦 Loading Cogs...")

        for filename in os.listdir(directory):
            if os.path.isdir(f'{directory}/{filename}'):
                self.load_cogs(f'{directory}/{filename}', is_root=False)
            elif filename.endswith('.py'):
                try:
                    self.load_extension(f'{directory.replace("/", ".")}.{filename[:-3]}')
                    logger.info(f'- ✅ Loaded Cog: {directory}/{filename}')
                except Exception as e:
                    logger.error(f'❌ Failed to load cog {filename}: {e}')
        if is_root:
            logger.info("🎉 All Cogs Loaded Successfully.")

    def create_coroutine_task(self, *coros) -> None:
        for coro in coros:
            if asyncio.iscoroutine(coro):
                logger.info(f" - ⚙️ Creating task for {coro.__name__}...")
                self.loop.create_task(coro)
            else:
                logger.error(f"❌ Invalid task: {coro} is not a coroutine.")

    async def on_ready(self) -> None:
        logger.info("=" * 50)
        logger.info(f"🤖 Bot Name      : {self.user.name}")
        logger.info(f"🆔 Bot ID        : {self.user.id}")
        logger.info(f"🏓 Latency       : {round(self.latency * 1000)} ms")
        logger.info("=" * 50)
        logger.info(f"🏰 Guild Name    : {self.guilds[0].name}")
        logger.info(f"🆔 Guild ID      : {self.guilds[0].id}")
        logger.info(f"👥 Member Count  : {self.guilds[0].member_count}")
        logger.info(
            f"👑 Owner         : {self.guilds[0].owner.name}#{self.guilds[0].owner.discriminator}, ID: {self.guilds[0].owner.id}")

        logger.info("-" * 50)

        logger.info("🔧 Creating presence update task...")
        self.create_coroutine_task(
            self.presence(),
        )

        logger.info("-" * 50)

        logger.info("FIScord Bot is now online. 🚀")

    async def presence(self) -> None:
        activities = [
            discord.Activity(type=discord.ActivityType.watching, name="the matrix 🖥️"),
            discord.Activity(type=discord.ActivityType.playing, name="compiling your fears 💻"),
            discord.Activity(type=discord.ActivityType.playing, name="deploying chaos 🚀"),
            discord.Activity(type=discord.ActivityType.playing, name="sudo make me a sandwich 🥪"),
            discord.Activity(type=discord.ActivityType.watching, name="echoing through the server 🌐"),
            discord.Activity(type=discord.ActivityType.playing, name="rm -rf / boredom"),
            discord.Activity(type=discord.ActivityType.playing, name="initializing brain.exe 🧠"),
            discord.Activity(type=discord.ActivityType.watching, name="accessing forbidden files 🔒"),
            discord.Activity(type=discord.ActivityType.playing, name="overclocking my thoughts ⚡"),
            discord.Activity(type=discord.ActivityType.watching, name="monitoring network traffic 📡"),
            discord.Activity(type=discord.ActivityType.watching, name="bridging VLANs 🔗"),
            discord.Activity(type=discord.ActivityType.watching, name="syncing with the mainframe 🖥️"),
            discord.Activity(type=discord.ActivityType.playing, name="updating firmware 🔧"),
            discord.Activity(type=discord.ActivityType.playing, name="patching reality 🪄"),
            discord.Activity(type=discord.ActivityType.watching, name="routing packets 🛰️"),
            discord.Activity(type=discord.ActivityType.watching, name="TCP handshake in progress 🤝"),
            discord.Activity(type=discord.ActivityType.playing, name="I void warranties 😎"),
            discord.Activity(type=discord.ActivityType.playing, name="Not a bot, just efficient 🤖"),
            discord.Activity(type=discord.ActivityType.playing, name="C:\\> _"),
            discord.Activity(type=discord.ActivityType.playing, name="In sudo we trust 💻"),
            discord.Activity(type=discord.ActivityType.playing, name="Overclocked caffeine intake ☕⚡"),
        ]

        while True:
            activity = random.choice(activities)
            await self.change_presence(activity=activity)
            await asyncio.sleep(random.randint(10, 20))  # alle 1–2 Minuten wechseln