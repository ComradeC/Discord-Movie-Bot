# basic modules

# external modules
import nextcord
from nextcord.ext import commands
from nextcord import message

# local modules
from dbcon import db_add_movie, db_select, db_delete, db_movie_set_watched


class Movies(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("MoviesDB cog loaded successfully")

    @commands.command(name="add_movie", aliases=["am", "добавить_фильм", "дф"], help="Добавляет фильм в список, чтобы посмотреть его позже")
    async def add_movie(self, ctx, movie):
        status = db_add_movie(movie)
        if status == "Error":
            await ctx.message.add_reaction("❓")
        else:
            await ctx.message.add_reaction("👍")

    @commands.command(name="movies_watch", aliases=["movies", "movie", "кино", "фильмы"], help="Печатает список еще непросмотренных фильмов в БД")
    async def print_movies(self, ctx, *args):
        if args:
            movie_list = db_select("movies", args[0])
        else:
            movie_list = db_select("movies")

        msg = await ctx.send("Movie list")
        thread = await msg.create_thread(name="Movie list", auto_archive_duration=60)
        for movie in movie_list:
            await thread.send(movie)

    @commands.command(name="delete_movie", aliases=["dm", "удали_фильм", "уф"], help="Удаляет фильм из базы данных")
    async def delete_movie(self, ctx, movie):
        status = db_delete("movies", movie)
        if status == "Error":
            await ctx.message.add_reaction("❓")
        else:
            await ctx.message.add_reaction("⚡")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        emoji = payload.emoji.name
        if emoji == "👁️":
            channel = await self.bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            status = db_movie_set_watched(message.content)
            if status != "Error":
                await message.add_reaction("👍")
            else:
                await message.add_reaction("❓")


def setup(bot):
    bot.add_cog(Movies(bot))
