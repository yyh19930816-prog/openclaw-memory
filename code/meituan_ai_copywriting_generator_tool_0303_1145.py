#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
EmailGenie - AI-Powered Email Copywriting Generator
Source: github.com/HarieshKumar17/EmailGenie-AI-Powered-Email-Copywriting-Generator
Created: 2023-08-15
A Streamlit app for generating AI-powered email templates with profile management.
"""

import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('emailgenie.db')
    c = conn.cursor()
    
    # Create profiles table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS profiles
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  profile_name TEXT,
                  industry TEXT,
                  target_audience TEXT,
                  background TEXT,
                  sender_name TEXT,
                  sender_company TEXT,
                  sender_email TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Create templates table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS templates
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  template_name TEXT,
                  template_type TEXT,
                  content TEXT,
                  profile_id INTEGER,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()

# Save profile to database
def save_profile(profile_data):
    conn = sqlite3.connect('emailgenie.db')
    c = conn.cursor()
    
    c.execute('''INSERT INTO profiles 
                 (profile_name, industry, target_audience, background, sender_name, sender_company, sender_email)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              profile_data)
    
    conn.commit()
    conn.close()

# Load all profiles from database
def load_profiles():
    conn = sqlite3.connect('emailgenie.db')
    profiles = pd.read_sql('SELECT * FROM profiles ORDER BY created_at DESC', conn)
    conn.close()
    return profiles

# Main app function
def main():
    # Initialize database
    init_db()
    
    # Page configuration
    st.set_page_config(page_title="EmailGenie", page_icon="📧", layout="wide")
    
    st.title("📧 EmailGenie - AI Email Generator")
    st.subheader("Create compelling emails with AI assistance")
    
    # Navigation tabs
    tab1, tab2, tab3 = st.tabs(["Profile Setup", "Email Templates", "Send Email"])
    
    # Profile Setup Tab
    with tab1:
        st.header("👤 User Profile Setup")
        
        # Create new profile form
        with st.form("profile_form"):
            st.subheader("Create New Profile")
            col1, col2 = st.columns(2)
            
            with col1:
                profile_name = st.text_input("Profile Name*")
                industry = st.text_input("Industry*")
                target_audience = st.text_input("Target Audience*")
                
            with col2:
                sender_name = st.text_input("Your Name*")
                sender_company = st.text_input("Your Company/Role*")
                sender_email = st.text_input("Your Email*")
            
            background = st.text_area("Personal/Company Background*")
            
            submitted = st.form_submit_button("Save Profile")
            
            if submitted:
                if all([profile_name, industry, target_audience, background, 
                        sender_name, sender_company, sender_email]):
                    profile_data = (
                        profile_name, industry, target_audience, 
                        background, sender_name, sender_company, 
                        sender_email
                    )
                    save_profile(profile_data)
                    st.success("Profile saved successfully!")
                else:
                    st.error("Please fill in all required fields (*)")
        
        # Display existing profiles
        st.subheader("🔍 Existing Profiles")
        profiles = load_profiles()
        
        if not profiles.empty:
            for _, profile in profiles.iterrows():
                with st.expander(f"🏷 {profile['profile_name']} (Created: {profile['created_at']})"):
                    st.write(f"**Industry:** {profile['industry']}")
                    st.write(f"**Target Audience:** {profile['target_aud