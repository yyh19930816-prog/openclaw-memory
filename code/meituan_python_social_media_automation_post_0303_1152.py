#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Source: ColombiaPython/social-media-automation (https://github.com/ColombiaPython/social-media-automation)
Date: 2023-04-01
Description: Selenium script to post image with text to Facebook Groups
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time
import os

class FacebookPoster:
    def __init__(self, username, password, image_path, group_urls):
        """
        Initialize Facebook Poster with credentials and post details
        
        Args:
            username (str): Facebook login email
            password (str): Facebook login password
            image_path (str): Path to image file to upload
            group_urls (list): List of Facebook group URLs to post to
        """
        self.username = username
        self.password = password
        self.image_path = image_path
        self.group_urls = group_urls
        service = Service('/path/to/geckodriver')  # Update this path
        options = Options()
        options.headless = False  # Set to True for background operation
        self.driver = webdriver.Firefox(service=service, options=options)
        
    def login(self):
        """Log in to Facebook account"""
        self.driver.get("https://www.facebook.com/")
        email_field = self.driver.find_element(By.ID, "email")
        email_field.send_keys(self.username)
        password_field = self.driver.find_element(By.ID, "pass")
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)  # Wait for login to complete
        
    def post_to_groups(self, text):
        """
        Post image with text to each specified Facebook group
        
        Args:
            text (str): Text content to post with image
        """
        for group_url in self.group_urls:
            self.driver.get(group_url)
            time.sleep(3)
            
            # Click photo/video upload button
            try:
                photo_btn = self.driver.find_element(
                    By.XPATH, "//div[@aria-label='Photo/Video']"
                )
                photo_btn.click()
            except:
                print(f"Couldn't find upload button in {group_url}")
                continue
                
            time.sleep(2)
            
            # Upload image file
            file_input = self.driver.find_element(
                By.XPATH, "//input[@type='file']"
            )
            file_input.send_keys(os.path.abspath(self.image_path))
            time.sleep(3)  # Wait for upload
            
            # Add post text
            post_box = self.driver.find_element(
                By.XPATH, "//div[@data-contents='true']"
            )
            post_box.send_keys(text)
            time.sleep(1)
            
            # Click post button
            post_btn = self.driver.find_element(
                By.XPATH, "//div[@aria-label='Post']"
            )
            post_btn.click()
            time.sleep(5)  # Wait for post to complete
            
    def close(self):
        """Close browser session"""
        self.driver.close()


if __name__ == "__main__":
    # Configure these variables before running
    FB_USERNAME = "your_facebook@email.com"
    FB_PASSWORD = "yourpassword"
    IMAGE_PATH = "path/to/your/image.jpg"
    GROUP_URLS = [
        "https://www.facebook.com/groups/group1",
        "https://www.facebook.com/groups/group2"
    ]
    POST_TEXT = "Check out this image posted automatically!"
    
    poster = FacebookPoster(FB_USERNAME, FB_PASSWORD, IMAGE_PATH, GROUP_URLS)
    try:
        poster.login()
        poster.post_to_groups(POST_TEXT)
    finally:
        poster.close()