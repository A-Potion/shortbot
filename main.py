import discord
import os
import requests
import json
import validators
from dotenv import load_dotenv
from discord import app_commands

if os.path.isfile(".env") == False:
    file = open(".env", "w")
    file.write(f'TOKEN = "{input("What`s your Discord bot`s token?\n")}"\n')
    file.write(f'BITLY = "{input("What`s your BitLy API key?\n")}"\n')
    file.write(f'ID = {input("What`s your Discord server ID?\n")}\n')
    file.close()


load_dotenv()

bitly_token = os.getenv("BITLY")

headers = {
  'Authorization': f'Bearer {bitly_token}',
  'Content-Type': 'application/json',
}

endpoint = 'https://api-ssl.bitly.com/v4/shorten'

myguild = discord.Object(id=str(os.getenv("ID")))

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
async def shorturl(interaction: discord.Interaction, url: str):
    """Shortens a link of your choice."""
    data = {
        'long_url': url,
        "domain": "bit.ly",
    }
    if validators.url(url) == True:
        response = requests.post(endpoint, headers = headers, data=json.dumps(data))
        shortened = json.loads(response.content)['link']
        embedVar = discord.Embed(title="Your shortened link is...", description = shortened, color = 0x00ff00)
        await interaction.response.send_message(embed=embedVar)
    else:
        embedVar = discord.Embed(title="Please enter a valid URL!", color=0xff0000)
        await interaction.response.send_message(embed=embedVar)

bot.run(os.getenv('TOKEN'))

