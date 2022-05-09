# basic modules

# external modules
from nextcord.ext import commands

# local modules
from dbcon import db_load


class Movies(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("MoviesDB cog loaded successfully")

    @commands.command(name="add_movie", aliases=["am", "добавить_фильм", "дф"], help="Добавляет фильм в список, чтобы посмотреть его позже")
    async def add_movie(self, ctx, movie):
        movie = (movie, False)
        status = db_load("insert", "movies", movie)
        if status != "INSERT 0":
            await ctx.message.add_reaction("👍")
        else:
            await ctx.message.add_reaction("❓")

#    # debug command. Commented for the time being.
#    @commands.command(name="movies_all", aliases=[], help="Печатает список всех фильмов в БД")
#    async def print_movies(self, ctx):
#        movie_list = list()
#        cur = conn.cursor()
#        cur.execute("SELECT * FROM movies")
#        for _ in range(cur.rowcount):
#            movie_list += (cur.fetchone())
#        await ctx.send(movie_list)

    @commands.command(name="movies_watch", aliases=["movies", "movie", "кино", "фильмы"], help="Печатает список еще непросмотренных фильмов в БД")
    async def print_movies_unwatched(self, ctx):
        movie_list = db_load("select", "movies", "title", "not_watched")
        for movie in movie_list:
            await ctx.send(movie[0])

    @commands.command(name="delete_movie", aliases=["dm", "удали_фильм", "уф"], help="Удаляет фильм из базы данных")
    async def delete_movie(self, ctx, movie):
        status = db_load("delete", "movies", movie)
        if status != "DELETE 0":
            await ctx.message.add_reaction("⚡")
        else:
            await ctx.message.add_reaction("❓")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        emoji = payload.emoji.name
        if emoji == "👁️":
            channel = await self.bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            status = db_load("update", "movies", message.content)
            if status != "UPDATE 0":
                await message.add_reaction("👍")
            else:
                await message.add_reaction("❓")

#    @MovieBot.event
#    async def on_reaction_remove(self, reaction, user):
#        print('So, you have chosen oblivion.')
#        await reaction.message.channel.send(f'So, you have chosen oblivion.')
#        if user != MovieBot.user:
#            await reaction.message.channel.send(f'Увиденное не забудешь. Но я попробую.')
#            cur = conn.cursor()
#            cur.execute("update movies set watched=false where title=%s", [reaction.message.content])
#            conn.commit()
#            cur.close()

#    @commands.Cog.listener()
#    async def on_raw_reaction_add(self, payload):
#        print(payload)
#        channel = self.bot.get_channel(payload.channel_id)
#        if self.bot.get_user(payload.user_id) != self.bot.user:
#            await channel.send(f'Увиденное не забудешь. Но я попробую.')
#            cur = conn.cursor()
#            txt = await channel.fetch_message(payload.message_id)
#            cur.execute("update movies set watched=false where title=%s", [str(txt.content)])
#            conn.commit()
#            cur.close()


def setup(bot):
    bot.add_cog(Movies(bot))
