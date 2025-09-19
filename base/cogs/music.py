import discord
from discord.ext import commands
from discord.commands import slash_command
import asyncio
import yt_dlp

from base.utils.utilities import Utilities

ffmpeg_options = {
    'options': '-vn'
}

ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True
}


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        ytdl = yt_dlp.YoutubeDL(ytdl_format_options)
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.utils = Utilities()
        self.queues = {}  # {guild_id: [YTDLSource, ...]}

    async def play_next(self, ctx, guild_id):

        if not self.utils.check_bot_channel(ctx):
            return

        if self.queues[guild_id]:
            next_song = self.queues[guild_id].pop(0)
            ctx.voice_client.play(next_song, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx, guild_id), self.bot.loop))
            await ctx.send(f"Jetzt spielt: **{next_song.title}**")
        else:
            await ctx.voice_client.disconnect()
            await ctx.send("Queue ist leer, ich habe den Voice-Channel verlassen.")

    @slash_command(name="play", description="Spielt ein YouTube-Video ab oder fügt es zur Queue hinzu")
    async def play(self, ctx: discord.ApplicationContext, url: str):

        if not self.utils.check_bot_channel(ctx):
            return

        await ctx.defer()
        if not ctx.author.voice:
            await ctx.respond("Du musst in einem Voice-Channel sein!", ephemeral=True)
            return

        channel = ctx.author.voice.channel
        voice_client = ctx.voice_client

        if not voice_client:
            voice_client = await channel.connect()

        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        guild_id = ctx.guild.id

        if guild_id not in self.queues:
            self.queues[guild_id] = []

        if voice_client.is_playing():
            self.queues[guild_id].append(player)
            await ctx.respond(f"**{player.title}** wurde zur Queue hinzugefügt.")
        else:
            voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx, guild_id), self.bot.loop))
            await ctx.respond(f"Jetzt spielt: **{player.title}**")

    @slash_command(name="queue", description="Zeigt die aktuelle Queue an")
    async def queue(self, ctx: discord.ApplicationContext):

        if not self.utils.check_bot_channel(ctx):
            return

        guild_id = ctx.guild.id
        if guild_id in self.queues and self.queues[guild_id]:
            msg = "\n".join([f"{i+1}. {song.title}" for i, song in enumerate(self.queues[guild_id])])
            await ctx.respond(f"Aktuelle Queue:\n{msg}")
        else:
            await ctx.respond("Die Queue ist leer.")

    @slash_command(name="skip", description="Überspringt das aktuelle Lied")
    async def skip(self, ctx: discord.ApplicationContext):

        if not self.utils.check_bot_channel(ctx):
            return

        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await ctx.respond("Das aktuelle Lied wurde übersprungen.")
        else:
            await ctx.respond("Es wird gerade keine Musik abgespielt.", ephemeral=True)

    @slash_command(name="stop", description="Stoppt die Musik und leert die Queue")
    async def stop(self, ctx: discord.ApplicationContext):

        if not self.utils.check_bot_channel(ctx):
            return

        guild_id = ctx.guild.id
        if ctx.voice_client:
            ctx.voice_client.stop()
            if guild_id in self.queues:
                self.queues[guild_id] = []
            await ctx.voice_client.disconnect()
            await ctx.respond("Die Musikwiedergabe wurde gestoppt und ich habe den Voice-Channel verlassen.")
        else:
            await ctx.respond("Ich bin in keinem Voice-Channel.", ephemeral=True)

    @slash_command(name="pause", description="Pausiert die aktuelle Musikwiedergabe")
    async def pause(self, ctx: discord.ApplicationContext):

        if not self.utils.check_bot_channel(ctx):
            return

        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await ctx.respond("Musik pausiert.")
        else:
            await ctx.respond("Es wird gerade keine Musik abgespielt.", ephemeral=True)

    @slash_command(name="resume", description="Setzt die pausierte Musikwiedergabe fort")
    async def resume(self, ctx: discord.ApplicationContext):

        if not self.utils.check_bot_channel(ctx):
            return

        voice_client = ctx.voice_client
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await ctx.respond("Musik wird fortgesetzt.")
        else:
            await ctx.respond("Die Musik ist nicht pausiert.", ephemeral=True)

def setup(bot: discord.Bot):
    bot.add_cog(Music(bot))
