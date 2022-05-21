# quotes_db_commands.py

# external modules
from nextcord.ext import commands
import re
# local modules
from dbcon import db_add_quote, db_select, db_delete


class Quotes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("QuotesDB cog loaded successfully")

    @commands.command(name="add_quote", aliases=["aq", "запиши", "quote"], help="Увековечивает цитату в золотом фонде")
    async def add_quote(self, ctx, *args):
        timecode_reg = r"\d?:?\d?\d:\d\d"
        timestamp = None
        movie_name = None
        text = args[0]
        for i in range(1, len(args)):
            if re.match(timecode_reg, args[i]):
                timestamp = args[i]
            else:
                movie_name = args[i]
        status = db_add_quote(text, movie_name, timestamp)
        if status == "Error":
            await ctx.message.add_reaction("❓")
        else:
            await ctx.message.add_reaction("👍")

    @commands.command(name="quotes", aliases=["фонд", "цитаты"], help="Ваш карманный фонд золотых цитат")
    async def print_quotes(self, ctx):
        quotes_list = db_select("quotes")
        msg = await ctx.send("Quotes list")
        thread = await msg.create_thread(name="Quotes list", auto_archive_duration=60)
        for quote in quotes_list:
            message = f"{quote[0]} {quote[1]} {quote[2]}"
            await thread.send(message)

    @commands.command(name="delete_quote", aliases=["dq", "удали"], help="Удаляет цитату из фонда (but why would you do this?)")
    async def delete_quote(self, ctx, quote):
        status = db_delete("quotes", quote)
        if status == "Error":
            await ctx.message.add_reaction("❓")
        else:
            await ctx.message.add_reaction("⚡")


def setup(bot):
    bot.add_cog(Quotes(bot))
