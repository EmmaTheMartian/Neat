import os
import consts
import util.option_util as option_util


# Load events and commands
import bot.events
import bot.commands


# Actually run the bot :D
if __name__ == '__main__':
	option_util.try_load('options.json')
	consts.BOT.run(os.environ['TOKEN'])
	option_util.save('options.json')
