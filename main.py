import discord
import os
import sys

RAT_POEM = '''
rat

Hello darkness, my old friend...

I've come to talk with you again...

Because a vision softly cre-eeping,

Left its seeds while I was sle-eeping,

And the rat, that was planted, in my brain

Still remains...

Within the sound, of silence
'''

GREG_RANT = '''
STOP POSTING ABOUT GREGTECH, I'M TIRED OF SEEING IT! My friends on reddit send me memes, on discord it's fucking memes - I was in a subreddit, right? and ALLLLLLLLL of the POSTS are just GregTech stuff. I- I showed my Champion underwear to my girlfriend, and the logo I flipped it and I said, "Hey babe: When the underwear greg 😂 😂 😂"
'''

class Bot(discord.Client):
    async def on_message(self, msg):
        if msg.author.bot: return
        
        content = msg.content.split()
        if 'neat' in content:
            await msg.reply(embed = discord.Embed(
                title = 'Neat',
                description = 'Neat is a mod by Vaskii'
            ))
        elif 'rat' in content:
            await msg.reply(embed = discord.Embed(
                title = 'Rat',
                description = RAT_POEM
            ))
        elif 'greg' in content:
            await msg.reply(embed = discord.Embed(
                title = 'Greg',
                description = GREG_RANT
            ))
        
        if msg.content.lower().startswith('what is spectrum'):
            await msg.reply(embed = discord.Embed(
                title = 'Spectrum',
                description = 'Spectrum is a mod by DaFuqs'
            ))

    async def on_ready(self):
        await bot.change_presence(
            status = discord.Status.online,
            activity = discord.CustomActivity(
                'Informing people about mods.',
                emoji = discord.PartialEmoji(
                    name = '📔'
                )
            )
        )

bot = Bot()

token = os.getenv('TOKEN')
if len(sys.argv) >= 2:
    token = sys.argv[1]

bot.run(token)

