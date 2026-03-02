"""
pilcord - Image generation library for Discord bots
Source: https://github.com/krishsharma0413/pilcord
Date: 2023-03-15
Description: Generates Discord cards and memes using PIL
"""

from io import BytesIO
from typing import Optional, Union, BinaryIO
from PIL import Image, ImageDraw, ImageFont
import requests
import textwrap

class MemeGenerator:
    """Handles meme generation functionality"""
    
    @staticmethod
    def fight_under_this_flag(avatar_url: str, username: str) -> BytesIO:
        """
        Generates 'fight under this flag' meme
        
        Args:
            avatar_url: URL of user's avatar
            username: Discord username
            
        Returns:
            BytesIO: Image data ready for Discord
        """
        # Fetch base image
        base_img = Image.open(requests.get(avatar_url, stream=True).raw)
        base_img = base_img.resize((300, 300))
        
        # Create blank canvas
        canvas = Image.new('RGB', (600, 400), color='black')
        draw = ImageDraw.Draw(canvas)
        
        # Add avatar and text
        canvas.paste(base_img, (150, 50))
        font = ImageFont.load_default(size=20)
        draw.text((150, 360), f"{username} WILL FIGHT UNDER THIS FLAG", 
                 font=font, fill='white')
        
        # Save to bytes buffer
        buffer = BytesIO()
        canvas.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer
        
    @staticmethod
    def uwu_discord(text: str) -> BytesIO:
        """
        Generates UWU Discord meme
        
        Args:
            text: Text to display
            
        Returns:
            BytesIO: Image data ready for Discord
        """
        # Create blank canvas
        canvas = Image.new('RGB', (500, 200), color='#2C2F33')
        draw = ImageDraw.Draw(canvas)
        
        # Add text
        font = ImageFont.load_default(size=16)
        draw.multiline_text((10, 10), text, font=font, fill='white')
        
        # Save to bytes buffer
        buffer = BytesIO()
        canvas.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer
        
    @staticmethod
    def rip(avatar_url: str, username: str, born: str, died: str) -> BytesIO:
        """
        Generates RIP tombstone meme
        
        Args:
            avatar_url: URL of user's avatar
            username: Discord username
            born: Birth date/description
            died: Death description
            
        Returns:
            BytesIO: Image data ready for Discord
        """
        # Fetch base image
        avatar = Image.open(requests.get(avatar_url, stream=True).raw)
        avatar = avatar.resize((100, 100))
        
        # Create tombstone
        canvas = Image.new('RGB', (300, 400), color='black')
        draw = ImageDraw.Draw(canvas)
        
        # Draw tombstone
        draw.rectangle([50, 50, 250, 350], fill='gray')
        canvas.paste(avatar, (100, 100))
        
        # Add text
        font = ImageFont.load_default(size=12)
        draw.text((100, 210), f"REST IN PEACE\n{username}", 
                 font=font, fill='black', align='center')
        draw.text((80, 250), f"BORN: {born}", font=font, fill='black')
        draw.text((80, 270), f"DIED: {died}", font=font, fill='black')
        
        # Save to bytes buffer
        buffer = BytesIO()
        canvas.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer

# Example usage:
# meme = MemeGenerator()
# rip_image = meme.rip(avatar_url, "John", "2000", "2023")
# await ctx.send(file=discord.File(rip_image, 'rip.png'))