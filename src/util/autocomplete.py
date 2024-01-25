from typing import Iterable
import discord
import util.option_util as option_util
import util.mod_util as mod_util


def simple(values: Iterable[str]):
	return lambda c: [a for a in values if a.startswith(c.value.lower())]


def get_category_filters(c: discord.AutocompleteContext):
	return simple(
		mod_util._CF_CATEGORIES if c.options['platform'] in {'cf', 'curseforge'} else
		mod_util._MR_CATEGORIES if c.options['platform'] in {'mr', 'modrinth'} else
		[]
	)(c)


def get_option_value(c: discord.AutocompleteContext):
	return simple(option_util.OPTIONS[c.options['option']]['values'])(c)
