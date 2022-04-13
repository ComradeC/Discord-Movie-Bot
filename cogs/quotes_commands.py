# quotes_commands.py

from nextcord.ext import commands
import json
import nextcord


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

    @commands.command(name="add_quote", aliases=["aq", "д_цитату"], help="Добавляет цитату в золотой фонд")
    async def add_quote(self, ctx, quote):
        quotes = read("DBs/golden_quotes.json").get("quotes")
        quotes.append(quote)
        write("DBs/golden_quotes.json", {"quotes": quotes})
        await ctx.message.add_reaction("👍")

    @commands.command(name="quotes", aliases=["quote", "цитаты"], help="Ваш карманный фонд золотых цитат")
    async def print_quotes(self, ctx):
        quotes_list = ""
        quotes = read("DBs/golden_quotes.json").get("quotes")
        for i in range(len(quotes)):
            quotes_list += (str(quotes[i]).capitalize()) + "\n"
        thread = await ctx.channel.create_thread(name="Quotes List", auto_archive_duration=60, type=nextcord.ChannelType.public_thread)
        await thread.send("```" + quotes_list + "```")

    @commands.command(name="delete_quote", aliases=["dq", "у_цитату"], help="Удаляет цитату из фонда")
    async def delete_quote(self, ctx, quote):
        quotes = read("DBs/golden_quotes.json").get("quotes")
        quotes.remove(quote)
        write("DBs/golden_quotes.json", {"quotes": quotes})
        await ctx.message.add_reaction("⚡")


async def setup(bot):
    await bot.add_cog(Quotes(bot))
