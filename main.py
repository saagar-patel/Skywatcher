
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = '!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='hello')
async def hello(ctx):
    if ctx.author == bot.user:
        return
    await ctx.send('Hello once!')


"""
Will output the daily summary objects and phenomena to the channel

--- Params

None
"""
@bot.command(name="Daily Summary")
async def daily_summary(ctx):
    pass

"""
Will output the coordinates and relative direction of the 
"""
@bot.command(name="Locate")
async def locate(ctx, arg):
    pass

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await bot.close()
    print("BOT HAS SHUTDOWN")

bot.run('TOKEN')
