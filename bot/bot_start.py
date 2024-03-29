# bot_start.py

# external modules
from nextcord.ext import commands, application_checks
import nextcord


# local modules
from cogs.tools.settings import DISCORD_TOKEN
from cogs.tools.ZeroTier import get_network_users
# cogs
from cogs import movies_commands, quotes_commands, polls_commands, karma_commands

intents = nextcord.Intents.all()

MovieBot = commands.Bot(command_prefix="!", intents=intents)
MovieBot.add_cog(movies_commands.Movies(MovieBot))
# MovieBot.add_cog(quotes_commands.Quotes(MovieBot))
MovieBot.add_cog(polls_commands.Polls(MovieBot))
# MovieBot.add_cog(karma_commands.Karma(MovieBot))


@MovieBot.event
async def on_ready():
    print(f"{MovieBot.user} к бою готов!")


@MovieBot.slash_command(name="hello", description="Поздоровайся, будь человеком")
async def hello(ctx):
    await ctx.send("Драсти")


@MovieBot.slash_command(name="zt", description="Табличка со статусом пользователей")
async def zt(ctx):
    network_name, network_users = get_network_users()
    message = f"```\n{network_name} users were last seen\n"
    for k, v in network_users().items():
        message += k + v + "\n"
    await ctx.send(message + "```")


@MovieBot.slash_command(name="permits")
@application_checks.has_permissions(create_public_threads=True)
async def test_perms(interaction: nextcord.Interaction):
    await interaction.response.send_message('You can create public threads.')


MovieBot.run(DISCORD_TOKEN)
