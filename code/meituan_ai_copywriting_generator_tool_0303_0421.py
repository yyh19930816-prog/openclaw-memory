# EmailGenie-AI-Powered-Email-Copywriting-Generator
# Source: https://github.com/HarieshKumar17/EmailGenie-AI-Powered-Email-Copywriting-Generator
# Date: 2023-11-15
# Description: Streamlit-based email generator with profile management

import streamlit as st
import pandas as pd
import sqlite3
from sqlite3 import Error
from datetime import datetime
import os

# Initialize database connection
def create_connection():
    """Create SQLite database connection"""
    conn = None
    try:
        conn = sqlite3.connect('emailgenie.db')
        return conn
    except Error as e:
        st.error(f"Database connection error: {e}")
    return conn

def initialize_db(conn):
    """Initialize database tables if they don't exist"""
    try:
        cursor = conn.cursor()
        
        # Profiles table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_name TEXT NOT NULL,
            industry TEXT,
            target_audience TEXT,
            background TEXT,
            sender_name TEXT,
            sender_company TEXT,
            sender_email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
    except Error as e:
        st.error(f"Database initialization error: {e}")

def save_profile(conn, profile_data):
    """Save new profile to database"""
    try:
        sql = '''
        INSERT INTO profiles(
            profile_name, industry, target_audience, 
            background, sender_name, sender_company, sender_email
        ) VALUES(?,?,?,?,?,?,?)
        '''
        cursor = conn.cursor()
        cursor.execute(sql, profile_data)
        conn.commit()
        return True
    except Error as e:
        st.error(f"Profile save error: {e}")
        return False

def load_profiles(conn):
    """Load all profiles from database"""
    try:
        query = "SELECT * FROM profiles ORDER BY created_at DESC"
        df = pd.read_sql(query, conn)
        return df
    except Error as e:
        st.error(f"Profile load error: {e}")
        return pd.DataFrame()

def main():
    """Main application function"""
    st.set_page_config(page_title="EmailGenie", page_icon=":email:")
    st.title("EmailGenie - AI Email Copywriting")
    
    # Initialize database
    conn = create_connection()
    if conn is not None:
        initialize_db(conn)
    else:
        st.error("Database connection failed!")
        return
    
    # Profile Management Section
    st.header("User Profile Setup")
    
    # Create new profile
    st.subheader("Create New Profile")
    with st.form("profile_form"):
        profile_name = st.text_input("Profile Name*")
        industry = st.text_input("Industry*")
        target_audience = st.text_input("Target Audience*")
        background = st.text_area("Personal/Company Background*")
        sender_name = st.text_input("Your Name*")
        sender_company = st.text_input("Your Company/Role*")
        sender_email = st.text_input("Your Email*")
        
        submitted = st.form_submit_button("Save Profile")
        if submitted:
            required_fields = [
                profile_name, industry, target_audience,
                background, sender_name, sender_company, sender_email
            ]
            if all(required_fields):
                profile_data = (
                    profile_name, industry, target_audience,
                    background, sender_name, sender_company, sender_email
                )
                if save_profile(conn, profile_data):
                    st.success("Profile saved successfully!")
            else:
                st.error("Please fill in all required fields (*)")
    
    # Display existing profiles
    st.subheader("Existing Profiles")
    profiles = load_profiles(conn)
    if not profiles.empty:
        for _, profile in profiles.iterrows():
            with st.expander(f"Profile: {profile['profile_name']}"):
                st.write(f"**Industry:** {profile['industry']}")
                st.write(f"**Target Audience:** {profile['target_audience']}")
                st.write