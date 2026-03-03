#!/usr/bin/env python3
# Source: https://github.com/IgorShadurin/app.yumcut.com
# Date: 2023-11-10
# Description: Core video generation script for YumCut - AI short video generator

import random
import json
from pathlib import Path
from moviepy.editor import concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip
from moviepy.config import change_settings
from gtts import gTTS
import requests
from PIL import Image, ImageDraw, ImageFont

# Configure moviepy to use ImageMagick if available
change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

class YumCutGenerator:
    """Main class for generating short vertical videos"""
    
    def __init__(self, topic: str, style: str = "casual", target_lang: str = "en"):
        """
        Initialize generator with video parameters
        
        Args:
            topic: Main subject/topic for the video content
            style: Visual style ('casual', 'professional', 'fun')
            target_lang: Language code for voice/subs (en, es, pt etc.)
        """
        self.topic = topic
        self.style = style
        self.lang = target_lang
        self.assets_dir = Path("assets")
        self.output_dir = Path("output")
        self._setup_dirs()
        
    def _setup_dirs(self):
        """Create required directories if they don't exist"""
        self.assets_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
    def generate_script(self) -> str:
        """Generate video script/text using topic"""
        # In production this would use LLM API
        script_examples = {
            "en": f"Did you know about {self.topic}? The surprising truth might shock you!",
            "es": f"Sabías que {self.topic}? La verdad sorprendente podría impactarte!",
            "pt": f"Você sabia sobre {self.topic}? A verdade surpreendente pode chocá-lo!"
        }
        return script_examples.get(self.lang, script_examples["en"])
    
    def generate_voiceover(self, text: str) -> Path:
        """Generate audio voiceover from text"""
        tts = gTTS(text=text, lang=self.lang, slow=False)
        voice_path = self.output_dir / "voiceover.mp3"
        tts.save(str(voice_path))
        return voice_path
    
    def get_stock_videos(self) -> list:
        """Get stock videos based on topic/style"""
        # In production would query stock API with topic/params
        return [self.assets_dir / "stock1.mp4", self.assets_dir / "stock2.mp4"]
    
    def create_subtitles(self, script: str, audio_duration: float) -> TextClip:
        """Create animated subtitles matching voiceover"""
        return TextClip(
            script,
            fontsize=40,
            color="white",
            font="Arial-Bold",
            stroke_color="black",
            stroke_width=1,
            size=(700, None),
            method="caption"
        ).set_duration(audio_duration).set_position(("center", "bottom"))
    
    def generate_video(self) -> Path:
        """Main method to generate complete video"""
        # Step 1: Generate script/content
        script = self.generate_script()
        print(f"Generated script: {script}")
        
        # Step 2: Generate voiceover
        voice_path = self.generate_voiceover(script)
        audio_clip = AudioFileClip(str(voice_path))
        
        # Step 3: Get stock videos
        video_clips = [self.get_stock_videos()[0]]  # Simplified
        
        # Step 4: Create subtitles
        subtitles = self.create_subtitles(script, audio_clip.duration)
        
        # Step 5: Compose final video
        final_clip = CompositeVideoClip([
            concatenate_videoclips(video_clips).set_duration(audio_cl