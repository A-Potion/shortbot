import discord
import os
from dotenv import load_dotenv
from discord import app_commands
import BitlyAPI

load_dotenv()

myguild = discord.Object(id=1255896898586280080)

class Bot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
            self.tree.copy_global_to(guild=myguild)
            await self.tree.sync(guild=myguild)

    async def on_ready(self):
        print(f"Logged on as {self.user}!")

intents = discord.Intents.default()
bot = Bot(intents=intents)

@bot.tree.command()
@app_commands.describe(
    url = "The link you'd like to shorten",
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int):
    """Shortens a link of your choice."""
    await interaction.response.send_message(f"{first_value} + {second_value} = {first_value + second_value}")

bot.run(os.getenv('TOKEN'))

