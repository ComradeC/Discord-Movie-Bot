from discord.ext import commands
import psycopg2

conn = psycopg2.connect(dbname='moviebotdb', user='postgres', password='admin')


class MoviesDB(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("MoviesDB cog loaded successfully")


    @commands.command(name="add_movie", aliases=["movie", "фильм"], help="Добавляет фильм в список, чтобы посмотреть его позже")
    async def addMovieDB(self, ctx, movie):
        cur = conn.cursor()
        cur.execute("INSERT INTO MOVIES (title, watched) values (%s, false);", [movie])
        conn.commit()
        cur.close()
        await ctx.message.add_reaction("👍")


    @commands.command(name="movies_db_all", aliases=["movie_DB_all", "киноБДВсе", "фильмыБДВсе"], help="Печатает список всех фильмов в БД")
    async def printMoviesDBAll(self, ctx):
        movie_list = list()
        cur = conn.cursor()
        cur.execute("SELECT * FROM movies")
        for i in range(cur.rowcount):
            movie_list += (cur.fetchone())
            # await ctx.send()
        await ctx.send(movie_list)


    @commands.command(name="movies_to_watch", aliases=["watch", "что посмотреть", "Смотреть"], help="Печатает список еще несмотренных фильмов в БД")
    async def printMoviesDBUnwatched(self, ctx):
        cur = conn.cursor()
        cur.execute("SELECT title FROM movies where watched=false")
        for i in range(cur.rowcount):
            await ctx.send(cur.fetchone()[0])
        cur.close()


    @commands.command(name="delete_movie_DB", aliases=["dmDB", "у_фильмБД"], help="Удаляет фильм из базы данных")
    async def delete_movie(self, ctx, movie):
        cur = conn.cursor()
        cur.execute("DELETE FROM movies WHERE title=%s", [movie])
        conn.commit()
        cur.close()
        await ctx.message.add_reaction("⚡")


def setup(bot):
    bot.add_cog(MoviesDB(bot))
