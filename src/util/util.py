import discord


ERRORS = {
	'unknown_mod_platform': lambda arg: f'Unknown mod platform: {arg}',
	'no_such_mod': lambda arg: f'No such mod: {arg}',
	'unknown_meme': lambda arg: f'No such meme: {arg}',
	'invalid_value': lambda arg: f'Invalid option value: {arg}',
	'unknown_mode': lambda arg: f'Unknown or invalid mode: {arg}',
	'guild_is_none': lambda: 'Guild is equal to `None`. This error should not happen, please report it!',
	'search_failed': lambda: 'Search failed'
}


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
