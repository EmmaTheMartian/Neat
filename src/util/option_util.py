from typing import Any
import os
import json
import discord

# TODO: Replace this JSON-based system with a database
GUILD_OPTIONS: dict[str, dict[str, Any]] = {
	'disable_profanity': {},
	'disable_memes': {}
}

OPTIONS = {
	'disable_memes': {
		'name': 'Disable Memes',
		'info': 'Toggles if memes should be disabled. This will prevent the bot from replying automatically to messages containing ["neat", "greg", "rat", "what is spectrum"].',
		'cast': lambda obj: True if obj.lower() == 'true' else False,
		'values': ['True', 'False'],
		'default': False,
	},
	'disable_profanity': {
		'name': 'Disable Profanity',
		'info': 'Removes swears and profanity from any meme messages.',
		'cast': lambda obj: True if obj.lower() == 'true' else False,
		'values': ['True', 'False'],
		'default': False,
	},
}


def get_option(option: str, guild: discord.Guild):
	return OPTIONS[option]['default'] if str(guild.id) not in GUILD_OPTIONS[option] else GUILD_OPTIONS[option][str(guild.id)]


def set_option(option: str, value: str, guild: discord.Guild):
	v = OPTIONS[option]['cast'](value)
	# If the value is equal to the default, just delete it instead of saving the default value hundreds of times.
	# This is to reduce memory usage while the bot is running and will make file sizes smaller.
	if v == OPTIONS[option]['default']:
		del GUILD_OPTIONS[option][str(guild.id)]
	else:
		GUILD_OPTIONS[option][str(guild.id)] = v


def try_load(path: str):
	global GUILD_OPTIONS
	# TODO: set up a database to store this in rather than a JSON file.
	if os.path.exists(path):
		with open('options.json', 'r') as f:
			GUILD_OPTIONS = json.load(f)
		print('Loaded options.json')
		print(GUILD_OPTIONS)


def save(path: str):
	with open(path, 'w+') as f:
		json.dump(GUILD_OPTIONS, f)
	print('Saved options.json')
