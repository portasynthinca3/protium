#!/usr/bin/env pypy3

# Protium Discord bot created by portasynthinca3
# https://github.com/portasynthinca3/Protium

# constant messages
SUPPORTING = '''
You can tell your friends about this bot, as well as:
Donate money on Patreon: https://patreon.com/portasynthinca3
'''

BOT_INFO = '''
Hi!
This project was created by portasynthinca3 (https://github.com/portasynthinca3).
You can join our support server if you're experiencing any issues: https://discord.gg/N52uWgD.
Please consider supporting us (`/p support`).
'''

ANNOUNCEMENT = '''
idk what to put here \\(-_-)/
'''

# try importing libraries
import sys, os
import requests
import asyncio
import discord
from PIL import Image, ImageDraw, ImageFont
from pil_extensions import ExtendedImageDraw
from discord.ext.commands import Bot
from discord.errors import Forbidden
import time
from threading import Thread
import traceback
from discord.message import Message, MessageReference

# prepare constant embeds
EMBED_COLOR = 0xf99b16

HELP = discord.Embed(title='Protium', color=EMBED_COLOR)
HELP.add_field(inline=False, name=':loudspeaker: Latest Announcement', value=ANNOUNCEMENT)

HELP.add_field(inline=False, name=':exclamation: Usage', value='Just mention me when replying to a message! I\'ll pin the result if I have permission to do so')



PRIVACY = discord.Embed(title='Protium Privacy Policy', color=EMBED_COLOR)
PRIVACY.add_field(inline=False, name='1. SCOPE', value='''
This message describes the relationship between the Protium Discord bot ("Protium", "the bot", "bot"), its creator ("I", "me") and its Users ("you").''')
PRIVACY.add_field(inline=False, name='2. AUTHORIZATION', value='''
When you authorize the bot, it is added as a member of the server you've chosen. It has no access to your profile, direct messages or anything that is not related to the selected server.''')
PRIVACY.add_field(inline=False, name='3. DATA PROCESSING', value='''
Protium processes every message it receives, both in authorized server channels and in direct messages. I should note, however, that before your message goes directly to the code I wrote, it's first received by the discord.py library, which I trust due to it being open source.
When my code receives a direct message, it sends a simple response back and stops further processing.
Else, if the message is received in a server channel:
- the bot generates a quote image
- the bot pins said image if it has permission to do so''')
PRIVACY.add_field(inline=False, name='4. DATA STORAGE', value='''
Protium stores the following data:
- nothing''')
PRIVACY.add_field(inline=False, name='5. CONTACTING', value='''
You can contact me regarding any issues through E-Mail (`portasynthinca3@gmail.com`)''')
PRIVACY.add_field(inline=False, name='6. DATA REMOVAL', value='''
There\'s nothing to remove since no data is stored.''')
PRIVACY.add_field(inline=False, name='7. DATA DISCLOSURE', value='''
There\'s nothing to disclose since no data is stored.''')





# check if there is a token in the environment variable list
if 'PROT_TOKEN' not in os.environ:
    print('No bot token (PROT_TOKEN) in the list of environment variables')
    exit()
TOKEN = os.environ['PROT_TOKEN']

# create the temp folder
if not os.path.exists('temp'):
    os.mkdir('temp')

# load the fonts
nick_font = ImageFont.truetype('Montserrat-Black.otf', 60)
text_font = ImageFont.truetype('Montserrat-Bold.otf',  60)

bot = Bot(command_prefix='/p ', help_command=None)

def bot_presence_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while True:
        loop.run_until_complete(upd_bot_presence())
        time.sleep(10)

async def upd_bot_presence():
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.playing,
        name=f'around in {str(len(bot.guilds))} servers | "{bot.command_prefix}help" for help'
    ))

@bot.event
async def on_ready():
    Thread(target=bot_presence_thread, name='Presence updater').start()
    
    print('Everything OK!')

@bot.command(pass_context=True, name='help')
async def help_cmd(ctx):
    await ctx.send(embed=HELP)

@bot.command(pass_context=True, name='privacy')
async def privacy_cmd(ctx):
    await ctx.send(embed=PRIVACY)

@bot.command(pass_context=True, name='support')
async def privacy_cmd(ctx):
    await ctx.send(SUPPORTING)

@bot.command(pass_context=True, name='info')
async def info_cmd(ctx):
    await ctx.send(BOT_INFO)

# determines text size
def text_size(t):
    # temporary image
    return ImageDraw.Draw(Image.new('RGBA', (1, 1))).textsize(t, font=text_font)

# we need this because the bot has to train its message generation models
@bot.event
async def on_message(msg: discord.Message):
    channel = msg.channel

    # ignore bots
    if msg.author.bot:
        return

    # don't react to DMs
    if msg.guild == None:
        await channel.send(':x: **This bot only works in servers**')
        return

    # check if it's a command
    if msg.content.startswith(bot.command_prefix):
        # process the command and return
        await bot.process_commands(msg)
        return

    # get the referenced message
    ref = msg.reference
    if ref == None:
        return

    replied_to = ref.resolved
    if bot.user not in msg.mentions or type(replied_to) is not discord.Message:
        return

    if replied_to.content == '':
        return

    # limit line length to 100 chars
    text = replied_to.content
    max_l_width = 100
    text = '\n'.join(['\n'.join([l[i:i+max_l_width] for i in range(0, len(l), max_l_width)]) for l in text.split('\n')])

    # determine text size and all corresponding dimensions
    rt_w, rt_h  = text_size(text)
    t_w,  t_h  = max(rt_w, 856), max(rt_h, 386)
    mc_w, mc_h = t_w + 40, t_h + 40
    o_w,  o_h  = mc_w + 160, t_h + 40 + 178 + 160

    # create an image
    img = Image.new('RGBA', (o_w, o_h), color=(47, 49, 54, 255))
    d = ExtendedImageDraw(img)

    # download the avatar
    ava_path = f'temp/{replied_to.author.id}.png'
    with open(ava_path, 'wb') as a:
        a.write(requests.get(replied_to.author.avatar_url).content)
    ava = Image.open(ava_path)

    # draw the cards
    card_color = (30, 31, 34, 255)
    d.rounded_rectangle([(80, 80), (80 + mc_w, 80 + mc_h)], 20, card_color)
    d.rounded_rectangle([(80, 80 + mc_h + 40), (80 + mc_w, 80 + mc_h + 40 + 178)], 20, card_color)

    # draw the avatar
    ava = d.circled_image((140, 140), ava) # doesn't actually draw it
    img.paste(ava, (100, 80 + mc_h + 40 + 20), ava)

    # draw the text
    sent = discord.utils.snowflake_time(replied_to.id)
    nick = f'{replied_to.author.name}, {sent.year}'
    d.multiline_text((250, 80 + mc_h + 40 + 50), nick, font=nick_font, align='left')

    d.multiline_text((80 + ((mc_w - rt_w) // 2), 80 + ((mc_h - rt_h) // 2)), text, font=text_font, align='center')

    # save and send it
    img_path = f'temp/{replied_to.id}.png'
    img.save(img_path, 'PNG')
    m = await msg.channel.send(file=discord.File(img_path))
    os.remove(img_path)

    # pin it
    try:
        await m.pin()
    except Forbidden:
        pass

async def exception_handler(exctype, excvalue, exctraceback):
    if exctype is KeyboardInterrupt or exctype is SystemExit:
        sys.__excepthook__(exctype, excvalue, exctraceback)

    traceback.print_exception(exctype, excvalue, exctraceback)
    await (await bot.application_info()).owner.send(f':x: **Exception**\n```\n{str(excvalue)}\n```')

def exception_wrapper(exctype, excvalue, exctraceback):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(exception_handler)

sys.excepthook = exception_wrapper

bot.run(TOKEN)
