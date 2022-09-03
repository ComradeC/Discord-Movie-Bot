# basic modules

# external modules
from nextcord.ext import commands
import nextcord

# local modules
from .tools.db_commands import db_add_movie, db_select, db_movie_set_watched, db_delete, db_select_all, db_movie_set_not_watched
from .tools.id_lookup import id_gather


class Movies(commands.Cog, nextcord.ClientCog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Movies cog loaded successfully")

    @nextcord.slash_command(name="add_movie",
                            description="Добавляет фильм в список, чтобы посмотреть его позже",
                            guild_ids=[962235918150955008, 757218832111763557])
    async def add_movie(self, interaction: nextcord.Interaction, title):
        await interaction.response.defer(with_message="Just a sec...", ephemeral=True)
        username = interaction.user.name
        ids = await id_gather(title)
        kp_id = ids[0]
        imdb_id = ids[1]

        status = db_add_movie(title, kp_id, imdb_id)
        if status == "Error":
            await interaction.followup.send("Something went wrong.")
        else:
            await interaction.followup.send(f"Jobs done!")

            msg = await interaction.channel.send(f"{title} has been added to the Movie List by {username}")
            if kp_id:
                emoji = "<\U0001F1F0>"  # "k" for kinopoisk
                await msg.add_reaction(emoji)
            if imdb_id:
                emoji = "<\U00002139>"  # "i" for imdb
                await msg.add_reaction(emoji)

    @nextcord.slash_command(name="movies",
                            guild_ids=[962235918150955008, 757218832111763557])
    async def movies(self, interaction: nextcord.Interaction):
        pass

    @movies.subcommand(description="Печатает список всех фильмов в БД")
    async def all(self, interaction: nextcord.Interaction):
        movie_list = db_select_all()

        msg = await nextcord.PartialInteractionMessage.fetch(await interaction.response.send_message("Full movie list"))
        thread = await msg.create_thread(name="Full movie list", auto_archive_duration=1440)
        for movie in movie_list:
            msg = await thread.send(movie[0])
            if movie[1] is True:
                await msg.add_reaction("👁️")

    @movies.subcommand(description="Печатает список еще непросмотренных фильмов в БД")
    async def not_watched(self, interaction: nextcord.Interaction):
        movie_list = db_select("movies")

        msg = await nextcord.PartialInteractionMessage.fetch(await interaction.response.send_message("Movie list"))
        thread = await msg.create_thread(name="Movie list", auto_archive_duration=1440)
        for movie in movie_list:
            await thread.send(movie)

    @nextcord.message_command(name="delete_movie",
                              guild_ids=[962235918150955008, 757218832111763557])
    async def delete_movie(self, interaction: nextcord.Interaction, message: nextcord.Message):
        status = db_delete("movies", message.content)
        if status == "Error":
            await message.add_reaction("❓")
            await interaction.response.send_message("Something went wrong")
        else:
            await message.add_reaction("⚡")
            await interaction.response.send_message(f"Deleted {message.content}")

    @nextcord.message_command(name="set_watched",
                              guild_ids=[962235918150955008, 757218832111763557])
    async def set_watched(self, interaction: nextcord.Interaction, message: nextcord.Message):
        db_movie_set_watched(message.content)
        await message.add_reaction("👁️")
        await interaction.response.send_message(f"Flagged {message.content} as watched")

    @nextcord.message_command(name="set_not_watched",
                              guild_ids=[962235918150955008, 757218832111763557])
    async def set_not_watched(self, interaction: nextcord.Interaction, message: nextcord.Message):
        db_movie_set_not_watched(message.content)
        await message.clear_reaction("👁️")
        await interaction.response.send_message(f"Flagged {message.content} as not watched")


def setup(bot):
    bot.add_cog(Movies(bot))
