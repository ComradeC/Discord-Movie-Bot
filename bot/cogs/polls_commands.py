# polls_commands.py
import datetime
import random

# external modules
from nextcord.ext import commands
import nextcord

global view


class JoinButton(nextcord.ui.Button):

    def __init__(self, label, category_id):
        super().__init__()
        self.label = label
        self.cat_id = category_id

    async def join(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass

    async def callback(self, interaction: nextcord.Interaction):
        msg = interaction.message
        embed_dict = msg.embeds[0].to_dict()
        if embed_dict['fields'][self.cat_id]['value'] == "none":
            embed_dict['fields'][self.cat_id]['value'] = interaction.user.name
        elif interaction.user.name in embed_dict['fields'][self.cat_id]['value']:
            pass
        else:
            embed_dict['fields'][self.cat_id]['value'] += "\n" + interaction.user.name
        new_embed = nextcord.Embed.from_dict(embed_dict)
        await msg.edit(embed=new_embed)


class NewFieldModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("New category", timeout=5 * 60)
        self.category_name = nextcord.ui.TextInput("Category name", required=True)
        self.add_item(self.category_name)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        self.stop()


class ViewPoll(nextcord.ui.View):

    categories = ["Cringe", "Normal"]

    @nextcord.ui.button(label="New category", style=nextcord.ButtonStyle.blurple, row=3)
    async def new_category(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        msg = interaction.message
        embed_dict = msg.embeds[0].to_dict()
        modal = NewFieldModal()
        await interaction.response.send_modal(modal)
        await modal.wait()
        if modal.category_name.value.title() not in self.categories:
            embed_dict['fields'].append({'value': 'none',
                                         'name': f'{modal.category_name.value.title()}',
                                         'inline': True})
            new_embed = nextcord.Embed.from_dict(embed_dict)
            new_button = JoinButton(label=f"Join {modal.category_name.value.title()}", category_id=len(self.categories))
            self.categories.append(modal.category_name.value.title())
            view.add_item(new_button)
            await msg.edit(embed=new_embed, view=view)

    @nextcord.ui.button(label="Quit all", style=nextcord.ButtonStyle.red, row=3)
    async def callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        msg = interaction.message
        username = interaction.user.name
        embed_dict = msg.embeds[0].to_dict()
        for category in embed_dict['fields']:
            category['value'] = category['value'].replace(f"\n{username}", "")
            category['value'] = category['value'].replace(f"{username}", "")
            if category['value'] == "":
                category['value'] = "none"
        new_embed = nextcord.Embed.from_dict(embed_dict)
        await msg.edit(embed=new_embed)


class Polls(commands.Cog, nextcord.ClientCog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Polls cog loaded successfully")

    @nextcord.slash_command(name="poll",
                            guild_ids=[962235918150955008, 757218832111763557])
    async def poll(self, interaction: nextcord.Interaction):
        pass

    @poll.subcommand(description="Creates a new poll")
    async def create(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(title=f"Poll for {datetime.date.today()}", color=random.randint(0, 65535))
        embed.add_field(name="Cringe", value="none")
        embed.add_field(name="Normal", value="none")
        global view
        view = ViewPoll(timeout=3600 * 24)

        button_0 = JoinButton(label="Join Cringe", category_id=0)
        button_1 = JoinButton(label="Join Normal", category_id=1)
        view.add_item(button_0)
        view.add_item(button_1)
        await interaction.response.send_message(view=view, embed=embed)


def setup(bot):
    bot.add_cog(Polls(bot))
