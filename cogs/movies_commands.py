import random
from dbcon import *


# external modules
import nextcord
#from nextcord.ext import commands
#from nextcord import client



class Movies(nextcord.ext.commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.ext.commands.Cog.listener()
    async def on_ready(self):
        print("MoviesDB cog loaded successfully")


    @nextcord.ext.commands.command(name="add_movie", aliases=["movie", "фильм", "посмотреть"], help="Добавляет фильм в список, чтобы посмотреть его позже")
    async def addMovieDB(self, ctx, movie):
        cur = conn.cursor()
        cur.execute("INSERT INTO MOVIES (title, watched) values (%s, false);", [movie])
        conn.commit()
        cur.close()
        await ctx.message.add_reaction("👍")


    @nextcord.ext.commands.command(name="moviesall", aliases=[], help="Печатает список всех фильмов в БД")
    async def printMoviesDBAll(self, ctx):
        movie_list = list()
        cur = conn.cursor()
        cur.execute("SELECT * FROM movies")
        for i in range(cur.rowcount):
            movie_list += (cur.fetchone())
            # await ctx.send()
        await ctx.send(movie_list)


    @nextcord.ext.commands.command(name="movieswatch", aliases=["watch", "смотреть"], help="Печатает список еще несмотренных фильмов в БД")
    async def printMoviesDBUnwatched(self, ctx):
        cur = conn.cursor()
        watchlist=list()
        repeats=list()
        m = 0
        cur.execute("SELECT title FROM movies where watched=false")
        for i in range(cur.rowcount):
            watchlist+=cur.fetchone()
        while (len(repeats)<5):
            j=random.randint(0,len(watchlist)-1)
            repeats.append(watchlist[j])
        for i in range(len(repeats)):
            msg = await ctx.send(repeats[i])
            await msg.add_reaction('☑')
        cur.close()

    @nextcord.ext.commands.command(name="deletemovie", aliases=["удалифильм"], help="Удаляет фильм из базы данных")
    async def delete_movie(self, ctx, movie):
        cur = conn.cursor()
        cur.execute("DELETE FROM movies WHERE title=%s", [movie])
        conn.commit()
        cur.close()
        await ctx.message.add_reaction("⚡")


def setup(bot):
    bot.add_cog(Movies(bot))
