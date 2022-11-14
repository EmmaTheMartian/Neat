# imports
import discord
from discord import commands
import os
import sys
import requests


# variables
bot = discord.Bot(
    activity = discord.CustomActivity(
        emoji = discord.PartialEmoji(name = '📔'),
        name = 'Informing prople about mods.'
    ),
    description = 'This bot is really just a joke bot, but it has some utilities too. Keyword: some.'
)

headers = {
    'Accept': 'application/json',
    'x-api-key': os.getenv('CF_KEY')
}


# constants
RAT_POEM = '''All I know how to do is reply "haha funny rat mod" every time someone says "rat" in the reddit comments. Is there more to life? Is there more to existence? I wouldn't know. It's not in my code.'''

GREG_RANT = '''OMG😲😲 IS THAT👉 A MOTHER👨‍👩‍👧‍👦FUCKING😊 🌟GREGTECH🌟🔧🔧🔧🔧 REFERENCE!??!?!? GregTech🔧🔧🔧🔧 is the best mod ever made!!!! 🏆🏆GregoriousT for universe leadership 2030 🪐🌌 👑👑👑When the 只有格雷格。 is greggy! 🔧🛠️🔧🛠️🔧🛠️🔧🛠️ Ultra super mega extreme voltage tier 😳😳😳Death😵 by electrocution🔌 and vaporizing 🔥😄😄😄💀💀I have spent 1000 hours on GT:NH 😄🙂😐😕☹️💀What is grass??? 🌳🌲🌳🌲Sex and cum on behalf of Regian24 🥛😄GregTech 7 📣📣📣I am diagnosed with 17 separate mind conditions👍👍👍🏥'''


# gets a mod and returns the json data.
def get_mod(platform: str, slug: str):
    m = {
        'name': 'N/a',
        'authors': ['N/a'],
        'summary': 'N/a',
        'downloadCount': 0,
        'websiteUrl': 'N/a'
    }

    # Modrinth
    if platform in ('modrinth', 'md'):
        # get data
        data = requests.get(f'https://api.modrinth.com/api/v1/mod/{slug}').json()
        team_id = data['team']
        team_members = requests.get(f'https://api.modrinth.com/api/v1/team/{team_id}/members').json()
        members = []
        for m in team_members:
            mid = m['user_id']
            members.append(requests.get(f'https://api.modrinth.com/api/v1/user/{mid}').json()['username'])

        # set return values
        m['name'] = data['title']
        m['authors'] = members
        m['summary'] = data['description']
        m['downloadCount'] = data['downloads']
        m['websiteUrl'] = f'https://modrinth.com/mod/{slug}'
    # CF
    elif platform in ('curseforge', 'curse', 'cf'):
        # thanks to NikkyAI! The CF API is confusing...
        # get data
        data = requests.get(f'https://curse.nikky.moe/api/addon/{slug}').json()
        members = []
        for m in data['authors']:
            members.append(m['name'])

        # set return values
        m['name'] = data['name']
        m['authors'] = members
        m['summary'] = data['summary']
        m['downloadCount'] = data['downloadCount']
        m['websiteUrl'] = data['websiteUrl']
    
    # return... it says "return m"... **RETURN** m
    return m


# events
@bot.listen('on_message')
async def on_message(msg):
    if msg.author.bot: return 
    content = msg.content.lower().split()

    if 'neat' in content:
        await msg.reply(embed = discord.Embed(
            title = 'Neat',
            description = 'Neat is a mod by Vazkii'
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


# commands
@bot.slash_command()
async def mod(
    ctx,
    platform: commands.Option(str, 'Platform', choices=['curseforge', 'modrinth']),
    slug: commands.Option(str, 'Mod ID (Slug or Project ID)')
):
    '''Gets a mod, platform should be a mod platform, and slug is the CF ID, or the Modrinth slug.'''
    data = get_mod(platform, slug)
    await ctx.respond(embed = discord.Embed(
        title = data['name'],
        description = (data['summary'] +\
                '\n---\nBy: ' + ', '.join(data['authors']) +\
                '\n---\nDownloads: ' + str(data['downloadCount']) +\
                '\n---\nURL: ' + data['websiteUrl'])
    ))


@bot.slash_command()
async def search(
    ctx,
    platform: commands.Option(str, 'Platform', choices=['curseforge', 'modrinth']),
    search_text: commands.Option(str, 'Search Text')
):
    '''Searches for a mod with the provided text.'''
    mods = []
    
    # search on Modrinth
    if platform == 'modrinth':
        r = requests.get(f'https://api.modrinth.com/api/v1/mod?query={search_text}')
        for mod in r.json()['hits']:
            mods.append(f'- {mod["title"]} (**Slug**: *{mod["slug"]}*)\n')
    # search on CF
    elif platform == 'curseforge':
        r = requests.get(f'https://api.curseforge.com/v1/mods/search?gameId=432&categoryId=&searchFilter={search_text}', headers = headers)
        for mod in r.json()['data']:
            mods.append(f'- {mod["name"]} (**ID**: *{mod["id"]}*, **Slug**: *{mod["slug"]}*)\n')
    
    # send
    await ctx.respond(embed = discord.Embed(
        title = 'Search',
        description = ''.join(mods)
    ))


# main things
token = os.getenv('TOKEN')

if len(sys.argv) >= 2:
    token = sys.argv[1]
if len(sys.argv) >= 3:
    headers['x-api-key'] = sys.argv[2]

bot.run(token)

