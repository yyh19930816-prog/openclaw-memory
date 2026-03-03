#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Source: ColombiaPython/social-media-automation (https://github.com/ColombiaPython/social-media-automation)
Date: 2023-03-15
Description: Selenium script to post images with text to Facebook, Twitter, and LinkedIn
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os

def facebook_post(email, password, image_path, group_url):
    """Post image with text to a Facebook group"""
    try:
        # Setup Firefox driver
        driver = webdriver.Firefox(executable_path='/path/to/geckodriver')
        driver.get("https://www.facebook.com")
        
        # Login
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys(email)
        
        password_field = driver.find_element(By.ID, "pass")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        
        # Wait for login to complete
        time.sleep(5)
        
        # Navigate to group
        if group_url:
            driver.get(group_url)
            time.sleep(3)
            
        # Post image
        if image_path:
            post_box = driver.find_element(By.XPATH, "//div[@aria-label='Create a post']")
            post_box.click()
            time.sleep(2)
            
            add_photo = driver.find_element(By.XPATH, "//input[@type='file']")
            add_photo.send_keys(os.path.abspath(image_path))
            time.sleep(5)  # Wait for upload
            
        # Submit post
        post_button = driver.find_element(By.XPATH, "//div[@aria-label='Post']")
        post_button.click()
        time.sleep(5)
        
    except Exception as e:
        print(f"Error posting to Facebook: {str(e)}")
    finally:
        driver.quit()

def twitter_post(username, password, image_path, tweet_text):
    """Post image with text to Twitter"""
    try:
        driver = webdriver.Firefox(executable_path='/path/to/geckodriver')
        driver.get("https://twitter.com/login")
        
        # Login
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='username']"))
        )
        username_field.send_keys(username)
        username_field.send_keys(Keys.RETURN)
        
        time.sleep(2)
        
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='current-password']"))
        )
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        
        # Compose tweet
        time.sleep(5)
        tweet_box = driver.find_element(By.XPATH, "//div[@aria-label='Tweet text']")
        tweet_box.send_keys(tweet_text)
        
        # Add image
        if image_path:
            image_button = driver.find_element(By.XPATH, "//input[@data-testid='fileInput']")
            image_button.send_keys(os.path.abspath(image_path))
            time.sleep(5)  # Wait for upload
            
        # Tweet
        tweet_button = driver.find_element(By.XPATH, "//div[@data-testid='tweetButton']")
        tweet_button.click()
        time.sleep(5)
        
    except Exception as e:
        print(f"Error posting to Twitter: {str(e)}")
    finally:
        driver.quit()

def linkedin_post(email, password, image_path, post_text, company_url=None):
    """Post image with text to LinkedIn (profile or company)"""
    try:
        driver = webdriver.Firefox(executable_path='/path/to/geckodriver')
        driver.get("https://www.linkedin.com/login")
        
        # Login
        email_field = driver.find_element