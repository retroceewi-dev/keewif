from curses.ascii import isalpha, isalnum

import discord
from discord.ext import commands
import os # default module
import asyncio
import re
import random
import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv


asyncio.set_event_loop(asyncio.new_event_loop())
load_dotenv() # load all the variables from the env file

bot = discord.Bot()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.moderation = True
intents.reactions = True
# intents.roles = True


bot = commands.Bot(command_prefix='!', intents=intents)

vowels = [
        'a',
        'i',
        'o',
        'u',
        'e'
    ]
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
    return ' '.join(retsentence)
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!   {datetime.datetime.now()}")

# @bot.slash_command(name="keewify", description="Keewify!")
# async def keewify(ctx,
#                   tokeewi: discord.Option(discord.SlashCommandOptionType.string)):
#     ret = sentenceToKeewi(tokeewi)
#     print(ret)
#     time.sleep(0.1)
#     await ctx.respond(f'{ret}')
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
# Get welcome channel for use.

@bot.command()
async def keewify(ctx, *, message_content):
    ret = sentenceToKeewi(message_content)
    print(ret)
    await ctx.send(f'{ret}')
@bot.command()
async def dihify(ctx, *, message_content):
    ret = sentenceToDih(message_content)
    print(ret)
    await ctx.send(f'{ret}')
@bot.command()
async def murder(ctx, *, message_content):
    print("Murdered.")
    await ctx.send(f'{message_content}: {random.choice(murdermsgs)}!')

exclude = [
        641468688620584970,
        1405772116867158039,
        1493442279267106837,
        759712287396200479,
        900013076089294908
    ]

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
            await ctx.send("No 16-17s found! Teh...")
                        
ageroles = [
    1290492844838096956,
    1283473260003983430,
    1283473032719110204
]
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
        await ctx.send("None of the Roleless were found! Teh...")
                   
@bot.command()
async def kickroleless(ctx):
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
                    await user.kick(reason="NO age role selected.")
                if len(message) + 30 >= 500:
                    await ctx.send(message)
                    message = ""
    if not message == "":
        await ctx.send(message)
        await ctx.send(str(total) + " members were found / kicked.")
    else:
        await ctx.send("None of the Roleless were found nor kicked! Teh...")

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

@bot.event
async def on_member_ban(guild, user):

    welcome = bot.get_channel(1283237643458711645)
    print(f"Member banned: {user.display_name}")
    await welcome.send(f"<@{user.id}> was banned! Cya!")

@bot.event
async def on_command_error(ctx, error):
    print(f"Command sent with \n'{ctx.message.content}'\n errored in {ctx.guild} channel #{ctx.channel}.")
    print(f"error: {error}")
@bot.event
async def on_reaction_add(reaction, user):
    # print("Reaction added.")
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
        pass
bot.run(os.getenv('TOKEN')) # run the bot with the token

