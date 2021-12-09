import discord
from discord.ext import commands
import requests, random
import json

TOKEN = 'Токен бота'
BOT_PREFIX = '/' #!join

bot = commands.Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_ready():
    print(bot.user.name + ' connected to the channel')


@bot.event
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined in {member.joined_at}')


bot.remove_command('help')
@bot.command(pass_context = True)
async def help(ctx):
    author = ctx.message.author

    await ctx.send(f'Hello, {author.mention}! I am BOT!') # Выводим сообщение с упоминанием автора


@bot.command( pass_context = True )
async def kick( ctx, member: discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )

    await member.kick( reason = reason )
    await ctx.send( f'kick user { member.mention }' )


@bot.command( pass_context = True )
async def ban( ctx, member: discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )

    await member.ban( reason = reason )
    await ctx.send( f'ban user { member.mention }' )


@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        await ctx.send(f"{user} have been unbanned sucessfully")
        return


@bot.command()
async def gif(ctx, message):
    response = requests.get(f'https://api.giphy.com/v1/gifs/search?api_key=mZtqJ1vj48h5Wr7vrh0pTqCJ1eVyvC76&q={message}&limit=10&offset=1&rating=g&lang=en') # Get-запрос
    json_data = response.json() # Извлекаем JSON
    res = []
    for i in range(10):
        res.append(json_data['data'][i]['images']['original']['url'])
    embed = discord.Embed(color = 0xff9900, title = 'Gif')
    embed.set_image(url = random.choice(res))
    await ctx.send(embed = embed)


try:
    with open("users.json") as fp:
        users = json.load(fp)
except Exception:
    users = {}

def save_users():
    with open("users.json", "w+") as fp:
        json.dump(users, fp, sort_keys=True, indent=4)

def add_points(user: discord.User, points: int):
    id = user.id
    if id not in users:
        users[id] = {}
    users[id]["points"] = users[id].get("points", 0) + points
    print("{} now has {} points".format(user.name, users[id]["points"]))
    save_users()

def get_points(user: discord.User):
    id = user.id
    if id in users:
        return users[id].get("points", 0)
    return 0

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print("{} sent a message".format(message.author.name))
    if message.content.lower().startswith("!lvl"):
        msg = "You have {} points!".format(get_points(message.author))
        await message.channel.send(msg)
    add_points(message.author, 1)

bot.run(TOKEN)
