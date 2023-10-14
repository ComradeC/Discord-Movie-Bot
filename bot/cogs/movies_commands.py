# basic modules

# external modules
from nextcord.ext import commands
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, delete, update
import nextcord

# local modules
from .tools.id_lookup import id_gather
from .tools.settings import Session
from .tools.models import MovieModel


class Movies(commands.Cog, nextcord.ClientCog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Movies cog loaded successfully")

    @nextcord.slash_command(name="add_movie",
                            description="Добавляет фильм в список, чтобы посмотреть его позже",)
    async def add_movie(self, interaction: nextcord.Interaction, title):
        await interaction.response.defer(with_message="Just a sec...", ephemeral=True)
        ids = id_gather(title)
        kp_id = ids[0]
        imdb_id = ids[1]
        if interaction.guild_id:
            author = "public"
        else:
            author = str(interaction.user.id)

        try:
            with Session() as session:
                movie = MovieModel(title=title, watched_status=False, added_by=author, kp_id=kp_id, imdb_id=imdb_id)
                session.add(movie)
                session.commit()
                if author == "public":
                    await interaction.followup.send(f"Jobs done!")
                    msg = await interaction.channel.send(f"{title} has been added to the Movie List by"
                                                         f" {interaction.user.display_name}")
                else:
                    msg = await interaction.followup.send(f"{title} has been added to your personal Movie List")
                if kp_id:
                    emoji = "<\U0001F1F0>"  # "k" for kinopoisk
                    await msg.add_reaction(emoji)
                if imdb_id:
                    emoji = "<\U00002139>"  # "i" for imdb
                    await msg.add_reaction(emoji)
        except SQLAlchemyError:
            return await interaction.followup.send("Something went wrong.")

    @nextcord.slash_command(name="movies")
    async def movies(self, interaction: nextcord.Interaction):
        pass

    @movies.subcommand(description="Печатает список всех фильмов")
    async def all(self, interaction: nextcord.Interaction):
        # check for public/personal list
        if interaction.guild_id:
            author = "public"
        else:
            author = str(interaction.user.id)

        try:
            with Session() as session:
                query = select(MovieModel.title, MovieModel.watched_status).where(MovieModel.added_by == author)
                movie_list = session.execute(query)
        except SQLAlchemyError:
            return await interaction.followup.send("Something went wrong.")

        if author == "public":
            msg = await nextcord.PartialInteractionMessage.fetch(await interaction.
                                                                 response.send_message("Full movie list"))
            thread = await msg.create_thread(name="Full movie list", auto_archive_duration=1440)
            for movie in movie_list:
                msg = await thread.send(movie[0])
                if movie[1] is True:
                    await msg.add_reaction("👁️")
        else:
            await interaction.response.send_message("Your personal movie list:")
            for movie in movie_list:
                msg = await interaction.user.send(movie[0])
                if movie[1] is True:
                    await msg.add_reaction("👁️")

    @movies.subcommand(description="Печатает список еще непросмотренных фильмов")
    async def not_watched(self, interaction: nextcord.Interaction):
        # check for public/personal list
        if interaction.guild_id:
            author = "public"
        else:
            author = str(interaction.user.id)

        try:
            with Session() as session:
                movie_list = session.scalars(select(MovieModel.title).where(MovieModel.watched_status == "False").
                                             where(MovieModel.added_by == author))
        except SQLAlchemyError:
            return await interaction.followup.send("Something went wrong.")

        if author == "public":
            msg = await nextcord.PartialInteractionMessage.fetch(await interaction.response.send_message("Movie list"))
            thread = await msg.create_thread(name="Movie list", auto_archive_duration=1440)
            for movie in movie_list:
                await thread.send(movie)
        else:
            await interaction.response.send_message("Your unwatched movies:")
            for movie in movie_list:
                await interaction.user.send(movie)

    @nextcord.message_command(name="delete_movie")
    async def delete_movie(self, interaction: nextcord.Interaction, message: nextcord.Message):
        # check for public/personal list
        if interaction.guild_id:
            author = "public"
        else:
            author = str(interaction.user.id)

        try:
            with Session() as session:
                session.execute(delete(MovieModel).
                                where((MovieModel.title == message.content) & (MovieModel.added_by == author)))
                session.commit()
        except SQLAlchemyError:
            return await interaction.response.send_message("Something went wrong")
        await message.add_reaction("⚡")
        await interaction.response.send_message(f"Deleted {message.content}")

    @nextcord.message_command(name="set_watched")
    async def set_watched(self, interaction: nextcord.Interaction, message: nextcord.Message):
        # check for public/personal list
        if interaction.guild_id:
            author = "public"
        else:
            author = str(interaction.user.id)

        try:
            with Session() as session:
                session.execute(update(MovieModel).
                                where((MovieModel.title == message.content) & (MovieModel.added_by == author)).
                                values(watched_status=True))
                session.commit()
        except SQLAlchemyError:
            return await interaction.response.send_message("Something went wrong")
        await message.add_reaction("👁️")
        await interaction.response.send_message(f"Flagged {message.content} as watched")


def setup(bot):
    bot.add_cog(Movies(bot))
