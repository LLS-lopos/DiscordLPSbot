import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()



bot = commands.Bot(command_prefix=">>>", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("test un 2, 1 deux ...")
    try:
        syncronisation = await bot.tree.sync()
        print(f"commande: {syncronisation}")
    except Exception as e: print(e)

# evenement au message
@bot.event
async def on_message(msg: discord.Message):
    # empecher au robot de se répondre à lui-même
    if msg.author.bot: return
    if msg.content.lower() in ['yo', 'salut', 'bonjours']:
        await msg.author.send("Ne me dérange plus")  # envoie un message en privé
        await msg.channel.send("salutation mon brave")  # envoie un message dans le salon où l'utilisateur se trouve
    if msg.content.lower() in ['bienvenue']:
        await bot.get_channel(1336174883574513705).send("Bienvenue")  # envoie un message dans un salon spécifique si l'utilisateur s'y trouve

# commande serveur
@bot.tree.command(name="test", description="Commende de test")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("La commande de Test fonctionne bien !!!")

bot.run(os.getenv('DISCORD_TOKEN'))