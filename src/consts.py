import re
import discord


BOT = discord.Bot(
	activity = discord.CustomActivity(
		emoji = discord.PartialEmoji(name = 'sparkles'),
		name = 'Informing people about mods.'
	),
	description = 'Informs you about Neat, GregTech, Rats, and anything else you can find on CurseForge or Modrinth.',
	intents = discord.Intents(
		message_content = True,
		messages = True,
		presences = True,
	)
)

RESPONSE_NEAT = 'Neat is a mod by Vazkii'
RESPONSE_GREG = '''STOP POSTING ABOUT GREGTECH, I'M TIRED OF SEEING IT! My friends on reddit send me memes, on discord it's fucking memes - I was in a subreddit, right? and ALLLLLLLLL of the POSTS are just GregTech stuff. I- I showed my Champion underwear to my girlfriend, and the logo I flipped it and I said, "Hey babe: When the underwear greg 😂 😂 😂"'''
RESPONSE_RAT = '''All I know how to do is reply "haha funny rat mod" every time someone says "rat" in the reddit comments. Is there more to life? Is there more to existence? I wouldn't know. It's not in my code.'''
RESPONSE_SPECTRUM = 'Spectrum is a mod by DaFuqs'
RESPONSE_RAT_SONG = '''Hello darkness, my old friend...
I've come to talk with you again...
Because a vision softly cre-eeping,
Left its seeds while I was sle-eeping,
And the rat, that was planted, in my brain
Still remains...
Within the sound, of silence
'''

MEMES = {
	'neat': ('Neat', RESPONSE_NEAT, 'https://media.forgecdn.net/avatars/588/684/637958998850280257.png'),
	'greg': ('Greg', RESPONSE_GREG, None),
	'rat': ('Rats', RESPONSE_RAT, None),
	'rat_song': ('rat', RESPONSE_RAT_SONG, None),
	'spectrum': ('Spectrum', RESPONSE_SPECTRUM, None),
}

PLATFORMS = { 'modrinth', 'curseforge', 'mr', 'cf' }

RE_NOT_ALPHANUMERIC = re.compile(r'[^a-zA-Z_\-0-9]', re.MULTILINE)
RE_PROFANITY = re.compile(f' ?(fucking) ?', re.MULTILINE)

EMMAS_ID = 647812268159008769
BOT_ID = 922212788053614602
