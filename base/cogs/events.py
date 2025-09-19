import discord
from discord.ext import commands

from base.config import BotConfig

from base.utils.embeds.event_embed import EmbedEvent
from base.utils.utilities import Utilities


class Events(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.utils = Utilities()
        self.config = BotConfig()

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        welcome_channel = self.bot.get_channel(self.config.WELCOME_CHANNEL_ID)

        if member.bot:
            await self.utils.ban_bot(member)

        await welcome_channel.send(embed=EmbedEvent().welcome_embed(member.guild, member))


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.channel.id == self.config.BOT_CHANNEL_ID:
            await message.channel.send("Du darfst hier keine Nachrichten senden.", delete_after=5)
            await message.delete()



def setup(bot: discord.Bot):
    bot.add_cog(Events(bot))