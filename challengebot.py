#challengebot.py
import discord
import os
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
import io

load_dotenv()
TOKEN = os.getenv('TOKEN')

#intents
intents = discord.Intents.all()
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='.', intents=intents)

#bot connect
@bot.event
async def on_ready():
    print("Bot is connected to Discord")
    await bot.load_extension('cogs.rps')

#sends message for errors
@bot.event
async def on_command_error(ctx, error):
        if str(error) == 'member is a required argument that is missing.':
            await ctx.channel.send(f'Use ".challenge @member" to challenge a user to a game of "Rock Paper Scissors".')
        else:
            await ctx.channel.send(f'poopy')

bot.run(TOKEN)