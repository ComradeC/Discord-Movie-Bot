# bot.py
# version 0.1

import os
import json

from discord.ext import commands
from dotenv import load_dotenv


def read(filename):
    try:
        with open(filename, "r") as json_file:
            return json.loads(json_file.read())
    except FileNotFoundError:
        return {}


def write(filename, save_object):
    with open(filename, "w") as json_file:
        json_file.write(json.dumps(save_object))


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"{bot.user} к бою готов!")


@bot.command(name="hello", help="Поздоровайся, будь человеком")
async def hello(ctx):
    await ctx.send("Драсти")


@bot.command(name="add_movie", help="Добавляет фильм в список")
async def add_movie(ctx, movie):
    movies = read("movie_list.json").get("movies")
    movies.append(movie)
    write("movie_list.json", {"movies": movies})
    await ctx.send("Добавлено")


@bot.command(name="movies", help="Печатает список фильмов")
async def print_movie_list(ctx):
    await ctx.send("Что бы посмотреть?")
    movies = read("movie_list.json").get("movies")
    for i in range(len(movies)):
        await ctx.send(str(movies[i]))


@bot.command(name="add_quote", help="Добавляет цитату в золотой фонд")
async def add_quote(ctx, quote, movie="nomovie", timecode="0:0"):
    quotes = read("golden_quotes.json").get("quotes")
    quote_final = [quote, movie, timecode]
    quotes.append(quote_final)
    write("golden_quotes.json", {"quotes": quotes})
    await ctx.send("Добавлено")


@bot.command(name="quotes", help="Ваш карманный фонд золотых цитат")
async def print_golden_quotes(ctx):
    quotes = read("golden_quotes.json").get("quotes")
    await ctx.author.send("Пантеон великих цитат")
    for i in range(len(quotes)):
        await ctx.author.send(" - ".join(quotes[i]))

bot.run(os.getenv("TOKEN"))
