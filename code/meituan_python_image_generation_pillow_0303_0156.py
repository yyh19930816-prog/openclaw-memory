# Source: krishsharma0413/pilcord (https://github.com/krishsharma0413/pilcord)
# Date: 2023-11-30
# Description: Example implementation of pilcord library features for Discord bot image generation

from io import BytesIO
import discord
from pilcord import RankCard, CardSettings
from PIL import Image

# Example Discord bot implementation
class MyBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_member_join(self, member):
        # Generate welcome card bytes using pilcord
        avatar_bytes = await member.avatar.read()
        
        # Create card settings
        settings = CardSettings(
            background="#36393f",  # Dark Discord background
            bar_color="#5865F2",  # Discord blurple
            text_color="white"
        )
        
        # Create rank card (used here as welcome card)
        card = RankCard(
            settings=settings,
            avatar=member.avatar.url,
            level=1,
            current_exp=0,
            max_exp=100,
            username=str(member),
            rank=None
        )
        
        card_bytes = card.card1()  # Generate image bytes
        
        # Send welcome message with generated image
        channel = member.guild.system_channel
        if channel:
            await channel.send(
                f"Welcome {member.mention}!",
                file=discord.File(BytesIO(card_bytes), filename="welcome.png")
            )

    async def on_message(self, message):
        if message.author == self.user:
            return
            
        # Example meme generation command
        if message.content.startswith('!meme'):
            args = message.content.split()[1:]
            
            if not args:
                await message.channel.send("Available memes: uwu_discord, rip, fight_under_this_flag")
                return
                
            meme_type = args[0]
            
            try:
                # In real usage, replace with actual pilcord meme generation
                # This is simplified for example
                img = Image.new('RGB', (400, 200), color='navy')
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                buffer.seek(0)
                
                await message.channel.send(
                    f"Here's your {meme_type} meme:",
                    file=discord.File(buffer, filename=f"{meme_type}.png")
                )
            except Exception as e:
                await message.channel.send(f"Error generating meme: {e}")

# Run the bot
if __name__ == '__main__':
    bot = MyBot(intents=discord.Intents.default())
    bot.run('YOUR_BOT_TOKEN')