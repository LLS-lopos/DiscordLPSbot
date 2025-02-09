import os

import discord
from discord import Message
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(dotenv_path=".token_bot")
token = os.getenv('DISCORD_TOKEN')
app_lopos_id = os.getenv('APP_ID')
app_lopos_token = os.getenv('LOPOS_APP_TOKEN')
bot_id = "1336162729106345984"


class BotLPS(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def on_ready(self):
        print(f"{self.user.display_name} est prêt et connecté!")
        try:
            synchronisation = await self.tree.sync()
            for i in synchronisation:
                print(f"commande: {i}")
        except Exception as e:
            print(e)

    async def on_member_join(self, membre):
        await self.get_channel(1336174883574513705).send(f"{membre.mention} vient d'arriver parmis nous")

    async def on_member_remove(self, membre):
        await self.get_channel(1336303100700393473).send(f"{membre.mention} nous a abondonné pour d'autre")

    async def on_message(self, message: Message, /) -> None:
        if message.author.bot: return
        if message.content.lower() in ["yo", "bonjours", "salut"]:
            await message.author.send("Salutation camarade")

    def test(self):
        @self.tree.command(name="test", description="Commende de test")
        async def test(interaction: discord.Interaction):
            await interaction.response.send_message("La commande de Test fonctionne bien !!!")

    def emojis(self):
        # utiliser les émojie personnaliser
        @self.tree.command(name="emoji", description="émoji propre au bot")
        async def emoji(interaction: discord.Interaction):
            # Vérifiez si l'interaction a lieu dans un serveur
            if interaction.guild is None:
                await interaction.response.send_message(
                    "Cette commande ne peut pas être utilisée dans un message direct.")
                return
            emojis = interaction.guild.emojis
            if not emojis:
                await interaction.response.send_message("Aucun émoji personnalisé trouvé sur ce serveur.")
                return

            # Créer une liste d'émojis à afficher
            emoji_list = [str(emoji) for emoji in emojis]
            await interaction.response.send_message("Voici la liste des émojis disponibles :\n" + "\n".join(emoji_list))

        @self.tree.command(name="choix_emoji", description="Choisissez un émoji personnalisé")
        async def choix_emoji(interaction: discord.Interaction, nom_emoji: str):
            # Trouver l'émoji par son nom
            emoji = discord.utils.get(interaction.guild.emojis, name=nom_emoji)

            if emoji:
                await interaction.response.send_message(f'Vous avez choisi l\'émoji : {emoji}')
            else:
                await interaction.response.send_message("Émoji non trouvé. Assurez-vous d'utiliser le bon nom.")

    def evenenent_clasique(self):
        pass

    def moderation(self):
        @self.tree.command(name="suppr", description="supprimer 'n' message")
        async def suppr(interaction: discord.Interaction, nombre: int):
            try:
                messages = []
                async for msg in interaction.channel.history(limit=nombre+1):
                    messages.append(msg)
                await interaction.channel.delete_messages(messages)
                await interaction.response.send_message(f"{nombre} messages supprimés avec succès.")
            except discord.Forbidden:
                await interaction.response.send_message("Je n'ai pas la permission de supprimer des messages.")
            except discord.HTTPException as e:
                await interaction.response.send_message(f"Erreur lors de la suppression des messages : {e.text}")

    def charger_bot(self):
        self.test()
        self.emojis()
        self.evenenent_clasique()
        self.moderation()
        super().run(token)


if __name__ == "__main__":
    bot = BotLPS()
    bot.charger_bot()
