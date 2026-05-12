from curses.ascii import isalpha, isalnum
import argparse
import valkommen
import discord
from discord.ext import commands
from discord.utils import parse_time
import os # default module
import asyncio
import math
import re
import random
import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import aiosqlite
import io
from PIL import Image
from sympy import preview, symbols
from sympy.parsing.latex import parse_latex
import json
# from 
from uuid import uuid4
import subprocess
from ytmusicapi import YTMusic, OAuthCredentials
import yt_dlp
from yt_dlp import YoutubeDL
import av as pyav
from pathlib import Path
import num2words
import cv2
import numpy as np
asyncio.set_event_loop(asyncio.new_event_loop())

argparser = argparse.ArgumentParser()
argparser.add_argument("-g", "--graph", required=False, action="store_true")
g_args = argparser.parse_args( )
print(g_args)
load_dotenv() # load all the variables from the env file
if os.path.exists('welcome.db'):
    os.remove('welcome.db') 
def format_seconds(seconds):
    if seconds is None:
        return "No valid duration found."
    if seconds <= 0:
        return "0s"
    years = seconds // 31536000
    weeks = (seconds % (31536000)) // 604800
    days = (seconds % 604800) // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    parts = []
    if years > 0: parts.append(f"{years}y")
    if weeks > 0: parts.append(f"{weeks}w")
    if days > 0: parts.append(f"{days}d")
    if hours > 0: parts.append(f"{hours}h")
    if minutes > 0: parts.append(f"{minutes}m")
    if secs > 0: parts.append(f"{secs}s")

    return " ".join(parts)
def extract_video_id(url: str):
        regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
        match = re.search(regex, url)
        # print(match.group(1))
        return match.group(1) if match else None
    
# [Setup]
bot = discord.Bot()
# bot.load_extension('cogs.music')
# bot = commands.Bot(help_command=None)
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
intents.guilds = True
intents.moderation = True
intents.reactions = True

# intents.roles = True  
ytmusic = YTMusic(auth=str(Path(__file__).resolve().parent / "browser.json")
                #   oauth_credentials=OAuthCredentials(client_id=os.getenv("YTM_CLIENT_ID"), client_secret=os.getenv("YTM_CLIENT_SECRET"))
                  )
musPlaylist = 'PL0aPlkD5goIKuS2BKyCNsB9tJcIM36TW1'
# db = tdb('database.json')
# dbUser = Query()
# ytmusic.create_playlist("Test", "Test")
# print(ytmusic.get_library_playlists())
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
 # [/]
vowels = [
        'a',
        'i',
        'o',
        'u',
        'e'
    ]
# [latex1]
def getlatex(string):
    unique = uuid4()
    temp_fname = f"temp_{unique}.png"
    final_fname = f"final_{unique}.png"
    obj = io.BytesIO()
    send = True

    clean = (string).replace("_{ }", "").replace("^{ }", '').strip()
    clean = r"\begin{align*} " + clean + r"\end{align*}"
    latex = (
        r"\documentclass[varwidth, border=20pt]{standalone}"
        
        r"\usepackage{amsmath,amsfonts,amssymb}"
        r"\begin{document}"
        r"$$ " + clean + r" $$"
        r"\end{document}"
    )
    try:
        parse_latex(clean)
    except Exception:
        send = False
    if send:
        preview(clean, output='png', viewer='file', filename=temp_fname, dvioptions=['-D', '1000','-bg', 'Transparent', '-bd', '0'], euler=False)
        discord_bg = "#313338"
        subprocess.run([
            "magick", temp_fname,
            "-trim",
            "-fill", "white", "-opaque", "black",
            # "-negate",
            "-background", discord_bg,
            "-alpha", "remove", "-alpha", "off",
            "-bordercolor", discord_bg, "-border", "30",
            final_fname
        ], check=True)
        with open(final_fname, "rb") as f:
            obj = io.BytesIO(f.read())
        os.remove(temp_fname)
        os.remove(final_fname)
        obj.seek(0)
        return obj
    else:
        errobj = io.BytesIO()
        preview(r"\text{Error: not valid LaTeX}", output='png', viewer='file', filename=temp_fname)
        with open(temp_fname, "rb") as f:
            errobj = io.BytesIO(f.read())
        os.remove(temp_fname)
        errobj.seek(0)

        return errobj # [/]

@bot.command()
async def help(ctx):
    await ctx.reply("""
    # BOTWI HELP
    ```
    COMMANDS
    -------------------------------------
    IN #bot:
        !keewify -> converts latin text after a space into the keewish dialect of english 
        
        !dihify -> converts text after a space into dih language. just try it to know.
                        
        !getpfp {user} -> returns the profile picture of a user

        !getemoji {emoji} -> returns the image of the emoji sent by the user
        
        !getsticker -> returns the image of the sticker you reply to with the command

        !randomframe -> returns a completely random frame from a random keewi video (VODS and main channel)

        !gamble -> 5 !randomframes. The more people that use it, the longer it takes.
    IN #calculus-roleplay:
        !latex (!l) {LATEX} -> will return an image of the LaTeX you send.
    -------------------------------------
    BLUNDERBOARD
        react with four or more of :blunder: (<blunder:1443027776771719329>) to send a message to #board-of-shame. Works similarly to starboard.
    ```
    """)


@bot.event
async def on_ready():
    
    print(f"{bot.user} is ready and online!   {datetime.datetime.now()}")
    if g_args.graph:
        async with aiosqlite.connect("welcome.db") as wdb:
            await wdb.execute("PRAGMA journal_mode=WAL;")
            await wdb.execute("PRAGMA synchronous=NORMAL;")
            await wdb.execute("""
                CREATE TABLE IF NOT EXISTS welcome (
                    month            TEXT  PRIMARY KEY,
                    total            INTEGER,
                    increase         NUMERIC DEFAULT 0.0
                )
            """)
            print("Starting welcome build. . .")
            index = 0
            mdictionary = {}
            mdx = 0
            async for message in bot.get_channel(1283237643458711645).history(limit=None, oldest_first=True):
                print(f"\r{index + 1}/{3749}", end="")
                match = re.search(r"(?:#(\d+)|\b(\d+)(?:st|nd|rd|th)\b)", message.content)
                # print(match)
                month = f"{'0' if message.created_at.month < 10 else ''}{message.created_at.month}-{message.created_at.year - 2000}"
                if not month in mdictionary.keys():
                    mdx += 1
                    if match:
                        mdictionary[month] = {
                            "count": int(re.sub(r'[\D]', '', match.group(1) or match.group(2))),
                        }
                    else:
                        print(mdx)
                        mdictionary[month] = {
                            "count": int(mdictionary[list(mdictionary.keys())[mdx - 2]]["count"]),
                        }
                else:
                    if match:
                        mdictionary[month]["count"] = int(re.sub(r'[\D]', '',  match.group(1) or match.group(2)))
                if not "messages" in mdictionary[month].keys():
                    mdictionary[month]["messages"] = [message]
                    print("Hmm...")
                else:
                    mdictionary[month]["messages"].append(message)
                index += 1
            # print(*mdictionary.items(), sep="\n")
            for idx, (key, value) in enumerate(mdictionary.items()):
                print(key)
                # print(value)
                print(idx)
                if idx > 0:
                    print(mdictionary[key]["count"])
                    print(list(mdictionary.values())[idx - 1]["count"])
                    increase = round((mdictionary[key]["count"] - list(mdictionary.values())[idx - 1]["count"]) / value["count"], 4) * 100
                else:
                    increase = 0.0
                # print(mdictionary[key]["count"])
                # print(f"\n\n{list(mdictionary.values())[idx - 1]}")
                print(f" INCREASE \n\n {increase} \n\n")
                print(("VALUES:"))
                
                
                await wdb.execute(""" 
                    INSERT INTO welcome (month, total, increase)
                    VALUES (?, ?, ?)
                """, (key, value["count"], increase))

                await wdb.commit()

                await valkommen.main()
    async with aiosqlite.connect("timeoutdb.db") as db:
        await db.execute("PRAGMA journal_mode=WAL;")
        await db.execute("PRAGMA synchronous=NORMAL;")
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_timeouts (
                user_id INTEGER   PRIMARY KEY,
                duration_seconds INTEGER,
                timeout_count INTEGER DEFAULT 0,
                timestamp TEXT
            )
        """)
        
        await db.commit()
    async with aiosqlite.connect("warndb.db") as db:
        await db.execute("PRAGMA journal_mode=WAL;")
        await db.execute("PRAGMA synchronous=NORMAL;")
        await db.execute("""
            CREATE TABLE IF NOT EXISTS warns (
                user_id INTEGER PRIMARY KEY,
                warn_count INTEGER DEFAULT 0,
                reasons TEXT
            )
        """)
        
        await db.commit()
    if bot.get_guild(1283235301355159694).get_member(bot.user.id).nick != "":
        # await bot.get_channel(1440833959096352898).send(f"{bot.get_guild(1283235301355159694).get_member(bot.user.id).nick}: hello everybody my name is #welcome!")
        pass
    else:
        await bot.get_channel(1440833959096352898).send(f"{bot.user.display_name} is now online!")
    
# [Audit ( Temp )]

# @bot.slash_command(name= "temporary_audit")
# async def temporary_audit(ctx):
#     await ctx.defer()
#     found_stats = {}
#     async with aiosqlite.connect("timeoutdb.db") as db:
#         async for message in bot.get_channel(1419520700573679677).history(limit=10000):
#             for embed in message.embeds:
#                 content = f"{embed.title} {embed.description}".lower()
#                 # print(content)
#                 if "member timeout" in content:
#                     match = re.search(r'<@!?(\d+)>', content)
#                     if match:
#                         userid = int(match.group(1))
#                         if bot.get_user(userid) is not None:
#                             print(bot.get_user(userid).name)
#                         async with db.execute(
#                             "SELECT timeout_count FROM user_timeouts WHERE user_id = ?",
#                             (userid,)
#                         ) as cursor:
#                             print("Cursored...")
#                             row = await cursor.fetchone()
#                             count = row[0] if row else 0

#                             new_count = count + 1
#                             found_stats[userid]= count
#                             await db.execute("""
#                             INSERT INTO user_timeouts (user_id, timeout_count)
#                             VALUES (?, ?)
#                             ON CONFLICT(user_id) DO UPDATE SET
#                             timeout_count = EXCLUDED.timeout_count
#                             """, (userid, new_count))
#         await db.commit()
#         # if not found_stats:
#         #     await ctx.respond("No timeout messages found.")
#         #     return
    
#     await ctx.respond("Done.")

# [/]
    
    
# [Fun commands!]
    # [Keewify / Dihify FUNCTIONS]
def sentenceToKeewi(s): #string

    ignored = [
        # words that do not make sense in the context.
        "as",
        "is",
        "was",
        "case",
        "a",
        "of",
        "the",
        "by",
        "has",
        " ",
        "  ",
        "   ",
        "'s",
        "'nt",
        "'re",
        "than",
        "it",
        "and",
        "my",
        "also",
        "in",
        "hey",
        "i"
    ]
    punc = [
        ",",
        ".",
        ";",
        ":",
        "?",
        "!",
        "`",
        "```",
        "\"",
        "'",
        "[",
        "(",
        "{",
        "]",
        ")",
        "}",
        "<",
        ">",
        "_",
        "-",
        "=",
        "+",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "\\",
        "/",
        "|",
        "..."
    ]
    print(s)
    sentence = re.split(r'(\n)', s)
    print(sentence)
    temp = []
    for word in sentence:
        if word == "\n":
            temp.append(word)
        else:
            temp.extend(word.split())
    sentence = temp
    print(sentence)
    retsentence = []

    for index, i in enumerate(sentence):
        if i != "\n":
            w = i.strip().replace('k', 'kwi').replace('K', 'KWI')
            for z in range(3):
                if len(w) > 0:
                    if w[-1] in punc:
                        w = w[:-1]
            if len(w) < 2:

                if w != 'i' and w != 'a':
                    retsentence.append(w + 'wi')
                else:
                    retsentence.append(w + 'i')
            if len(w) > 1:
                if w[-1] == 'y' and len(w) > 2:
                    if w[-3:] == 'eey':
                        retsentence.append(w[:-1] + 'wi')
                    elif w[-2:] == 'ey':
                        retsentence.append(w + "wi")
                    else:
                        if not w[-2].lower() == 'e' and not w[-2].lower() == 'o':
                            retsentence.append(w[:-1] + 'eewi')
                        else:
                            if not w == 'boy':
                                retsentence.append(w + 'wi')
                            else:
                                retsentence.append(w[:-1] + 'eewi') # The Syno Exception

                else:
                    if not w.lower() in ignored and not w.lower()[-2:] == 'ed' and not w in punc and not w.lower()[-2:] in ignored and not w.lower()[-2:] == 'wi':
                        if w.lower()[-1] != 'w':
                            retsentence.append(w + 'wi')
                        else:
                            retsentence.append(w)
                    else:
                        retsentence.append(w)

            if i.strip()[-1] in punc:
                if not (i.strip()[-2:] == "``" or i.strip()[-3:] == "```" or i.strip()[-1:] == '`' or i.strip()[-3:] == "..."):
                    retsentence.append(i.strip()[-1:])
                else:

                    if i.strip()[-3:] == "```" or i.strip()[-3:] == "...":

                        retsentence.append(i[-3:].replace(" ", ""))
                    else:
                        if i.strip()[-1:] == "`":
                            retsentence.append(i.strip()[-1])
        else:
            retsentence.append("\n")

    # retsentence.pop(0)
    return ' '.join(retsentence)

def sentenceToDih(s):
    print(s)
    sentence = re.split(r'(\n)', s)
    print(sentence)
    temp = []
    for word in sentence:
        if word == "\n":
            temp.append(word)
        else:
            temp.extend(word.split())
    sentence = temp
    print(sentence)
    retsentence = []
    ignoredih = [
        'ld',
        're',
        'as',
        'ed'
    ]
    for index, i in enumerate(sentence):
        t1 = []
        for j in i:
            if isalnum(j):
                t1.append(j)
        if len(t1) < 2:
            retsentence.append(''.join(t1))
            continue

        if ''.join(t1[-2:]).lower() == 'ck' or ''.join(t1[-2:]).lower() == 'sh':
            t1.pop(-2)
            t1.pop(-1)
            t1.append('h')


        else:
            if t1[-2] in vowels:
                if t1[-1].lower() != 's' or t1[-1].lower() != 't' or t1[-2].lower() != 'o':
                    t1[-1] = 'h'
            elif t1[-1] in vowels:
                t1.append('h')
            else:
                if not ''.join(t1[-2:]).lower() in ignoredih:
                    t1.append('ih')
        print("t1" + str(t1))
        retsentence.append(''.join(t1))
        print(retsentence)
    return ' '.join(retsentence) # [/]
    # [Latex]
@bot.command()
async def latex(ctx, *, message_content):
    if ctx.message.channel.id == 1471758642003837123:
        f=discord.File(fp=getlatex(message_content.replace("!latex ", "")), filename="math.png")
        await ctx.send(file=f)
@bot.command()
async def l(ctx, *, message_content):
    if ctx.message.channel.id == 1471758642003837123:
        f=discord.File(fp=getlatex(message_content.replace("!l ", "")), filename="math.png")
        await ctx.send(file=f) # [/]
welcomemsgs = [ # I use an array to avoid clutter. If it didn't lead to clutter, I would absolutely
                # have this be an inline message.
    "You're now a shatling ",
    "Hey lil twin, you're looking gurtilicious today! <:emoji_53:1467954916533207091> ",
    "Hey shatling! Keewi isn't gay, nor is she ginger. <:O_O:1462370057194831873>",
    "Welcome to the Keewiverse. We have been awaiting your arrival. <:gurt:1461601994857775282>",
    "mrrrrp mrow mrrp mrrp mrow meeoowwww mrrp mrrp meow mrrp purrrr"
]
murdermsgs = [
    "AHHHHHHH!",
    "I TRUSTED YOU!",
    "thats evil",
    "<:emoji_53:1467954916533207091>",
    "what the FREAK bro",
    "that hurts",
    "zamn...",
    "hohoho! no. yueessss. no."
]
@bot.event
async def on_message(message):
    # print(message.content)
    if message.channel.id == 1298733690733592597:
        # print("Music....")
        if "youtu" in message.content and ".com" in message.content:
            vidID = extract_video_id(url=message.content)
            # print(repr(vidID))
            # print(type(vidID))
            # print(ytmusic.get_playlist(musPlaylist))
            await asyncio.to_thread(ytmusic.add_playlist_items, musPlaylist, [vidID])
    await bot.process_commands(message)
    # [Sillies!]
@bot.command()
async def keewify(ctx, *, message_content):
    if ctx.message.channel.id == 1468498879896096852:
        ret = sentenceToKeewi(message_content)
        print(ret)
        await ctx.send(f'{ret}')
@bot.command()
async def dihify(ctx, *, message_content):
    if ctx.message.channel.id == 1468498879896096852:
        ret = sentenceToDih(message_content)
        print(ret)
        await ctx.send(f'{ret}')
@bot.command()
async def murder(ctx, *, message_content):
    if ctx.message.channel.id == 1468498879896096852:
        print("Murdered.")
        await ctx.send(f'{message_content}: {random.choice(murdermsgs)}!')

@bot.command()
async def magic8ball(ctx: commands.Context):
    if ctx.message.channel.id == 1468498879896096852:

        await ctx.reply(f'{random.choice([
            'nnnno',
            'yueesss',
            'hohoho!',
            'ben.',
            'ough.',
            'no.'
        ])}')
 # [/]
@bot.command()
async def randomframe(ctx: commands.Context):
    if ctx.message.channel.id == 1468498879896096852:
        try:
            dlopts = {"extract_flat": True, 
                    "quiet": True,
                    "js_runtimes": {'node': {}}}
            with YoutubeDL(dlopts) as ydl:
                channel = await asyncio.to_thread(ydl.extract_info, url="https://www.youtube.com/@keewidraws/videos", download=False )
                channel2 = await asyncio.to_thread(ydl.extract_info, url="https://www.youtube.com/@KeewiExtras/videos",download=False)
                # Now convert to total
                
                videos = [video for video in (channel["entries"] + channel2["entries"]) 
                        if video and video.get("id")]
                randvid = random.choice(videos)
                vidurl = f"https://youtube.com/watch?v={randvid['id']}"
                vidinfo = None
                loops = 0
                while not vidinfo:
                    loops += 1
                    try:
                        randvid = random.choice(videos)
                        vidurl = f"https://youtube.com/watch?v={randvid['id']}"
                        vidinfo = await asyncio.to_thread(ydl.extract_info, vidurl, download=False)
                        
                        if loops > 10:
                            await ctx.reply("erm...i failed...im so sorry...")
                            return
                    except Exception:
                        continue
                # streamURL = vidinfo["url"]
                print(format_seconds(vidinfo["duration"]))
                frame = random.uniform(1, vidinfo["duration"])
                formats = vidinfo.get("formats", [])
                secrets = [
                    "NOBODY WILL EVER BELIEVE YOU. Just kidding, they will.",
                    "hai tin!",
                    "meow meow mrrp purr meow",
                    "yeah im getting your video just relax",
                    "GAMBLING GAMBLING GAMBLING"
                ]
                message = await ctx.reply(f"Got video...{random.choice(secrets)}")
                for ix, f in enumerate(formats):
                    
                    if f.get('height') == 360 and f.get('ext') == 'mp4' and '.m3u8' not in f.get('url'):
                        streamURL = f.get("url")
                        break
                if not streamURL:
                    streamURL = next((f.get('url') for f in formats if f.get('height') == 360), None)
                
                # print(formats)
                # print(frame)
                vidContainer = pyav.open(streamURL)
                # print(vidContainer)
                vidContainer.seek(math.floor(frame) * 1_000_000, any_frame=False)
                # print(vidContainer)
                vidFrame = next(vidContainer.decode(video=0))
                # print(vidFrame)
                # img = vidFrame.to_image()
                img = vidFrame.to_ndarray(format="bgr24")
                # buffer = io.BytesIO()
                uuid = uuid4()
                # img.save(f"{uuid}.jpg")
                cv2.imwrite(f"{uuid}.jpg", img)
                # buffer.seek(0)
                await message.edit(content=f"<{vidurl}> ({vidinfo.get("title", "Could not get title.")}), approximately {format_seconds(math.floor(frame))}", file=discord.File(f"{uuid}.jpg"))
                vidContainer.close()
                # buffer.close()
                os.remove(f"{uuid}.jpg")
        except Exception as e:
            await ctx.reply("erm...i failed...im so sorry...")
        # print(vidurl)

@bot.command()
async def gamble(ctx: commands.Context):
    if ctx.message.channel.id == 1468498879896096852:
        await ctx.send("Gambling! Gambling! Yay! \n-# please note this may take a bit.")
        uuids = []
        sendingfiles = []
        final_message = ""
        for attempt in range(5):
            try:
                dlopts = {"extract_flat": True, 
                        "quiet": True,
                        "js_runtimes": {'node': {}}}
                with YoutubeDL(dlopts) as ydl:
                    channel = await asyncio.to_thread(ydl.extract_info, url="https://www.youtube.com/@keewidraws/videos", download=False )
                    channel2 = await asyncio.to_thread(ydl.extract_info, url="https://www.youtube.com/@KeewiExtras/videos",download=False)
                    # Now convert to total
                    
                    videos = [video for video in (channel["entries"] + channel2["entries"]) 
                            if video and video.get("id")]
                    randvid = random.choice(videos)
                    vidurl = f"https://youtube.com/watch?v={randvid['id']}"
                    vidinfo = None
                    loops = 0
                    while not vidinfo:
                        loops += 1
                        try:
                            randvid = random.choice(videos)
                            vidurl = f"https://youtube.com/watch?v={randvid['id']}"
                            vidinfo = await asyncio.to_thread(ydl.extract_info, vidurl, download=False)
                            
                            if loops > 10:
                                await ctx.reply("erm...i failed...im so sorry...")
                                return
                        except Exception as e:
                            continue
                    # streamURL = vidinfo["url"]
                    print(format_seconds(vidinfo["duration"]))
                    frame = random.uniform(1, vidinfo["duration"])
                    formats = vidinfo.get("formats", [])
                    for ix, f in enumerate(formats):
                        
                        if f.get('height') == 360 and f.get('ext') == 'mp4' and '.m3u8' not in f.get('url'):
                            streamURL = f.get("url")
                            break
                    if not streamURL:
                        streamURL = next((f.get('url') for f in formats if f.get('height') == 360), None)
                    
                    # print(formats)
                    # print(frame)
                    vidContainer = pyav.open(streamURL)
                    # print(vidContainer)
                    vidContainer.seek(math.floor(frame) * 1_000_000, any_frame=False)
                    # print(vidContainer)
                    vidFrame = next(vidContainer.decode(video=0))
                    # print(vidFrame)
                    # img = vidFrame.to_image()
                    img = vidFrame.to_ndarray(format="bgr24")
                    # buffer = io.BytesIO()
                    uuid = uuid4()
                    uuids.append(uuid)
                    # img.save(f"{uuid}.jpg")
                    cv2.imwrite(f"{uuid}.jpg", img)
                    # buffer.seek(0)
                    sendingfiles.append( discord.File(f"{uuid}.jpg") )
                    final_message+= (f"<{vidurl}> ({vidinfo.get("title", "Could not get title.")}), approximately {format_seconds(math.floor(frame))}\n")
                    # await message.edit(content=, file=)
                    vidContainer.close()
                    # buffer.close()
                    
            except Exception as e:
                print(e)
                # await ctx.reply("erm...i failed...im so sorry...")
        await ctx.reply(files=sendingfiles, content=final_message)
        for uid in uuids:
            os.remove(f"{uid}.jpg")
        
# [/]



# ------------------------------

    # [Roles]
exclude = [
    641468688620584970,
    1405772116867158039,
    1493442279267106837,
    759712287396200479,
    900013076089294908
]

    # [List 16-17s]
@bot.command()
async def listss(ctx):
    print("listss")
    ids = [
        1285018696951140487,
        1403573321316040837,
        1287929568069554209,
        1446991754476916779
    ]

    allow = False
    for role in ctx.author.roles:
        if not allow:
            if role.id in ids:
                allow = True
    else:
        pass
    if allow:
        message = ""
        for user in ctx.guild.members:
            if user.joined_at.astimezone(ZoneInfo("US/Pacific")).date() > datetime.date(2026, 1, 17):
                for role in user.roles:
                    if role.id == 1283473032719110204 and not user.id in exclude:
                        if len(message) > 500:
                            await ctx.send(message)
                            message = ""
                        message += (f"<@{str(user.id)}> is a 16-17.\n")
        if not message == "":
            await ctx.send(message)
        else:
            await ctx.send("No 16-17s found! Teh...")
                        
@bot.command()
async def listssquiet(ctx):
    print("listss")
    ids = [
        1285018696951140487,
        1403573321316040837,
        1287929568069554209,
        1446991754476916779
    ]

    allow = False
    for role in ctx.author.roles:
        if not allow:
            if role.id in ids:
                allow = True
    else:
        pass
    if allow:
        message = ""
        for user in ctx.guild.members:
            if user.joined_at.astimezone(ZoneInfo("US/Pacific")).date() > datetime.date(2026, 1, 17):
                for role in user.roles:
                    if role.id == 1283473032719110204 and not user.id in exclude:
                        if len(message) > 500:
                            await ctx.send(message)
                            message = ""
                        message += (f"<@{str(user.id)}>\n")
        if not message == "":
            await ctx.send(message)
        else:
            await ctx.send("No 16-17s found! Teh...") # [/]
                        
ageroles = [
    1290492844838096956,
    1283473260003983430,
    1283473032719110204,
    1462320862383308962
]
    # [List roleless]
@bot.command()
async def listroleless(ctx):
    print("listroleless")

    ids = [
        1285018696951140487,
        1403573321316040837,
        1287929568069554209,
        1446991754476916779
    ]

    allow = False
    for role in ctx.author.roles:
        if not allow:
            if role.id in ids:
                allow = True



    message = ""
    total = 0
    if allow:
        for user in ctx.guild.members:
            if user.joined_at.astimezone(ZoneInfo("US/Pacific")).date() < datetime.datetime.now().astimezone(ZoneInfo("US/Pacific")).date() - datetime.timedelta(7):
                sendInMsg = False
                increment = 0
                total += 1
                for role in user.roles:
                    if role.id in ageroles:
                        increment += 1
                if increment < 1 and user.id != 1467664380949696665:    
                    message += (f"<@{str(user.id)}>")
                if len(message) + 30 >= 500:
                    await ctx.send(message)
                    message = ""
    if not message == "":
        await ctx.send(message)
        await ctx.send(str(total) + " Roleless members found.")
    else:
        await ctx.send("None of the Roleless were found! Teh...") # [/]
adminIds = [
        1285018696951140487,
        1403573321316040837,
        1287929568069554209,
        1446991754476916779
    ]               
    # [Add Roleless]
@bot.command()
async def addroleless(ctx):
    print("addroleless")

    

    allow = False
    for role in ctx.author.roles:
        if not allow:
            if role.id in adminIds:
                allow = True


    message = ""
    total = 0
    if allow:
        for user in ctx.guild.members:
            if user.joined_at.astimezone(ZoneInfo("US/Pacific")).date() < datetime.datetime.now().astimezone(ZoneInfo("US/Pacific")).date() - datetime.timedelta(7):
                perform = False
                for role in user.roles:
                    if role.id != 1462320862383308962 and not role.id in ageroles:
                        perform = True
                    else:
                        perform = False 
                if perform :
                    sendInMsg = False 
                    increment = 0
                    
                    canSend = True
                    for role in user.roles:
                        if role.id in ageroles:
                            increment += 1
                    if increment < 1 and user.id != 1467664380949696665 and user.id != 411916947773587456 and user.id != 557628352828014614:
                        print(f"Added {user.id}")
                        total += 1
                        await user.add_roles(ctx.guild.get_role(1462320862383308962))


                    if len(message) + 30 >= 500:
                        await ctx.send(message)
                        message = ""
    # if not message == "":
    #     await ctx.send(message)
    #     await ctx.send(str(total) + " members were found / roled.")
    if not canSend:
        await ctx.send("I have no kick permissions.")
    elif total > 1:
        await ctx.send(str(total) + f" members were found / roled. \n ** **")
    else:
        await ctx.send("No members were roled.") # [/]
 # [/]



# [Server stuff]
    # [GETPFP]

@bot.command()
async def getpfp(ctx, *, message_content):
    try:
        if ctx.message.channel.id == 1468498879896096852:
            if int(re.sub(r'\D','',message_content)):
        
                await ctx.send(bot.get_user(int(re.sub(r'\D','',message_content))).display_avatar)
    except Exception:
        await ctx.send(f"Could not get member {int(re.sub('[^0-9]','',message_content))}") # [/]

    # [GETEMOJI]
@bot.command()
async def getemoji(ctx, *, message_content):
    try:
        if ctx.message.channel.id == 1468498879896096852:
            if int(re.sub(r'\D','',message_content.split(' ')[0])):
                print()
                cleaned = int(re.sub(r'\D', '', message_content.split(' ')[0].split(":")[2].split(">")[0]))
                # cleaned = message_content
                print(cleaned)
                url = bot.get_emoji(cleaned).url
                if url.endswith('gif'):
                    await ctx.send(url[:-3] + "webp" + "?animated=true&quality=lossless")
                elif message_content.split(" ")[0].startswith("<a:"):
                    if url.endswith('webp'):
                        await ctx.send(url + "?quality=lossless&animated=true")
                else:
                    await ctx.send(url)
                # await ctx.send( (await ctx.guild.fetch_emoji(cleaned)).url)
    except Exception as e:
        print(e)
        await ctx.send(f"Could not get emoji.") # [/]

    # [GETSTICKER]
@bot.command()
async def getsticker(ctx):
    try:
        if ctx.message.channel.id == 1468498879896096852:
            
            cleaned = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            await ctx.send(bot.get_sticker(cleaned.stickers[0].id).url)
    except Exception:
        await ctx.send(f"Could not get sticker.") # [/]

    # [WELCOME]
@bot.event
async def on_member_join(member):
    # Due to how pycord works, this is the necessary implementation.
    # It must be added in every instance it is used.
    welcome = discord.utils.get(member.guild.text_channels, name='welcome')

    print(f"Member joined: {member.display_name}")
    x = random.randint(1, 100)
    match x:
        case num if num in range(1, 21):
            msg = welcomemsgs[0]
        case num if num in range(21, 41):
            msg = welcomemsgs[1]
        case num if num in range(41, 61):
            msg = welcomemsgs[2]
        case num if num in range(61, 81):
            msg = welcomemsgs[3]
        case num if num in range(81, 100):
            msg = welcomemsgs[4]
        case _:
            msg = "Welcome!" # This is just a default case.
    await welcome.send(f'-# <@{member.id}>\n{msg}! \n\nYou are member #{member.guild.member_count}! \n Make sure you get reactions roles from <#1283449236209270815>!')
 # [/]
    # [BAN]
@bot.event
async def on_member_ban(guild, user):

    welcome = bot.get_channel(1283237643458711645)
    print(f"Member banned: {user.display_name}")
    await welcome.send(f"<@{user.id}> was banned! Cya!")
 # [/]
    # [ERROR]
@bot.event
async def on_command_error(ctx, error):
    ignore_commands = [
        '!ban',
        '!timeout',
        '!kick'
    ]
    if not ctx.message.content.split(' ')[0].lower() in ignore_commands:
        print(f"Command sent with \n'{ctx.message.content}'\n errored in {ctx.guild} channel #{ctx.channel}.")
        print(f"error: {error}") # [/]



    # [REACTION THINGS]
@bot.event
async def on_reaction_add(reaction, user): 
    # print("Reaction added.")
        # [BLUNDERBOARD]
    blunderboard = bot.get_channel(1495212872417017897)
    try:
        if reaction.emoji.id == 1443027776771719329:
            # print("Blundered....")
            try:
                if reaction.count == 4:
                    print("BLUNDER...!")
                    myembed = discord.Embed(
                        title=f"Blunder! x{reaction.count}",
                        description = f"{reaction.message.content}\n\n[Jump to Message]({reaction.message.jump_url})",
                        color = discord.Color.blurple(),
                    )
                    myembed.set_author(name=reaction.message.author.display_name, icon_url=reaction.message.author.display_avatar)
                    myembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1443027776771719329.webp")
                    myembed.set_footer(text=f"{reaction.message.id}")
                    if reaction.message.attachments != []:
                        myembed.description += f"\n\n[Jump to Attachment]({reaction.message.attachments[0].url})",
                        myembed.set_image(url=reaction.message.attachments[0].url)
                    x = []
                    send = True
                    async for i in blunderboard.history(limit=100, oldest_first = False):
                        if not str(reaction.message.id) in i.embeds[0].footer.text:
                            pass
                        else:
                            send = False
                            break
                    if send:
                        await blunderboard.send(embed=myembed)
                elif reaction.count >= 5:
                    async for amessage in blunderboard.history(limit=100, oldest_first = False):
                        if amessage.embeds != []:
                            try:
                                if str(reaction.message.id) in amessage.embeds[0].footer.text:
                                    myembed = discord.Embed(
                                        title=f"Blunder! x{reaction.count}",
                                        description = f"{reaction.message.content}\n\n[Jump to Message]({reaction.message.jump_url})",
                                        color = discord.Color.blurple(),
                                    )
                                    myembed.set_author(name=reaction.message.author.display_name, icon_url=reaction.message.author.display_avatar)
                                    myembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1443027776771719329.webp")
                                    myembed.set_footer(text=f"{reaction.message.id}")
                                    if reaction.message.attachments != []:
                                        myembed.description += f"\n\n[Jump to Attachment]({reaction.message.attachments[0].url})",
                                        myembed.set_image(url=reaction.message.attachments[0].url)
                                    await amessage.edit(embed=myembed)
                            except AttributeError:
                                pass
            except AttributeError:
                pass
    except AttributeError:
        pass # [/]
    
    if reaction.message.channel.id == 1283449236209270815:
        norole = True
        for role in user.roles:
            if role in ageroles:
                norole = False
                break
        if not norole:
            await user.remove_roles(reaction.message.guild.get_role(1462320862383308962))
            # await reaction.message.guild.get_channel(1419520700573679677).send(f"Removed age role from <@{user.id}> due to removing it.")
    
@bot.event
async def on_reaction_remove(reaction, user):
    if reaction.message.channel.id == 1283449236209270815:
        norole = True
        for role in user.roles:
            if role in ageroles:
                norole = False
                break
        if norole:
            await user.add_roles(reaction.message.guild.get_role(1462320862383308962))
            await reaction.message.guild.get_channel(1419520700573679677).send(f"Removed age role from <@{user.id}> due to removing it.")
    # [/]
# ----------------------
    # [TIMEOUT STATUS]

@bot.slash_command(name = 'timeoutstatus')

async def timeoutstatus(ctx, *, id):
    # try:
    # await ctx.defer()
    allow = False
    for role in ctx.author.roles:
        if role.id in adminIds:
            print(role)
            allow = True
            break
    if allow:
        intid: int = int(re.sub(r'\D','',id))
        member = ctx.guild.get_member(intid)
        print(type(member))
        if type(member) is None:
            member = bot.get_user(intid)
        if type(member) is None:
            return await ctx.respond("Command errored.")
        # print(type(member.id))
        await ctx.send(f"Fetched {bot.get_user(intid).display_name}'s timeout status. . .")
        if intid:
            
            
            await ctx.defer()
            async with aiosqlite.connect("timeoutdb.db") as db:
                async with db.execute(
                    "SELECT duration_seconds, timeout_count, timestamp FROM user_timeouts WHERE user_id = ?",
                    (member.id,)
                ) as cursor:
                    row = await cursor.fetchone()
                    print("Executed...")
                    print(row)
                    if row:
                        duration, count, last_time = row
                        myembed = discord.Embed(
                            title=f"Timeout status for: {member.id}",
                            description = f"Stats for: <@{member.id}>\n\n"
                            f"Timeout count: {count}\n"
                            f"Last duration: {format_seconds( duration)}\n",

                            color = discord.Color.red(),
                        )
                        myembed.set_author(name=member.display_name, icon_url=member.display_avatar)
                        await ctx.respond(
                            embed=myembed
                        )
                    else:
                        await ctx.respond(f"No information found for <@{member.id}>")
    else:
        await ctx.send("You do not have the necessary permissions to do that.")
    # except Exception as e:
        # await ctx.respond(f"Could not get member {intid}. {e}")

# [/]

    # [Auditlog]
@bot.event

async def on_audit_log_entry(entry: discord.AuditLogEntry):
    print(entry)
    if entry.action == discord.AuditLogAction.member_update:
        if hasattr(entry.after, 'communication_disabled_until'):
            t_id = entry._target_id
            until = entry.after.communication_disabled_until
            if until is not None:
                print("Inserting...")
                seconds = int((parse_time(entry.after.communication_disabled_until) - discord.utils.utcnow()).total_seconds())
                now = discord.utils.utcnow().isoformat()
                async with aiosqlite.connect("timeoutdb.db") as db:
                    await db.execute("""
                    INSERT INTO user_timeouts (user_id, duration_seconds, timeout_count, timestamp)
                    VALUES (?, ?, 1, ?)
                    ON CONFLICT(user_id) DO UPDATE SET
                        duration_seconds = excluded.duration_seconds,
                        timeout_count = timeout_count + 1,
                        timestamp = excluded.timestamp
                    """, (entry._target_id, seconds, now))

                    await db.commit() # [/]

    # [WARN]
@bot.command()
async def warn(ctx, *, message_content):
    separated = message_content.split('>')
    allow = False
    # await ctx.defer()
    try:
        for role in ctx.author.roles:
            if role.id in adminIds:
                allow = True
                break

        if len(separated) > 1:
            pass
        else:
            await ctx.reply("Could not get blank text / warn user without a reason.")
        if allow:
            async with aiosqlite.connect("warndb.db") as db:
                async with db.execute("""
                    SELECT reasons FROM warns WHERE user_id = ?
                """, (re.sub(r'\D','',separated[0]),)) as cursor:
                    row = await cursor.fetchone()
                
                reasons = json.loads(row[0]) if row else []
                reasons.append(''.join(separated[1:]).strip())
                await db.execute("""
                INSERT INTO warns (user_id, warn_count, reasons)
                VALUES (?, 1, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    warn_count = warn_count + 1,
                    reasons = excluded.reasons
                """, (re.sub(r'\D','',separated[0]), json.dumps(reasons)))
                async with db.execute("""
                    SELECT warn_count FROM warns WHERE user_id = ?""",
                (re.sub(r'\D','',separated[0]),)) as cursor:
                    countrow = await cursor.fetchone()
                await db.commit() 
                print(re.sub(r'\D','',separated[0]))
                username = await ctx.guild.fetch_member(re.sub(r'\D','',separated[0]))
                await ctx.reply(f"Warned user: {username.display_name}. This is their {num2words.num2words(countrow[0], to='ordinal', lang='en')} warn.")
                try:
                    timeoutlength = 3600 * (countrow[0]** (countrow[0] * 2))
                    print(timeoutlength)
                    print(ctx.guild.name)
                    member = await ctx.guild.fetch_member((re.sub(r'\D','',separated[0])))
                    print(member)
                    await member.timeout_for(duration=datetime.timedelta(seconds = timeoutlength), reason=''.join(separated[1:]))
                except Exception as e:
                    print(e)
                    await ctx.send("Could not timeout.")
                tembed=discord.Embed( title=f"Member Warn ", description=f"<@{username.id}>\n Reason: {''.join(separated[1:])}", color=discord.Color.red())
                tembed.set_author(name=username.name, icon_url=username.display_avatar.url)
                await bot.get_channel(1419520700573679677).send(
                    embed=tembed)
            
    except Exception as e:
        print(e)
        await ctx.reply("Could not warn user.")# [/]# [/]

# @bot.slash_command(name = 'warnstatus')
@bot.command()
async def warnstatus(ctx ,*, id):
    allow = False
    # await ctx.defer()
    for role in ctx.author.roles:
        if role.id in adminIds:
            allow = True
            break
    if allow:
        separated = id.split('>')
        async with aiosqlite.connect("warndb.db") as db:
            async with db.execute("""
                        SELECT reasons FROM warns WHERE user_id = ?
                    """, (re.sub(r'\D','',separated[0]),)) as cursor:
                        row = await cursor.fetchone()
                    
                        reasons = json.loads(row[0]) if row else []
                
        userid = re.sub(r'\D','',separated[0])
        tembed = discord.Embed(
            title=f"Warns for: <@{userid}>"
        ) 
        # tembed.description = '\n'.join(reasons)
        tembed.description = '\n'.join([f'{index + 1}. {reason}' for index, reason in enumerate(reasons)])
        tembed.color = discord.Color.brand_red()
        await ctx.reply(embed=tembed)
    else:
        await ctx.reply("You do not have permission to do that.")
# [/]




bot.run(os.getenv('TOKEN')) # Run the bot with the env token