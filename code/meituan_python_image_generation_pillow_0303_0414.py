"""
pilcord - A PIL-based image generation library for Discord bots
Source: https://github.com/krishsharma0413/pilcord
Date: 2023-03-15
Description: Generate ranking cards and memes for Discord bots
"""

from io import BytesIO
from typing import Optional, Union, BinaryIO
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

class CardSettings:
    """
    Settings for ranking card generation
    
    Args:
        background: Path to image or file-like object (4:1 aspect ratio recommended)
        bar_color: Color string for progress bar (default: "white")
        text_color: Color string for text (default: "white")
        background_color: Background color fallback (default: "#36393f")
    """
    def __init__(
        self,
        background: Union[Path, BinaryIO, str],
        bar_color: Optional[str] = 'white',
        text_color: Optional[str] = 'white',
        background_color: Optional[str] = "#36393f"
    ):
        self.background = background
        self.bar_color = bar_color
        self.text_color = text_color
        self.background_color = background_color

class RankCard:
    """
    Generate ranking cards for Discord bots
    
    NOTE: This class is deprecated - use DiscordLevelingCard instead
    """
    def __init__(
        self,
        settings: CardSettings,
        avatar: str,
        level: int,
        current_exp: int,
        max_exp: int,
        username: str,
        rank: Optional[int] = None
    ):
        self.settings = settings
        self.avatar = avatar
        self.level = level
        self.current_exp = current_exp
        self.max_exp = max_exp
        self.username = username
        self.rank = rank
    
    def card1(self) -> bytes:
        """Generate a simple ranking card style"""
        try:
            # Open background image
            if isinstance(self.settings.background, (str, Path)):
                bg = Image.open(self.settings.background)
            else:
                bg = Image.open(BytesIO(self.settings.background.read()))
            
            bg = bg.resize((1000, 250))
            
            # Create blank canvas
            card = Image.new("RGBA", bg.size)
            
            # Draw progress bar
            progress_width = 650
            progress_height = 30
            progress_x = 300
            progress_y = 180
            
            draw = ImageDraw.Draw(card)
            draw.rectangle(
                (progress_x, progress_y, progress_x + progress_width, progress_y + progress_height),
                fill="#333333"
            )
            
            # Calculate progress length
            progress_length = int((self.current_exp / self.max_exp) * progress_width)
            draw.rectangle(
                (progress_x, progress_y, progress_x + progress_length, progress_y + progress_height),
                fill=self.settings.bar_color
            )
            
            # Composite images and save
            final = Image.alpha_composite(bg.convert("RGBA"), card)
            buffer = BytesIO()
            final.save(buffer, format="PNG")
            buffer.seek(0)
            return buffer.read()
        
        except Exception as e:
            raise RuntimeError(f"Failed to generate rank card: {e}") from e

class MemeGenerator:
    """Generate memes for Discord"""
    
    @staticmethod
    def uwu_discord(text: str) -> bytes:
        """Generate UWU Discord meme"""
        try:
            base = Image.new("RGB", (500, 200), color="#36393f")
            draw = ImageDraw.Draw(base)
            font = ImageFont.load_default(size=40)
            
            draw.text(
                (50, 80),
                f"UWU {text} DISCORD",
                fill="white",
                font=font
            )
            
            buffer = BytesIO()
            base.save(buffer, format="PNG")
            buffer.seek(0)
            return buffer.read()
        
        except Exception as e:
            raise RuntimeError(f"Failed to generate UWU meme: {e}") from e

# Example Usage:
if __name__