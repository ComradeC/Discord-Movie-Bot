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

    @commands.command(name="am", help="Добавляет фильм в список")
    async def add_movie(self, movie):
        movies = read("movie_list.json").get("movies").lower()
        movies.append(movie)
        write("movie_list.json", {"movies": movies})
        await self.bot.add_reaction(":+1:")

    @commands.command(name="movies", help="Печатает список фильмов")
    async def print_movie_list(self):
        await self.bot.send("Что бы посмотреть?")
        movies = read("movie_list.json").get("movies")
        for i in range(len(movies)):
            await self.bot.send(str(movies[i]).capitalize())

    @commands.command(name="dm", help="Удаляет фильм из списка")
    async def print_movie_list(self, movie):
        movies = read("movie_list.json").get("movies")
        for i in range(len(movies)):
            if movie.lower() == movies[i]:
                movies.pop(i)
        write("movie_list.json", {"movies": movies})
        await self.bot.add_reaction(":zap:")


def setup(bot):
    bot.add_cog(Movies(bot))
