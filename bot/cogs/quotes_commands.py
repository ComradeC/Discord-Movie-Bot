# quotes_db_commands.py

# external modules
from nextcord.ext import commands
import re
import nextcord
# local modules
from .tools.db_commands import db_select, db_delete, db_add_quote, db_random_dow_quote


class Quotes(commands.Cog, nextcord.ClientCog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("QuotesDB cog loaded successfully")

    @nextcord.slash_command(name="add_quote",
                            description="Увековечивает цитату в золотом фонде",
                            guild_ids=[962235918150955008, 757218832111763557])
    async def add_quote(self, interaction: nextcord.Interaction, text, movie, timestamp):
        status = db_add_quote(text, movie, timestamp)
        if status == "Error":
            await interaction.response.send_message("Something went wrong.")
        else:
            await interaction.response.send_message(f'"{text}" from "{movie}" at {timestamp} is now part of the pantheon.')

    @nextcord.slash_command(name="quotes",
                            description="Ваш карманный фонд золотых цитат",
                            guild_ids=[962235918150955008, 757218832111763557])
    async def print_quotes(self, interaction: nextcord.Interaction):
        quotes_list = db_select("quotes")
        print(quotes_list)
        msg = await nextcord.PartialInteractionMessage.fetch(await interaction.response.send_message("Quotes list"))
        thread = await msg.create_thread(name="Quotes list", auto_archive_duration=60)
        for quote in quotes_list:
            print(quote)
            message = f'"{quote[0]}" from "{quote[1]}" at {quote[2]}'
            await thread.send(message)

    @nextcord.message_command(name="delete_quote",
                              guild_ids=[962235918150955008, 757218832111763557])
    async def delete_quote(self, interaction: nextcord.Interaction, message: nextcord.Message):
        text = re.match(r'.+?(?= from)', message.content)[0].replace('"', '')
        print(text)
        status = db_delete("quotes", text)
        if status == "Error":
            await message.add_reaction("❓")
            await interaction.response.send_message("Something went wrong")
        else:
            await message.add_reaction("⚡")
            await interaction.response.send_message(f'Deleted "{text}"')

    @nextcord.slash_command(name="dow_quote",
                            description="Выбирает случайную цитату из dow",
                            guild_ids=[962235918150955008, 757218832111763557])
    async def random_quote(self, interaction: nextcord.Interaction):
        quote = db_random_dow_quote()
        await interaction.response.send_message(quote)


def setup(bot):
    bot.add_cog(Quotes(bot))
