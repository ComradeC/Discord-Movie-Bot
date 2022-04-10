# quotes_commands.py

from discord.ext import commands
import json


def read(filename):
    try:
        with open(filename, "r") as json_file:
            return json.loads(json_file.read())
    except FileNotFoundError:
        return {}


def write(filename, save_object):
    with open(filename, "w") as json_file:
        json_file.write(json.dumps(save_object))


class Quotes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Quotes cog loaded successfully")

    @commands.command(name="aq", help="Добавляет цитату в золотой фонд")
    async def add_quote(self, quote, movie="nomovie", timecode="0:0"):
        quotes = read("golden_quotes.json").get("quotes").lower()
        quote_final = [quote, movie, timecode]
        quotes.append(quote_final)
        write("golden_quotes.json", {"quotes": quotes})
        await self.bot.add_reaction(":+1:")

    @commands.command(name="quotes", help="Ваш карманный фонд золотых цитат")
    async def print_golden_quotes(self):
        quotes = read("golden_quotes.json").get("quotes")
        await self.bot.author.send("Пантеон великих цитат")
        for i in range(len(quotes)):
            await self.bot.author.send(" - ".join(quotes[i])).capitalize()

    @commands.command(name="dq", help="Удаляет цитату из фонда")
    async def print_golden_quotes(self, quote):
        quotes = read("golden_quotes.json").get("quotes")
        for i in range(len(quotes)):
            if quote.lower() in quotes[i]:
                quotes.pop(i)
        write("golden_quotes.json", {"quotes": quotes})
        await self.bot.add_reaction(":zap:")


def setup(bot):
    bot.add_cog(Quotes(bot))
