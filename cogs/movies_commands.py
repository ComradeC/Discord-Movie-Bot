import psycopg2

# external modules
from nextcord.ext import commands

#conn = psycopg2.connect(dbname='moviebotdb', user='postgres', password='admin')     #local test connection
conn = psycopg2.connect(dbname='postgres', user='root', password='root')          #public server connection

class Movies(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("MoviesDB cog loaded successfully")


    @commands.command(name="add_movie", aliases=["movie", "фильм", "посмотреть"], help="Добавляет фильм в список, чтобы посмотреть его позже")
    async def addMovieDB(self, ctx, movie):
        cur = conn.cursor()
        cur.execute("INSERT INTO MOVIES (title, watched) values (%s, false);", [movie])
        conn.commit()
        cur.close()
        await ctx.message.add_reaction("👍")


    @commands.command(name="moviesall", aliases=[], help="Печатает список всех фильмов в БД")
    async def printMoviesDBAll(self, ctx):
        movie_list = list()
        cur = conn.cursor()
        cur.execute("SELECT * FROM movies")
        for i in range(cur.rowcount):
            movie_list += (cur.fetchone())
            # await ctx.send()
        await ctx.send(movie_list)


    @commands.command(name="movieswatch", aliases=["watch", "что посмотреть"], help="Печатает список еще несмотренных фильмов в БД")
    async def printMoviesDBUnwatched(self, ctx):
        cur = conn.cursor()
        cur.execute("SELECT title FROM movies where watched=false")
        for i in range(cur.rowcount):
            await ctx.send(cur.fetchone()[0])
        cur.close()


    @commands.command(name="deletemovie", aliases=["удалифильм"], help="Удаляет фильм из базы данных")
    async def delete_movie(self, ctx, movie):
        cur = conn.cursor()
        cur.execute("DELETE FROM movies WHERE title=%s", [movie])
        conn.commit()
        cur.close()
        await ctx.message.add_reaction("⚡")


def setup(bot):
    bot.add_cog(Movies(bot))
