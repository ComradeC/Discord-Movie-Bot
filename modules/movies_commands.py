# movies_commands.py

from discord.ext import commands
import json

import psycopg2
conn = psycopg2.connect(dbname='moviebotdb', user='postgres', password='admin')


def read(filename):
    try:
        with open(filename, "r") as json_file:
            return json.loads(json_file.read())
    except FileNotFoundError:
        return {}


def write(filename, save_object):
    with open(filename, "w") as json_file:
        json_file.write(json.dumps(save_object))


class Movies(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Movies cog loaded successfully")

    @commands.command(name="add_movie", aliases=["am", "д_фильм"], help="Добавляет фильм в список")
    async def add_movie(self, ctx, movie):
        movies = read("DBs/movie_list.json").get("movies")
        movies.append(movie)
        write("DBs/movie_list.json", {"movies": movies})
        await ctx.message.add_reaction("👍")

    @commands.command(name="add_movie_db", aliases=["amd", "д_фильм_бд"], help="Добавляет фильм в список, хранящийся в БД")
    async def addMovieDB(self, ctx, movie):
        cur=conn.cursor()
        cur.execute("INSERT INTO MOVIES (title, watched) values (%s, false);", [movie])
        conn.commit()
        cur.close()
        await ctx.message.add_reaction("👍")

    @commands.command(name="movies_db_all", aliases=["movie_DB_all", "киноБДВсе", "фильмыБДВсе"], help="Печатает список всех фильмов в БД")
    async def printMoviesDBAll(self, ctx):
        movie_list = ""
        cur=conn.cursor()
        cur.execute("SELECT * FROM movies")
        for i in range(cur.rowcount):
            movie_list += (cur.fetchone() + "\n")
        await ctx.send("```" + movie_list + "```")

    @commands.command(name="movies_to_watch", aliases=["movie_to_watch", "чтоПосмотреть", "Смотреть"],
                      help="Печатает список непросмотренных фильмов в БД")
    async def printMoviesDBUnwatched(self, ctx):
        cur = conn.cursor()
        movie_list = list()
        cur.execute("SELECT title FROM movies where watched=false")
        for i in range(cur.rowcount):
            movie_list += list(cur.fetchone())
        conn.commit()
        for i in range(len(movie_list)):
            print(movie_list[i])
        await ctx.send("```" + movie_list + "```")

    @commands.command(name="movies", aliases=["movie", "кино", "фильмы"], help="Печатает список фильмов")
    async def print_movie_list(self, ctx):
        movie_list = ""
        movies = read("DBs/movie_list.json").get("movies")
        for i in range(len(movies)):
            movie_list += (str(movies[i]).capitalize()) + "\n"
        await ctx.send("```" + movie_list + "```")

    @commands.command(name="delete_movie_DB", aliases=["dmDB", "у_фильмБД"], help="Удаляет фильм из базы данных")
    async def delete_movie(self, ctx, movie):
        cur = conn.cursor()
        cur.execute("DELETE FROM movies WHERE title=%s", [movie])
        conn.commit()
        cur.close()
        await ctx.message.add_reaction("⚡")

    @commands.command(name="delete_movie", aliases=["dm", "у_фильм"], help="Удаляет фильм из списка")
    async def delete_movie(self, ctx, movie):
        movies = read("DBs/movie_list.json").get("movies")
        movies.remove(movie)
        write("DBs/movie_list.json", {"movies": movies})
        await ctx.message.add_reaction("⚡")


def setup(bot):
    bot.add_cog(Movies(bot))
