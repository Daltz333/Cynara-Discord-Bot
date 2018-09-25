import discord
from discord.ext import commands
import random
import constants
from tinydb import TinyDB, Query
import time
import asyncio
import praw

bot = commands.Bot(command_prefix=constants.PREFIX, description=constants.DESCRIPTION)
db = TinyDB('db.json')
roles = TinyDB('roles.json')
user = Query()
leveledup = False
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='discord')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as:', bot.user.name)
    await bot.change_presence(game=discord.Game(name='type .help for commands!'))

@bot.event
async def on_message(message):  
    rolez = discord.utils.get(message.author.server.roles, name="Bots")

    if rolez in message.author.roles:
        pass

    else:
        user_add_xp(message.author.id, 1) 
        global leveledup
        if (leveledup):
            congrats2 = "Congratulations " + message.author.name + "! You have leveled up!"
            await bot.send_message(message.channel, congrats2)
            leveledup = False

    sorteddb = get_roles()
    usermessage = message.author

    rmrole = []

    for x in range(0, len(sorteddb)):
    
        if (int(sorteddb[x]['Level']) <= int(get_level(message.author.id))):
            role = discord.utils.get(usermessage.server.roles, name=sorteddb[x]['Role'])

            if role in message.author.roles:
                break

            else: 
                
                for y in range(0, len(sorteddb)):
                    rmrole.append(discord.utils.get(usermessage.server.roles, name=sorteddb[y]['Role']))
                    print(rmrole[y].name)
                
                print(rmrole)
                await bot.remove_roles(message.author, *rmrole)
                await asyncio.sleep(.05)
                congrats = "Congratulations! " + message.author.name + " has been promoted to " + role.name + "!"
                await bot.add_roles(message.author, role)

                await bot.send_message(message.channel, congrats)
                break

    await bot.process_commands(message)
    return

@bot.command(pass_context = True)
async def play(ctx, url):
    """Plays a song"""
    author = ctx.message.author
    voice_channel = author.voice_channel
    await bot.say("Starting Song!")
    vc = await bot.join_voice_channel(voice_channel)

    player = await vc.create_ytdl_player(url)
    player.start()

@bot.command(pass_context = True)
async def help():
    embed=discord.Embed(title="Cynara Administrative Commands", description="A list of commands available to users with administrative priveleges.")
    embed.add_field(name=".help", value="Shows this help message.", inline=False)
    embed.add_field(name=".ping", value="Returns the estimated latency between yourself and the server.", inline=False)
    embed.add_field(name=".setlvl @username {level}", value="Sets the specified users level.", inline=False)
    embed.add_field(name=".setrole {rolename} {level}", value="Set the role to be gained automatically once users reach the specified level. Note it does remove lower level roles on level up.", inline=True)
    embed.add_field(name=".delrole {rolename}", value="Deletes the specified autorole.", inline=True)
    await bot.say(embed=embed)

    embed2=discord.Embed(title="Cynara General Commands", description="A list of commands available to all users.")
    embed2.add_field(name=".lvl @username", value ="Grabs the specified users level.", inline=False)
    embed2.add_field(name=".meme", value="Grabs a random meme from /r/memes.", inline=False)
    embed2.add_field(name=".animeme", value="Grabs a random meme from /r/Animemes/", inline=False)
    embed2.add_field(name=".leaderboard", value="Shows the top 10 leveled players on the server.", inline=False)
    embed2.add_field(name=".say Enter text here", value="Makes Cynara say something.", inline=False)
    embed2.add_field(name=".play {URL}", value="Plays from MP3 streams or youtube urls.", inline=False)
    embed2.add_field(name=".stop", value="Stops Cynara from playing music.", inline=False)
    await bot.say(embed=embed2)

    embed3 = discord.Embed(title="Cynara Player Commands", description="Description not found.")
    embed3.add_field(name=".grimm", value = "Heh.", inline = False)
    embed3.add_field(name=".princess", value = "Heh.", inline = False)
    embed3.add_field(name=".cory", value = "Heh.", inline = False)
    embed3.set_footer(text="Made with love by Dalton Smith.")
    await bot.say(embed=embed3)

@bot.command(pass_context = True)
async def stop(ctx):
    """Stop playing a song"""
    for x in bot.voice_clients:
        if(x.server == ctx.message.server):
            return await x.disconnect()

    await bot.say("I am not connected to any voice channel on this server!")

@bot.command(pass_context=True)
async def cory():
    await bot.say("I love you! https://i.imgur.com/YX6ZTJ2.gif")

@bot.command(pass_context=True)
async def grimm():
    await bot.say("Daisuki! https://www.youtube.com/watch?v=k7tvxB3XSu8")

@bot.command(pass_context=True)
async def princess():
    await bot.say("https://i.imgur.com/ktGdV.gif")

@bot.command(pass_context = True)
async def say(ctx, *, word: str):
    """Makes the bot say something! EX: 'say Billy is Bob'"""
    await bot.delete_message(ctx.message)
    await bot.say(word)
    print ("Bot has said something")

@bot.command(pass_context = True)
async def meme():
    """Grabs a random meme from /r/memes"""
    memes_submissions = reddit.subreddit('memes').hot()
    post_to_pick = random.randint(1, 10)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    await bot.say(submission.url)

@bot.command(pass_context = True)
async def animeme():
    """Grabs a random meme from /r/memes"""
    memes_submissions = reddit.subreddit('Animemes').hot()
    post_to_pick = random.randint(1, 10)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    await bot.say(submission.url)

@commands.has_permissions(manage_roles=True) 
@bot.command(pass_context = True)
async def setrole(ctx, role, level: int):
    '''Set role to be gained at specified level. EX: setrole ROLENAME 50'''
    roleset = discord.utils.get(ctx.message.server.roles, name=role)

    if roleset is None:
        await bot.say("Invalid Role Name")
        return

    else:
        set_roles(roleset.name, level)

    await bot.say("Roles have been set")

@commands.has_permissions(manage_roles=True) 
@bot.command()
async def delrole(role):
    '''Deletes role to be gained at specified level. EX: delrole ROLENAME'''
    delete_roles(role)

@bot.command(pass_context=True)
async def ping(ctx):
    '''Grab the ping of the bot. Not very accurate'''
    channel = ctx.message.channel
    t1 = time.perf_counter()
    await bot.send_typing(channel)
    t2 = time.perf_counter()
    await bot.say("Ping: {}ms".format(round((t2-t1)*1000)))

@bot.command(pass_context=True)
async def leaderboard(ctx):
    '''Show the top 10 users on the server'''
    topten = get_top()
    embed=discord.Embed(title="====LEADERBOARD====", color=0x80ff80)

    for x in range(0, len(topten)):
        valuedynamic = "Level: ", topten[x]['Level'], " -  XP: ", topten[x]['XP']
        valuedynamic2 = str(valuedynamic)
        valuedynamic2 = valuedynamic2.replace("'","")
        valuedynamic2 = valuedynamic2.replace(",","")
        valuedynamic2 = valuedynamic2.replace("(","")
        valuedynamic2 = valuedynamic2.replace(")","")
        embed.add_field(name=ctx.message.server.get_member(topten[x]['UserID']).name, value=valuedynamic2, inline=False)

    await bot.say(embed=embed)

@commands.has_permissions(manage_roles=True) 
@bot.command(pass_context=True)
async def setlvl(ctx, member: discord.Member, level: int):
    '''Administrator Only! Sets user level and xp. '''
    if(member):
        user_set_level(member.id, level)
    else:
        user_set_level(ctx.message.author.id, level)

    await bot.say("Level has been set.")

@bot.command(pass_context=True)
async def lvl(ctx, member: discord.Member = None):
    '''Grabs the users Level and XP!'''
    embed=discord.Embed(color=0x80ff80)

    if(member):
        if(get_xp(member.id) == '-1'):
            await bot.say("This member hasn't talked on the server yet.")
        else:
            xp = "\nLevel: " + get_level(member.id) + "\nEXP: " + get_xp(member.id) + "/" +  get_limit(member.id)
            mainname = member.name 
    else:
        xp = "\nLevel: " + get_level(ctx.message.author.id) + "\nEXP: " + get_xp(ctx.message.author.id) + "/" +  get_limit(ctx.message.author.id) 
        mainname = ctx.message.author.name

    embed.add_field(name=mainname, value=xp, inline=False)

    await bot.say(embed=embed)
    print ("Grabbed users XP")

def user_add_xp(user_id: int, xp: int):
    if (db.search(user.UserID == user_id)):
        user_xp = db.search(user.UserID == user_id)
        new_xp = user_xp[0]["XP"] + xp
        if new_xp >= user_xp[0]['Limit']:
            new_level = user_xp[0]['Level'] + 1
            new_limit = ((user_xp[0]['Limit'] * .05) + 100) + user_xp[0]['Limit']
            db.update({'XP': new_xp, 'Level': new_level, 'Limit': int(new_limit)}, user.UserID == user_id)
            global leveledup
            leveledup = True

        else:   
            db.update({'XP': new_xp}, user.UserID == user_id)
    else:
        db.insert({'UserID': user_id, 'XP': xp, 'Level': 1, 'Limit': 100})

def set_roles(role, level:int):
    roles.insert({'Role': role, 'Level': level})

def get_roles():
    return sorted(roles.all(), key=lambda k: k['Level'], reverse=True)

def delete_roles(role):
    roles.remove(user.Role == role)

def user_set_level(user_id: int, level: int):
    db.update({'XP': 0, 'Level': 1, 'Limit': 100}, user.UserID == user_id)
    prev_amount = db.search(user.UserID == user_id)
    new_xp = prev_amount[0]['Level']
    new_limit = prev_amount[0]['Limit']
    for x in range(0, level-1):
        new_xp = ((new_xp * 0.05) + 100) + new_xp
        new_limit = ((new_limit * 0.05) + 100) + new_limit
    
    new_level = level

    db.update({'XP': int(new_xp), 'Level': new_level, 'Limit': int(new_limit)}, user.UserID == user_id)

def get_xp(user_id: int):
    try:
        xp = db.search(user.UserID == user_id)
        return str(xp[0]["XP"])
    except IndexError:
        return '-1'

def get_limit(user_id: int):
     userdb = db.search(user.UserID == user_id)
     return str(userdb[0]['Limit'])

def get_level(user_id: int):
    userdb = db.search(user.UserID == user_id)
    return str(userdb[0]['Level'])

def get_top():
    userdb = db.all()
    sorteddb = sorted(userdb, key=lambda k: k['XP'], reverse=True)[0:10]

    return sorteddb

bot.run(constants.BOT_TOKEN)
