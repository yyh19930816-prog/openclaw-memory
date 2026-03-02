# Source: github.com/krishsharma0413/pilcord
# Date: 2023-10-25
# Description: Example implementation of pilcord library for Discord image generation

from io import BytesIO
from typing import Optional, Union
from pathlib import Path
from PIL import Image
import requests
from pilcord import RankCard, CardSettings

def generate_rank_card(avatar_url: str, username: str, level: int, current_exp: int, 
                      max_exp: int, rank: Optional[int] = None) -> BytesIO:
    """
    Generate a Discord rank card with user stats.
    
    Args:
        avatar_url: URL of user's avatar image
        username: Discord username
        level: User's current level
        current_exp: Current experience points
        max_exp: Max experience for current level
        rank: Optional rank position
        
    Returns:
        BytesIO: Image data ready for Discord File
    """
    # Download background image
    bg_url = "https://i.imgur.com/WgN6uFI.jpg"
    bg_response = requests.get(bg_url)
    bg_image = BytesIO(bg_response.content)
    
    # Configure card settings
    settings = CardSettings(
        background=bg_image,
        bar_color="#5865F2",  # Discord blurple
        text_color="white",
        background_color="#36393f"
    )
    
    # Create and generate rank card
    card = RankCard(
        settings=settings,
        avatar=avatar_url,
        level=level,
        current_exp=current_exp,
        max_exp=max_exp,
        username=username,
        rank=rank
    )
    
    # Get card bytes and return as BytesIO
    card_bytes = card.card1()
    return BytesIO(card_bytes)

def generate_meme(meme_type: str, avatar_url: str, text: str) -> BytesIO:
    """
    Generate a meme image using predefined templates.
    
    Args:
        meme_type: Type of meme (uwu_discord, fight_under_this_flag, rip)
        avatar_url: URL of user's avatar
        text: Text to include in meme
        
    Returns:
        BytesIO: Image data ready for Discord File
    """
    # Note: Actual meme generation would use pilcord's meme functions
    # This is a placeholder implementation
    img = Image.new('RGB', (500, 500), color='gray')
    
    # Download and add avatar
    avatar_response = requests.get(avatar_url)
    avatar_img = Image.open(BytesIO(avatar_response.content))
    avatar_img = avatar_img.resize((200, 200))
    img.paste(avatar_img, (150, 150))
    
    # Add text
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((250, 50), f"{meme_type.upper()} MEME", font=font, fill="white")
    draw.text((20, 400), text, font=font, fill="white")
    
    # Convert to bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes