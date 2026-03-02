# Source: krishsharma0413/pilcord
# Date: 2023-08-20
# Description: Example usage of pilcord library for Discord image generation

from pilcord import RankCard, CardSettings
from io import BytesIO
import requests
import discord

async def generate_level_card():
    # Example Discord user data
    avatar_url = "https://cdn.discordapp.com/avatars/123456789012345678/a_abcdefghijklmnopqrstuvwxyz123456.png"
    username = "ExampleUser"
    level = 15
    current_exp = 750
    max_exp = 1000
    rank = 42
    
    # Get avatar image as bytes
    response = requests.get(avatar_url)
    avatar_bytes = BytesIO(response.content)
    
    # Create card settings
    settings = CardSettings(
        background="https://example.com/background.png",  # Replace with actual background URL
        bar_color="#5865F2",  # Discord blurple
        text_color="white",
        background_color="#36393f"  # Discord dark theme
    )
    
    # Create rank card instance
    card = RankCard(
        settings=settings,
        avatar=avatar_bytes,
        level=level,
        current_exp=current_exp,
        max_exp=max_exp,
        username=username,
        rank=rank
    )
    
    # Generate card1 style
    card_bytes = card.card1()
    
    # Create Discord file object
    return discord.File(BytesIO(card_bytes), filename="level_card.png")

async def generate_meme(meme_type: str, text: str):
    """Generate a meme image using pilcord"""
    from pilcord import MemeGenerator
    
    generator = MemeGenerator()
    
    if meme_type == "uwu_discord":
        meme_bytes = generator.uwu_discord(text)
    elif meme_type == "rip":
        meme_bytes = generator.rip(text)
    elif meme_type == "flag":
        meme_bytes = generator.fight_under_this_flag(text)
    else:
        raise ValueError("Invalid meme type")
    
    return discord.File(BytesIO(meme_bytes), filename=f"{meme_type}_meme.png")

# Example Discord bot command usage
async def level_command(interaction: discord.Interaction):
    """Discord slash command handler for level card"""
    card_file = await generate_level_card()
    await interaction.response.send_message(file=card_file)

async def meme_command(interaction: discord.Interaction, meme_type: str, text: str):
    """Discord slash command handler for meme generation"""
    try:
        meme_file = await generate_meme(meme_type, text)
        await interaction.response.send_message(file=meme_file)
    except ValueError as e:
        await interaction.response.send_message(str(e), ephemeral=True)