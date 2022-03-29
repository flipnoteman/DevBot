import asyncio
import random
import pyjokes
import os

from dotenv import load_dotenv
from discord.ext import commands
from jokeapi import Jokes

load_dotenv('.env')

help_command = commands.DefaultHelpCommand(
    no_category='Commands'
)

bot = commands.Bot(command_prefix='!', description='This is a test Discord bot', help_command=help_command)


# Requests a joke with a given category from the jokeapi
async def send_joke(ctx, category):
    j = await Jokes()
    jke = await j.get_joke(category=[category])
    if jke["type"] == "single":
        await ctx.channel.send(jke["joke"])
    else:
        await ctx.channel.send(jke["setup"])
        await ctx.channel.send(jke["delivery"])


# this is the list of naughty words
badWords = ['matt', 'dobby', 'balls', 'big']
replace_characters = ['$', '!', '#', '!', '&', '*', '%']


# Detects if a user uses one of the words in the naughty word list
@bot.event
async def on_message(message):
    for i in badWords:
        if i in message.content.lower():
            await message.delete()
            await message.channel.send(
                f'{message.author.mention} Don\'t say {i.replace(i[1:len(i)], random.choice(replace_characters) * len(i))}'
            )
            return
    await bot.process_commands(message)


# Login Event
@bot.event
async def on_ready():
    print('We have logged in as TestDevBotBTG')


# Says a hardcoded Quote
@bot.command(name='99', help='Says a random phrase')
async def nine_nine(ctx):
    quotes = ['Helpfullinx is gay!', 'Buddybutter is not gay!', 'Bingo!', 'Reaper\'s Balls!']

    response = random.choice(quotes)
    await ctx.send(response)


# Rolls dice given number of dice and how many sides each dice has...
# Perfect for D&D playing scrubs in chat
@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = ''
    for _ in range(number_of_dice):
        dice += str(random.choice(range(1, number_of_sides + 1)))
        if _ < number_of_dice - 1:
            dice += ', '
    await ctx.send(dice)


@bot.command(
    name='joke//OLD//',
    brief='given (language, category) returns a random joke',
    help='Languages include: en, de, es, it, gl, eu\nCategories include: neutral (regular joke), twister (tongue '
         'twister), all '
)
async def joke(ctx, lang: str, category: str):
    myJoke = pyjokes.get_joke(lang, category)
    await ctx.channel.send(myJoke)


# Joke command that pulls from an online api
@bot.command(
    name='joke',
    brief='random joke from http://v2.jokeapi',
    help='Categories are:\n\tAny, Misc, Programming, Dark, Pun, Spooky, Christmas'
)
async def jokeapi(ctx, category: str):
    await send_joke(ctx, category)


# Pretty Self explanatory
@bot.command(name="laugh")
async def laugh(ctx):
    quote = ''
    for i in range(100):
        quote += 'Ha '
    await ctx.channel.send(quote)


started = False


@bot.command(name="ttt")
async def ttt(ctx):
    if not started:
        t = TTT()
        t.name1 = ctx.message.author
        t.ctx = ctx
        await t.start()


class TTT():
    def __init__(self):
        self.ctx = None
        self.name1 = 'No-one'

    async def start(self):
        name2 = ''
        await self.ctx.channel.send('{0} Started the app'.format(self.name1))
        await self.ctx.channel.send('Who else is playing? (use $me)')
        try:
            namemessage = await bot.wait_for(event='message', timeout=15.0)
        except asyncio.TimeoutError:
            await self.ctx.send('You didn\'t respond within 15 seconds')
            return
        else:
            if namemessage.content == "$me":
                name2 = self.ctx.message.author
            else:
                self.ctx.send('Wrong command')
        await self.ctx.send('Player 2 = {}'.format(name2))


# This is the identifier command that runs the bot. The text is the token of the bot
bot.run(os.getenv('TOKEN'))
