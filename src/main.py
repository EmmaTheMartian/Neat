# ANCHOR: Imports
import discord
import modutil
import os
import random
from typing import Union


# ANCHOR: Variables
bot = discord.Bot(
	activity = discord.CustomActivity(
		emoji = discord.PartialEmoji(name = 'sob'),
		name = 'Informing people about mods.'
	),
	description = 'Informs you about Neat, GregTech, Rats, and anything else you can find on CurseForge or Modrinth.',
	intents = discord.Intents(
		message_content = True,
		messages = True,
		presences = True,
	)
)


NO_PROFANITY = True
DISABLE_MEMES = False
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
	'unknown_mod_platform': lambda arg: f'Unknown mod platform: {arg}',
	'no_such_mod': lambda arg: f'No such mod: {arg}'
}


# ANCHOR: Utility functions
def embed(title: str, description: str, **kwargs):
	return discord.Embed(
		title = title,
		description = description,
		color = discord.Color.random(),
		**kwargs
	)

def error(code: str, *args):
	e = embed('Error', ERRORS[code](*args))
	e.color = discord.Color.dark_red()
	return e

_PLATFORMS = ['curseforge', 'modrinth', 'cf', 'mr']
def _get_platforms(c: discord.AutocompleteContext):
	return [p for p in _PLATFORMS if p.startswith(c.value.lower())]

def _get_category_filters(c: discord.AutocompleteContext):
	return [
		f for f in (
			modutil._CF_CATEGORIES if c.options['platform'] in {'cf', 'curseforge'} else
			modutil._MR_CATEGORIES if c.options['platform'] in {'mr', 'modrinth'} else
			[]
		) if f.startswith(c.value.lower())
	]

# ANCHOR: Bot events
@bot.listen('on_ready')
async def on_ready():
	print('Bot ready!')


@bot.listen('on_message')
async def on_message(msg):
	if DISABLE_MEMES or msg.author.bot:
		return

	content = msg.content.lower()
	words = [word.strip('!@#$%^&*()_+-=[]{}\\|~`;:\'",.<>/?') for word in content.split()]

	if content.startswith('what is spectrum'):
		await msg.reply(embed = embed('Spectrum', RESPONSE_SPECTRUM))
	elif 'neat' in words:
		await msg.reply(embed = embed('Neat', RESPONSE_NEAT, thumbnail = 'https://media.forgecdn.net/avatars/588/684/637958998850280257.png'))
	elif 'rat' in words:
		await msg.reply(embed = embed('Rat', RESPONSE_RAT))
	elif 'greg' in words or 'gregtech' in words:
		await msg.reply(embed = embed('Greg', RESPONSE_GREG))


# ANCHOR: Slash commands
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
		data = modutil.Mod.from_curseforge(int(slug))
	elif platform in {'mr', 'modrinth'}:
		data = modutil.Mod.from_modrinth(slug)
	else:
		await c.respond(embed = error('unknown_mod_platform', platform))
		return

	if data == 404:
		await c.respond(embed = error('no_such_mod', slug))
		return

	e = embed(data.name, data.summary)
	e.set_thumbnail(url = data.icon_url)
	e.add_field(name = 'By', value = ', '.join(data.authors))
	e.add_field(name = 'Downloads', value = data.downloads)
	e.add_field(name = 'URL', value = data.url)
	await c.respond(embed = e)


@bot.slash_command(name = 'search')
@discord.commands.option('platform', description = 'Platform', autocomplete = _get_platforms)
@discord.commands.option('query', description = 'Search query')
@discord.commands.option('category_filter', description = 'Apply a category filter (e.g, modpacks, mods, etc.)', default = 'mod', autocomplete = _get_category_filters)
@discord.commands.option('show_ids', description = 'If project IDs/Slugs should be shown', input_type = bool, default = False, required = False)
async def search(
    c,
	platform: str,
	query: str,
	category_filter: str,
	show_ids: bool
):
	mods = []
	if platform in {'mr', 'modrinth'}:
		mods = modutil.search_modrinth(query, category_filter)
	elif platform in {'cf', 'curseforge'}:
		mods = modutil.search_curseforge(query, category_filter)
	else:
		await c.respond(embed = error('unknown_mod_platform', platform))
		return

	await c.respond(embed = embed('Search Results', '\n'.join([
		f'- **{mod[0]}** ({mod[2]})' + ('' if not show_ids else f' [ID: {mod[1]}]') for mod in mods
	])))


# ANCHOR: if/main
if __name__ == '__main__':
	bot.run(os.environ['TOKEN'])
