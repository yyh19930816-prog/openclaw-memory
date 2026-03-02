#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Source: https://github.com/wanghaisheng/tiktoka-studio-uploader
Date: 2023-12-06
Description: TikTok/YouTube video upload automation tool
"""

import os
import time
import random
from argparse import ArgumentParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class VideoUploader:
    """Core class for automating video uploads to TikTok/Youtube"""
    
    def __init__(self, platform, headless=True):
        """
        Initialize uploader with specified platform
        
        Args:
            platform (str): 'tiktok' or 'youtube'
            headless (bool): Run browser in headless mode
        """
        self.platform = platform.lower()
        self.headless = headless
        self._setup_driver()
        
    def _setup_driver(self):
        """Configure selenium webdriver with options"""
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        
    def login(self, username, password):
        """
        Log in to platform account
        
        Args:
            username (str): Account username/email
            password (str): Account password
        """
        login_url = {
            'tiktok': 'https://www.tiktok.com/login',
            'youtube': 'https://accounts.google.com/'
        }.get(self.platform)
        
        if not login_url:
            raise ValueError(f"Unsupported platform: {self.platform}")
            
        self.driver.get(login_url)
        time.sleep(random.uniform(2, 5))  # Random delay
        
        # Example login flow - would need platform-specific selectors
        try:
            username_field = self.driver.find_element(By.NAME, 'username')
            username_field.send_keys(username)
            password_field = self.driver.find_element(By.NAME, 'password')
            password_field.send_keys(password)
            login_button = self.driver.find_element(By.XPATH, '//button[contains(text(),"Log in")]')
            login_button.click()
            WebDriverWait(self.driver, 10).until(
                EC.url_changes(login_url)
            )
        except Exception as e:
            print(f"Login failed: {str(e)}")
            raise
            
    def upload_video(self, video_path, title, description='', tags=None):
        """
        Upload video to platform
        
        Args:
            video_path (str): Path to video file
            title (str): Video title
            description (str): Video description
            tags (list): List of tags/metadata
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
            
        upload_url = {
            'tiktok': 'https://www.tiktok.com/upload',
            'youtube': 'https://studio.youtube.com'
        }.get(self.platform)
        
        self.driver.get(upload_url)
        time.sleep(random.uniform(3, 7))  # Random delay
        
        try:
            # Upload process would vary by platform
            file_input = self.driver.find_element(By.XPATH, '//input[@type="file"]')
            file_input.send_keys(video_path)
            
            # Wait for upload to complete
            WebDriverWait(self.driver, 300).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"Upload complete")]'))
            )
            
            # Set metadata
            title_field = self.driver.find_element(By.ID, 'video-title')
            title_field.clear()
            title_field.send_keys(title)
            
            if description:
                desc_field = self.driver.find_element(By.ID, 'video-description')
                desc_field.send_keys(description)
                
            #