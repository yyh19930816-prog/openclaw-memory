# Source: krishsharma0413/pilcord (GitHub)
# Date: March 2023
# Description: Demonstrates PILCord's meme generation functionality for Discord bots

from io import BytesIO
from typing import Optional, Union
from pathlib import Path
from PIL import Image
import requests
import pilcord


async def generate_fight_flag_meme(image_url: str, text: str) -> BytesIO:
    """
    Generates 'fight_under_this_flag' meme
    
    Args:
        image_url: URL of the avatar/image to use
        text: Text to display on the flag
        
    Returns:
        BytesIO: In-memory image bytes
    """
    response = requests.get(image_url)
    avatar_bytes = BytesIO(response.content)
    
    meme_bytes = await pilcord.memes.fight_under_this_flag(avatar_bytes, text)
    return BytesIO(meme_bytes)


async def generate_uwu_discord_meme(image_url: str) -> BytesIO:
    """
    Generates 'uwu_discord' meme
    
    Args:
        image_url: URL of the avatar/image to use
        
    Returns:
        BytesIO: In-memory image bytes
    """
    response = requests.get(image_url)
    avatar_bytes = BytesIO(response.content)
    
    meme_bytes = await pilcord.memes.uwu_discord(avatar_bytes)
    return BytesIO(meme_bytes)


async def generate_rip_meme(
    image_url: str, 
    *, 
    year_born: Optional[str] = None, 
    year_death: Optional[str] = None
) -> BytesIO:
    """
    Generates 'rip' tombstone meme
    
    Args:
        image_url: URL of the avatar/image to use
        year_born: Birth year text (optional)
        year_death: Death year text (optional)
        
    Returns:
        BytesIO: In-memory image bytes
    """
    response = requests.get(image_url)
    avatar_bytes = BytesIO(response.content)
    
    meme_bytes = await pilcord.memes.rip(
        avatar_bytes, 
        born=year_born, 
        death=year_death
    )
    return BytesIO(meme_bytes)


async def save_meme_to_file(meme_bytes: BytesIO, filename: str) -> None:
    """
    Helper function to save meme to file
    
    Args:
        meme_bytes: Image bytes to save
        filename: Output filename
    """
    with open(filename, "wb") as f:
        f.write(meme_bytes.getbuffer())


# Example usage (async context required)
async def example_usage():
    avatar_url = "https://cdn.discordapp.com/avatars/123456789012345678/abcdefghijklmnopqrstuvwxyz.png"
    
    # Generate fight flag meme
    flag_meme = await generate_fight_flag_meme(avatar_url, "Our Server")
    await save_meme_to_file(flag_meme, "flag_meme.png")
    
    # Generate uwu discord meme
    uwu_meme = await generate_uwu_discord_meme(avatar_url)
    await save_meme_to_file(uwu_meme, "uwu_meme.png")
    
    # Generate rip meme
    rip_meme = await generate_rip_meme(avatar_url, year_born="2000", year_death="2022")
    await save_meme_to_file(rip_meme, "rip_meme.png")