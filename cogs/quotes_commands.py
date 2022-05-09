# quotes_db_commands.py

# external modules
from nextcord.ext import commands
# local modules
from dbcon import db_load


class Quotes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("QuotesDB cog loaded successfully")

    @commands.command(name="add_quote", aliases=["aq", "запиши", "quote"], help="Увековечивает цитату в золотом фонде")
    async def add_quote(self, ctx, *args):
        quote = args[0]
        timestamp = None
        movie_name = None
        try:
            for i in range(1, len(args)):
                if (':' in args[i]) and not (': ' in args[i]):
                    timestamp = args[i]
                if ': ' in args[i] or not (':' in args[i]):
                    movie_name = args[i]
        except IndexError:
            timestamp = None
            movie_name = None
        full_quote = (quote, movie_name, timestamp)
        status = db_load("insert", "quotes", full_quote)
        if status == "INSERT 0":
            await ctx.message.add_reaction("❓")
        else:
            await ctx.message.add_reaction("👍")

    @commands.command(name="quotes", aliases=["фонд", "цитаты"], help="Ваш карманный фонд золотых цитат")
    async def print_quotes(self, ctx):
        quotes_list = db_load("select", "quotes", "(text, movie_title, timestamp)")
        for quote in quotes_list:
            message = quote[0].replace(",", ", ").strip("()")
            await ctx.send(message)

    @commands.command(name="delete_quote", aliases=["dq", "удали"], help="Удаляет цитату из фонда (but why would you do this?)")
    async def delete_quote(self, ctx, quote):
        status = db_load("delete", "quotes", quote)
        if status == "DELETE 0":
            await ctx.message.add_reaction("❓")
        else:
            await ctx.message.add_reaction("⚡")


def setup(bot):
    bot.add_cog(Quotes(bot))
