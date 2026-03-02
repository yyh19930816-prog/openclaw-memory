# Source: HarieshKumar17/EmailGenie-AI-Powered-Email-Copywriting-Generator
# Date: 2023-11-15
# Description: Core profile management system for EmailGenie AI email generator

import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import os

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('emailgenie_profiles.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS profiles
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  profile_name TEXT,
                  industry TEXT,
                  target_audience TEXT,
                  background TEXT,
                  sender_name TEXT,
                  sender_company TEXT,
                  sender_email TEXT,
                  created_at TIMESTAMP)''')
    conn.commit()
    conn.close()

# Save new profile to database
def save_profile(profile_name, industry, target_audience, background, 
                 sender_name, sender_company, sender_email):
    conn = sqlite3.connect('emailgenie_profiles.db')
    c = conn.cursor()
    c.execute('''INSERT INTO profiles 
                 (profile_name, industry, target_audience, background,
                  sender_name, sender_company, sender_email, created_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (profile_name, industry, target_audience, background,
               sender_name, sender_company, sender_email, datetime.now()))
    conn.commit()
    conn.close()
    st.success(f"Profile '{profile_name}' saved successfully!")

# Load all profiles from database
def load_profiles():
    conn = sqlite3.connect('emailgenie_profiles.db')
    try:
        profiles = pd.read_sql('SELECT * FROM profiles ORDER BY created_at DESC', conn)
    except:
        profiles = pd.DataFrame()  # Return empty DataFrame if no profiles exist
    conn.close()
    return profiles

# Delete a profile from database
def delete_profile(profile_id):
    conn = sqlite3.connect('emailgenie_profiles.db')
    c = conn.cursor()
    c.execute('DELETE FROM profiles WHERE id = ?', (profile_id,))
    conn.commit()
    conn.close()
    st.success("Profile deleted successfully!")

# Main profile management function
def user_profile_setup():
    st.header("📝 User Profile Setup")
    
    # Create new profile section
    st.subheader("Create New Profile")
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            profile_name = st.text_input("Profile Name*", help="Give your profile a unique name")
            industry = st.text_input("Industry*", help="e.g. SaaS, Marketing, Healthcare")
            target_audience = st.text_input("Target Audience*", help="Who you typically email")
        with col2:
            sender_name = st.text_input("Your Name*")
            sender_company = st.text_input("Your Company/Role*")
            sender_email = st.text_input("Your Email*")
        
        background = st.text_area("Personal/Company Background*", 
                                help="Brief description about you/your company")
        
        if st.form_submit_button("💾 Save Profile"):
            if all([profile_name, industry, target_audience, background, 
                   sender_name, sender_company, sender_email]):
                save_profile(profile_name, industry, target_audience, background,
                           sender_name, sender_company, sender_email)
            else:
                st.error("Please fill in all required fields (*)")

    # View and manage existing profiles
    st.subheader("Existing Profiles")
    profiles = load_profiles()
    
    if not profiles.empty:
        for _, profile in profiles.iterrows():
            with st.expander(f"🔹 {profile['profile_name']}"):
                col1, col2 = st.columns([3,1])
                with col1:
                    st.write(f"**Industry:** {profile['industry']}")
                    st.write(f"**Target Audience:** {profile['target_audience']}")
                    st.write(f"**Sender:** {profile['sender_name']} ({profile['sender_company