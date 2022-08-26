# bot_start.py

# external modules
from nextcord.ext import commands
import nextcord


# local modules
from cogs.tools.settings import DISCORD_TOKEN

# cogs
from cogs import movies_commands, quotes_commands

intents = nextcord.Intents.all()

MovieBot = commands.Bot(command_prefix="!", intents=intents)
MovieBot.add_cog(movies_commands.Movies(MovieBot))
MovieBot.add_cog(quotes_commands.Quotes(MovieBot))


@MovieBot.event
async def on_ready():
    print(f"{MovieBot.user} к бою готов!")


@MovieBot.slash_command(name="hello", description="Поздоровайся, будь человеком", guild_ids=[962235918150955008, 757218832111763557])
async def hello(ctx):
    await ctx.send("Драсти")


MovieBot.run(DISCORD_TOKEN)
