# quotes_db_commands.py
import sys
import time
from dbcon import *

# external modules
from nextcord.ext import commands



class Quotes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("QuotesDB cog loaded successfully")

    @commands.command(name="addquote", aliases=["запиши", "quote"], help="Увековечивает цитату в золотом фонде")
    async def add_quote(self, ctx, *args):
        cur = conn.cursor()
        quote = args[0]
        timestamp = None
        movieName = None
        try:
            for i in range(1, len(args)):
                if (':' in args[i]) and not (': ' in args[i]):
                    timestamp = args[i]
                if ': ' in args[i] or not (':' in args[i]):
                    movieName = args[i]
        except IndexError:
            timestamp = None
            movieName = None
        try:
            cur.execute(
                "insert into quotes (text, movieid, timestamp) values (%s, (select id from movies where title=%s), %s);",
                [quote, movieName, timestamp])
        except Exception:
            await ctx.send(sys.exc_info())
            cur.close()
        conn.commit()
        cur.close()
        await ctx.message.add_reaction("👍")

    @commands.command(name="quotesDB", aliases=["фонд","цитаты"], help="Ваш карманный фонд золотых цитат")
    async def print_quotesDB(self, ctx):
        text_list = list()
        time_list = list()
        movie_list = list()
        cur = conn.cursor()
        cur.execute("select text, title, timestamp from quotes left join movies on movieid=movies.id")
        for i in range(cur.rowcount):
            quote = cur.fetchone()
            text_list.append(quote[0])
            movie_list.append(quote[1])
            time_list.append(quote[2])
        for i in range(len(text_list)):
            toSend = str()
            toSend += '"' + text_list[i] + '"'
            if not (movie_list[i] is None): toSend += ' from "' + str(movie_list[i]) + '"'
            if not (time_list[i] is None): toSend += ' at ' + str(time_list[i])
            await ctx.send(toSend)
        # await ctx.send(quote_list)

    @commands.command(name="deletequote", aliases=["удали"], help="Удаляет цитату из фонда (but why would you do this?)")
    async def delete_quote(self, ctx, quote):
        cur = conn.cursor()
        cur.execute ("delete from quotes where text=%s", [quote])
        conn.commit()
        if (cur.statusmessage == "DELETE 0"): await ctx.message.add_reaction("❓")
        else: await ctx.message.add_reaction("⚡")
        #await ctx.send(cur.statusmessage)
        cur.close()

def setup(bot):
    bot.add_cog(Quotes(bot))
