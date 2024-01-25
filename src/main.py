import discord
import modutil

bot = discord.Bot(
	activity = discord.CustomActivity(
		emoji = discord.PartialEmoji(name = 'sob'),
		name = 'Informing people about mods.'
	),
	description = 'Informs you about Neat, GregTech, Rats, and anything else you can find.'
)


NO_PROFANITY = True
RESPONSE_NEAT = 'Neat is a mod by Vazkii'
RESPONSE_GREG = '''STOP POSTING ABOUT GREGTECH, I'M TIRED OF SEEING IT! My friends on reddit send me memes, on discord it's ''' + ('' if NO_PROFANITY else 'fucking' ) + '''memes - I was in a subreddit, right? and ALLLLLLLLL of the POSTS are just GregTech stuff. I- I showed my Champion underwear to my girlfriend, and the logo I flipped it and I said, "Hey babe: When the underwear greg 😂 😂 😂"'''
RESPONSE_RAT = '''All I know how to do is reply "haha funny rat mod" every time someone says "rat" in the reddit comments. Is there more to life? Is there more to existence? I wouldn't know. It's not in my code.'''
RESPONSE_SPECTRUM = 'Spectrum is a mod by DaFuqs'
RESPONSE_RAT_SONG = '''rat
Hello darkness, my old friend...
I've come to talk with you again...
Because a vision softly cre-eeping,
Left its seeds while I was sle-eeping,
And the rat, that was planted, in my brain
Still remains...
Within the sound, of silence
'''
ERRORS = {
	'unknown_mod_platform': lambda arg: f'Unknown mod platform: {arg}'
}


def embed(title: str, description: str):
	return discord.Embed(title = title, description = description)

def error(code: str, *args):
	return embed('Error', ERRORS[code](*args))

_PLATFORMS = ['curseforge', 'modrinth', 'cf', 'mr']
def _get_platforms(c: discord.AutocompleteContext):
	return [p for p in _PLATFORMS if p.startswith(c.value.lower())]

@bot.listen('on_message')
async def on_message(msg):
	if msg.author.bot:
		return

	content = msg.content.lower()
	words = content.split()()

	if content.startswith('what is spectrum'):
		await msg.reply(embed('Spectrum', RESPONSE_SPECTRUM))
	elif 'neat' in words:
		await msg.reply(embed('Neat', RESPONSE_NEAT))
	elif 'rat' in words:
		await msg.reply(embed('Rat', RESPONSE_RAT))
	elif 'greg' in words or 'gregtech' in words:
		await msg.reply(embed('Greg', RESPONSE_GREG))


@bot.slash_command(name = 'mod')
@discord.commands.option('platform', description = 'Platform', autocomplete = _get_platforms)
@discord.commands.option('slug', description = 'Project ID or Slug')
async def mod(
	c: discord.ApplicationContext,
	platform: str,
	slug: str
):
	platform = platform.lower()
	data = None

	if platform in {'cf', 'curseforge'}:
		data = modutil.Mod.from_curseforge(slug)
	elif platform in {'mr', 'modrinth'}:
		data = modutil.Mod.from_modrinth(slug)
	else:
		await c.respond(embed = error('unknown_mod_platform', platform))
		return

	description =\
		f'''{data.summary}
		---
		By: {', '.join(data.authors)}
		---
		Downloads: {data.downloads}
		---
		URL: {data.url}'''.strip('\t ')

	await c.respond(embed = embed(data.name, description))


@bot.slash_command(name = 'search')
@discord.commands.option('platform', description = 'Platform', autocomplete = _get_platforms)
@discord.commands.option('query', description = 'Search query')
async def search(
    ctx,
	platform: str,
	query: str
):
	mods = []
	if platform in {'mr', 'modrinth'}:
		mods = modutil.search_modrinth(query)

    # search on Modrinth
    if platform == 'modrinth':
		mods = modutil.search_modrinth(query)
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
