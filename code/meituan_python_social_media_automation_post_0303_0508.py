#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Source: ColombiaPython/social-media-automation
Date: 2023-11-08
Description: Selenium script to post images with text on Facebook groups
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FacebookPoster:
    def __init__(self, username, password, image_path, group_urls, driver_path):
        """
        Initialize Facebook poster bot
        
        Args:
            username (str): Facebook username/email
            password (str): Facebook password
            image_path (str): Path to image to post
            group_urls (list): List of Facebook group URLs
            driver_path (str): Path to geckodriver executable
        """
        self.username = username
        self.password = password
        self.image_path = image_path
        self.group_urls = group_urls
        self.driver_path = driver_path
        
        # Set up Firefox options
        options = webdriver.FirefoxOptions()
        options.headless = False
        
        # Initialize driver
        self.driver = webdriver.Firefox(
            executable_path=self.driver_path,
            options=options
        )
        self.wait = WebDriverWait(self.driver, 20)

    def login(self):
        """Log into Facebook"""
        self.driver.get("https://www.facebook.com")
        
        # Fill in login form
        email_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_field.send_keys(self.username)
        
        password_field = self.driver.find_element(By.ID, "pass")
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.RETURN)
        
        # Wait for login to complete
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='navigation']"))
        )

    def post_to_group(self, group_url):
        """Post image and text to a Facebook group"""
        self.driver.get(group_url)
        
        # Find post box
        post_box = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
        )
        post_box.click()
        
        # Add photo
        photo_button = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Photo/Video']"))
        )
        photo_button.click()
        
        # Upload image
        file_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        file_input.send_keys(os.path.abspath(self.image_path))
        
        # Wait for upload to complete
        time.sleep(5)
        
        # Post button
        post_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Post']"))
        )
        post_button.click()
        
        # Wait for post to complete
        time.sleep(5)

    def post_to_all_groups(self):
        """Post to all groups in the list"""
        self.login()
        
        for group_url in self.group_urls:
            try:
                self.post_to_group(group_url)
                print(f"Successfully posted to {group_url}")
            except Exception as e:
                print(f"Error posting to {group_url}: {str(e)}")
                
        self.driver.quit()

if __name__ == "__main__":
    # Configure these values before running
    USERNAME = "your_facebook_email@example.com"
    PASSWORD = "your_facebook_password"
    IMAGE_PATH = "./sample.jpg"  # Path to your image
    GROUP_URLS = [
        "https://www.facebook.com/groups/samplegroup1",
        "https://www.facebook.com/groups/samplegroup2"
    ]
    DRIVER_PATH = "./geckodriver"  # Path to