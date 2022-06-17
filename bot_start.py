# bot_start.py

# external modules
import nextcord
from nextcord.ext import commands

# local modules
from bot.settings import DISCORD_TOKEN

# cogs
from bot.cogs import movies_commands, quotes_commands


MovieBot = commands.Bot(command_prefix="!", intends=nextcord.Intents.all())

MovieBot.add_cog(movies_commands.Movies(MovieBot))
MovieBot.add_cog(quotes_commands.Quotes(MovieBot))


@MovieBot.event
async def on_ready():
    print(f"{MovieBot.user} к бою готов!")


@MovieBot.command(name="hello", help="Поздоровайся, будь человеком")
async def hello(ctx):
    await ctx.send("Драсти")

MovieBot.run(DISCORD_TOKEN)
