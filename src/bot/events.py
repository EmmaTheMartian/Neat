import re
import pprint
import discord
import consts
import util.util as util
import util.option_util as option_util


def _filter_profanity(string: str):
	return re.sub(consts.RE_PROFANITY, ' ', string)


@consts.BOT.listen('on_ready')
async def on_ready():
	print('Bot ready!')


@consts.BOT.listen('on_message')
async def on_message(msg: discord.Message):
	global _bot_restart

	if msg.author.bot:
		return

	# Bot owner debug stuff
	if msg.guild is None and msg.author.id == consts.EMMAS_ID and msg.content.startswith(f'<@{consts.BOT_ID}>'):
		match msg.content.replace(f'<@{consts.BOT_ID}>/', ''):
			case 'close':
				await consts.BOT.close()
			case 'ping':
				await msg.reply('Pong')
			case 'save_options':
				option_util.save('options.json')
				await msg.reply('Saved to options.json')
			case 'load_options':
				option_util.try_load('options.json')
				await msg.reply('Loaded options.json')
			case 'print_options':
				await msg.reply(pprint.pformat(option_util.GUILD_OPTIONS))
		return

	if msg.guild is None:
		await msg.reply(embed = util.error('guild_is_none'))
		return

	if option_util.get_option('disable_memes', msg.guild):
		return

	content = msg.content.lower()
	words = re.sub(consts.RE_NOT_ALPHANUMERIC, ' ', content).split()

	title = ''
	desc = ''
	thumbnail = None
	should_reply = False

	def set_to(meme: str):
		nonlocal title, desc, thumbnail, should_reply
		title = consts.MEMES[meme][0]
		desc = consts.MEMES[meme][1]
		thumbnail = consts.MEMES[meme][2]
		should_reply = True

	if content.startswith('what is spectrum'):
		set_to('spectrum')
	elif 'neat' in words:
		set_to('neat')
	elif 'rat' in words or 'rats' in words:
		set_to('rat')
	elif 'greg' in words or 'gregtech' in words:
		set_to('greg')

	if should_reply:
		await msg.reply(embed = util.embed(
			title,
			desc if not option_util.get_option('disable_profanity', msg.guild) else _filter_profanity(desc),
			thumbnail = thumbnail
		))
