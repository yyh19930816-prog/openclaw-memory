#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Source: https://github.com/harry0703/MoneyPrinterTurbo
# Date: 2024-03-20
# Description: Core functionality for automated video generation from text prompts

import os
import json
import random
import requests
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip
from moviepy.video.fx.all import resize

class MoneyPrinterTurbo:
    def __init__(self, config_path="config.json"):
        """
        Initialize video generator with configuration
        """
        with open(config_path) as f:
            self.config = json.load(f)
        self.video_clips = []
        self.audio_clips = []
        
    def generate_script(self, topic):
        """
        Generate video script using AI provider
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config['api_key']}"
        }
        payload = {
            "model": self.config["model"],
            "messages": [{"role": "user", "content": f"Write a script about {topic}"}],
            "temperature": 0.7
        }
        
        response = requests.post(self.config["api_url"], headers=headers, json=payload)
        return response.json()["choices"][0]["message"]["content"]
    
    def get_video_clips(self, script):
        """
        Get video clips based on script keywords
        """
        keywords = self.extract_keywords(script)
        for keyword in keywords:
            clip = self.search_video_clip(keyword)
            if clip:
                self.video_clips.append(clip)
                
    def search_video_clip(self, keyword):
        """
        Search for video clip matching keyword
        """
        try:
            response = requests.get(
                self.config["pexels_api_url"],
                headers={"Authorization": self.config["pexels_api_key"]},
                params={"query": keyword, "per_page": 1}
            )
            video_url = response.json()["videos"][0]["video_files"][0]["link"]
            return VideoFileClip(video_url)
        except:
            return None
            
    def generate_audio(self, script):
        """
        Generate narration audio from script
        """
        # Placeholder - actual implementation would use TTS API
        print(f"Generating audio narration for script")
        return AudioFileClip("placeholder_audio.mp3")
        
    def generate_subtitles(self, script):
        """
        Generate subtitles overlays for video
        """
        words = script.split()
        duration_per_word = len(self.audio_clips[0]) / len(words)
        subtitle_clips = []
        
        for i, word in enumerate(words):
            txt_clip = TextClip(word, fontsize=70, color='white', 
                              font=self.config["font"], stroke_color='black',
                              stroke_width=2)
            txt_clip = txt_clip.set_position('center').set_duration(duration_per_word)
            txt_clip = txt_clip.set_start(i * duration_per_word)
            subtitle_clips.append(txt_clip)
            
        return subtitle_clips
        
    def compose_video(self, output_path="output.mp4"):
        """
        Compose final video with all elements
        """
        # Resize all video clips to match config
        resized_clips = [resize(clip, (self.config["width"], self.config["height"])) 
                        for clip in self.video_clips]
        
        # Combine video clips
        final_video = concatenate_videoclips(resized_clips)
        
        # Add audio
        final_audio = CompositeAudioClip(self.audio_clips)
        final_video = final_video.set_audio(final_audio)
        
        # Add background music if enabled
        if self.config["background_music"]:
            bg_music = AudioFileClip(self.config["background_music"])
            bg_music = bg_music.volumex(self.config["music_volume"])
            final_audio = CompositeAudioClip([final_audio, bg_music])
            final_video = final