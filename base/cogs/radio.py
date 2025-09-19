import discord
from discord.ext import commands
from discord.commands import slash_command
from discord.ui import Select, View
import aiofiles
import json

from base.utils.utilities import Utilities


class RadioSelect(Select):
    def __init__(self, stations, callback):
        options = [
            discord.SelectOption(label=s["name"][:100], value=str(i))
            for i, s in enumerate(stations)
        ]
        super().__init__(placeholder="Wähle einen Radiosender", options=options)
        self.stations = stations
        self.callback_func = callback

    async def callback(self, interaction: discord.Interaction):
        await self.callback_func(interaction, self)


class RadioView(View):
    def __init__(self, stations):
        super().__init__(timeout=None)
        self.add_item(RadioSelect(stations, self.on_select))

    async def on_select(self, interaction: discord.Interaction, select: Select):
        index = int(select.values[0])
        station = select.stations[index]
        url = station["url"]
        name = station["name"]
        voice_state = interaction.user.voice

        if not voice_state or not voice_state.channel:
            await interaction.response.send_message(
                "Du bist in keinem Voice-Channel.", ephemeral=True
            )
            return

        # Verbindung zum Voice-Channel herstellen
        if interaction.guild.voice_client:
            vc = interaction.guild.voice_client
            if vc.channel != voice_state.channel:
                await vc.move_to(voice_state.channel)
        else:
            vc = await voice_state.channel.connect()

        # Sicherstellen, dass der Client verbunden ist
        if not vc.is_connected():
            await interaction.response.send_message(
                "Fehler beim Verbinden zum Voice-Channel.", ephemeral=True
            )
            return

        # Audio abspielen
        if vc.is_playing():
            vc.stop()
        vc.play(discord.FFmpegPCMAudio(url))

        await interaction.response.send_message(f"Spiele jetzt: **{name}**", ephemeral=True)


class Radio(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.utils = Utilities()
        self.bot = bot
        self.stations = []

    async def load_stations(self, path: str):
        async with aiofiles.open(path, mode="r", encoding="utf-8") as file:
            content = await file.read()
            self.stations = json.loads(content)

    @slash_command(name="radio", description="Zeigt eine Liste von verfügbaren Radiosendern an")
    async def radio(self, ctx: discord.ApplicationContext):

        if not await self.utils.check_bot_channel(ctx):
            return

        await ctx.defer(ephemeral=True)

        if not self.stations:
            await self.load_stations("base/data/streams.json")  # Pfad zu deiner JSON Datei

        if not self.stations:
            await ctx.respond("Keine Radiosender gefunden.", ephemeral=True)
            return

        view = RadioView(self.stations)
        await ctx.respond("Wähle einen Radiosender aus:", view=view, ephemeral=True)


def setup(bot: discord.Bot):
    bot.add_cog(Radio(bot))
