import discord


from base.utils.embeds.base_embed import EmbedsBase

class EmbedClear(EmbedsBase):
    def __init__(self):
        super().__init__()

    def clear_embed(self, amount: int, icon_url: str = "") -> discord.Embed:
        title = "🗑️ Nachricht gelöscht" if amount == 1 else "🗑️ Nachrichten gelöscht"
        description = (
            f"Es wurde {amount} Nachricht gelöscht"
            if amount == 1
            else f"Es wurden {amount} Nachrichten gelöscht"
        )

        embed = discord.Embed(
            title=title,
            description=description,
            color=self.INFO_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)

    def clear_all_embed(self, amount: int, icon_url: str = "") -> discord.Embed:
        embed = discord.Embed(
            title="🗑️ Es wurden alle Narichten gelöscht",
            description=f"Es wurden {amount} Narichten gelöscht",
            color=self.INFO_COLOR
        )
        return self.set_standard_footer_and_author(embed, icon_url)