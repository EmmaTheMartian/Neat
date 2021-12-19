import discord
import sys

class Bot(discord.Client):
    async def on_message(self, msg):
        if 'neat' in msg.content.lower() and msg.author.bot is not True:
            await msg.channel.send(embed = discord.Embed(
                title = 'Neat',
                description = 'Neat is a mod by Vaskii'
            ))

Bot().run(sys.argv[1])

