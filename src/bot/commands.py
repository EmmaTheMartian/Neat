import discord
import consts
import util.autocomplete as autocomplete
import util.mod_util as mod_util
import util.option_util as option_util
import util.util as util


@consts.BOT.slash_command(name = 'mod')
@discord.commands.option('platform', description = 'Platform', autocomplete = autocomplete.simple(consts.PLATFORMS))
@discord.commands.option('slug', description = 'Project ID or Slug')
async def mod(
	c: discord.ApplicationContext,
	platform: str,
	slug: str
):
	platform = platform.lower()
	data = None

	if platform in {'cf', 'curseforge'}:
		data = mod_util.Mod.from_curseforge(int(slug))
	elif platform in {'mr', 'modrinth'}:
		data = mod_util.Mod.from_modrinth(slug)
	else:
		await c.respond(embed = util.error('unknown_mod_platform', platform))
		return

	if data == 404:
		await c.respond(embed = util.error('no_such_mod', slug))
		return

	e = util.embed(data.name, data.summary)
	e.set_thumbnail(url = data.icon_url)
	e.add_field(name = 'By', value = ', '.join(data.authors))
	e.add_field(name = 'Downloads', value = str(data.downloads))
	e.add_field(name = 'URL', value = data.url)
	await c.respond(embed = e)


@consts.BOT.slash_command(name = 'search')
@discord.commands.option('platform', description = 'Platform', autocomplete = autocomplete.simple(consts.PLATFORMS))
@discord.commands.option('query', description = 'Search query')
@discord.commands.option('category_filter', description = 'Apply a category filter (e.g, modpacks, mods, etc.)', default = 'mod', autocomplete = autocomplete.get_category_filters)
@discord.commands.option('show_ids', description = 'If project IDs/Slugs should be shown', input_type = bool, default = False, required = False)
async def search(
    c: discord.ApplicationContext,
	platform: str,
	query: str,
	category_filter: str,
	show_ids: bool
):
	mods = []
	if platform in {'mr', 'modrinth'}:
		mods = mod_util.search_modrinth(query, category_filter)
	elif platform in {'cf', 'curseforge'}:
		mods = mod_util.search_curseforge(query, category_filter)
	else:
		await c.respond(embed = util.error('unknown_mod_platform', platform))
		return

	if mods == None:
		await c.respond(embed = util.error('search_failed'))
		return

	if len(mods) > 0:
		await c.respond(embed = util.embed('Search Results', '\n'.join([
			f'- **{mod[0]}** ({mod[2]})' + ('' if not show_ids else f' [ID: {mod[1]}]') for mod in mods
		])))
	else:
		await c.respond(embed = util.embed('No results!', 'Check your spelling and category filters'))


@consts.BOT.slash_command(name = 'meme')
@discord.commands.option('meme', description = 'Meme to reply with', autocomplete = autocomplete.simple(consts.MEMES.keys()))
async def meme(
	c: discord.ApplicationContext,
	meme: str
):
	if meme not in consts.MEMES:
		await c.respond(embed = util.error('unknown_meme', meme))
		return

	await c.respond(embed = util.embed(consts.MEMES[meme][0], consts.MEMES[meme][1]))


@consts.BOT.slash_command(name = 'options')
@discord.default_permissions(administrator = True)
@discord.commands.option('mode', description = 'Mode for the command', autocomplete = autocomplete.simple({ 'set', 'get', 'info', 'getall' }))
@discord.commands.option('option', description = 'Option to configure', autocomplete = autocomplete.simple(option_util.OPTIONS.keys()), required = False)
@discord.commands.option('value', description = 'Value to set the option to', autocomplete = autocomplete.get_option_value, required = False)
async def options(
	c: discord.ApplicationContext,
	mode: str,
	option: str,
	value: str
):
	if option is not None:
		option = option.lower()
		if option not in option_util.OPTIONS:
			await c.respond(embed = util.error('unknown_option', option))
			return

	if c.guild is None:
		await c.respond(embed = util.error('guild_is_none'))
		return

	match mode:
		case 'set':
			o = option_util.OPTIONS[option]
			valid_values = o['values']
			if value not in valid_values:
				await c.respond(embed = util.error('invalid_value', value))
				return
			option_util.set_option(option, value, c.guild)
			await c.respond(embed = util.embed(o['name'], f'Set option to: {value}'))
		case 'get':
			await c.respond(embed = util.embed(option_util.OPTIONS[option]['name'], f'Current value: {option_util.get_option(option, c.guild)}'))
		case 'info':
			o = option_util.OPTIONS[option]
			e = util.embed(o['name'], o['info'])
			e.add_field(name = 'Allowed Values', value = ', '.join([f'`{v}`' for v in o['values']]))
			await c.respond(embed = e)
		case 'getall':
			e = util.embed('Current Settings', '')
			for o, data in option_util.OPTIONS.items():
				e.add_field(name = data['name'], value = option_util.get_option(o, c.guild))
			await c.respond(embed = e)
		case _:
			await c.respond(embed = util.error('unknown_mode', mode))
