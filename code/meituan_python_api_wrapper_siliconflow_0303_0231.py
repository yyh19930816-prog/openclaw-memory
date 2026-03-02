#!/usr/bin/env python3
"""
discord.py bot example
Source: https://github.com/Rapptz/discord.py
Date: 2023-04-01
Description: Basic Discord bot demonstrating client and commands functionality
"""

import discord
from discord.ext import commands

# Initialize bot with command prefix and intents
intents = discord.Intents.default()
intents.message_content = True  # Required for message content access
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_ready():
    """Called when the bot is fully logged in"""
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def ping(ctx):
    """Responds with 'pong'"""
    await ctx.send('pong')

@bot.command()
async def greet(ctx, *, name: str = "there"):
    """Greets a user
    
    Parameters
    ----------
    name : str
        The name of the person to greet (default: "there")
    """
    await ctx.send(f'Hello {name}!')

@bot.command()
async def info(ctx):
    """Displays bot information"""
    embed = discord.Embed(title="Bot Info", color=discord.Color.blue())
    embed.add_field(name="Developer", value="Meituan", inline=False)
    embed.add_field(name="Library", value="discord.py", inline=False)
    embed.add_field(name="Prefix", value=bot.command_prefix, inline=False)
    await ctx.send(embed=embed)

class MyClient(discord.Client):
    """Example client demonstrating basic event handling"""
    async def on_ready(self):
        print(f'Client logged on as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return
            
        if message.content.startswith('hello'):
            await message.channel.send('Hi!')

# Replace 'your_token_here' with your actual bot token
if __name__ == "__main__":
    print("Starting bot...")
    bot.run('your_token_here')
    
    # Uncomment below to run the client example instead
    # intents = discord.Intents.default()
    # intents.message_content = True
    # client = MyClient(intents=intents)
    # client.run('your_token_here')