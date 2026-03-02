# discord.py bot example
# Source: https://github.com/Rapptz/discord.py
# Created: 2023-11-20
# Description: A basic Discord bot with ping/pong functionality and simple commands

import discord
from discord.ext import commands

# Define intents - these determine what events your bot can receive
# More info: https://discordpy.readthedocs.io/en/stable/intents.html
intents = discord.Intents.default()
intents.message_content = True  # Required for bot to see message content

# Initialize bot with command prefix and intents
# Prefix can be changed to whatever you prefer ('!', '.', '$', etc.)
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_ready():
    """Called when the bot has successfully connected to Discord"""
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def ping(ctx):
    """Simple command that responds with 'pong'"""
    await ctx.send('pong')

@bot.command()
async def hello(ctx):
    """Greet the user"""
    await ctx.send(f'Hello {ctx.author.mention}!')

@bot.command()
async def info(ctx):
    """Display basic bot information"""
    embed = discord.Embed(
        title="Bot Information",
        description="A simple Discord bot example",
        color=discord.Color.blue()
    )
    embed.add_field(name="Prefix", value=f"`{bot.command_prefix}`", inline=True)
    embed.add_field(name="Commands", value="ping, hello, info", inline=True)
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    """Handle all messages"""
    # Don't respond to ourselves or other bots
    if message.author == bot.user or message.author.bot:
        return
    
    # Let commands process normally
    await bot.process_commands(message)

# Note: In production, store your token securely (environment variables, config files)
# Never commit tokens to source control!
bot.run('your_bot_token_here')