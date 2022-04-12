# movies_commands.py

import discord
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

    @commands.command(name="movies", aliases=["movie", "кино", "фильмы"], help="Печатает список фильмов")
    async def print_movie_list(self, ctx):
        await ctx.send("Что бы посмотреть?")
        movies = read("DBs/movie_list.json").get("movies")
        for i in range(len(movies)):
            await ctx.send(str(movies[i]).capitalize())

    @commands.command(name="delete_movie", aliases=["dm", "у_фильм"], help="Удаляет фильм из списка")
    async def delete_movie(self, ctx, movie):
        movies = read("DBs/movie_list.json").get("movies")
        movies.remove(movie)
        write("DBs/movie_list.json", {"movies": movies})
        await ctx.message.add_reaction("⚡")


def setup(bot):
    bot.add_cog(Movies(bot))
