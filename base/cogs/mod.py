import discord
from discord.ext import commands
from discord.commands import slash_command
from discord.ext.bridge import has_permissions

from base.config import BotConfig
from base.utils.embeds.clear_embed import EmbedClear


class Moderation(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.config = BotConfig()

    @slash_command(name="clear", description="Löscht eine bestimmte Anzahl von Nachrichten")
    @has_permissions(manage_messages=True)
    async def clear(self, ctx: discord.ApplicationContext, amount: int = 1):
        await ctx.channel.purge(limit=amount + 1, check=lambda m: not m.pinned)
        await ctx.respond(embed=EmbedClear().clear_embed(amount, ctx.guild.icon.url), ephemeral=True)

    @slash_command(name="clear_all", description="Löscht alle Nachrichten")
    @has_permissions(manage_messages=True)
    async def clear_all(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        total_deleted = 0

        for channel in ctx.guild.text_channels:
            try:
                deleted = await channel.purge(check=lambda m: not m.pinned)
                total_deleted += len(deleted)
            except discord.Forbidden as e:
                await ctx.respond(f"Es ist ein Fehler aufgetreten : {e}")

        await ctx.respond(embed=EmbedClear().clear_all_embed(total_deleted, ctx.guild.icon.url), ephemeral=True)

def setup(bot: discord.Bot):
    bot.add_cog(Moderation(bot))