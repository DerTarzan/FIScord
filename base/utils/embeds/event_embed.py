import discord

from base.utils.embeds.base_embed import EmbedsBase
from base.utils.utilities import Utilities


class EmbedEvent(EmbedsBase):
    def __init__(self):
        self.utils = Utilities()
        super().__init__()

    def welcome_embed(self, guild: discord.Guild, member: discord.Member) -> discord.Embed:
        embed = discord.Embed(
            title="🛬 Willkommen",
            description=f"Willkommen {member.mention} auf {guild.name}.",
            color=self.INFO_COLOR
        )
        embed.set_thumbnail(url=member.avatar.url)

        return self.set_standard_footer_and_author(embed, guild.icon.url)