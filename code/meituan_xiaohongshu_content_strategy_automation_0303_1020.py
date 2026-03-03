#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Source: Freyasrepo/TT-Refugee-Adaptation (https://github.com/Freyasrepo/TT-Refugee-Adaptation)
Date: 2024-03-20
Description: Analyzes TikTok refugee migration to Xiaohongshu using unsupervised learning.
"""

import pandas as pd
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import NMF
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

def clean_text(text):
    """Cleans text by removing special chars and normalizing"""
    if not isinstance(text, str):
        return ""
    # Remove special characters and emojis
    text = re.sub(r'[^\w\s]', '', text)
    # Normalize mixed Chinese/English
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def convert_engagement(val):
    """Converts Xiaohongshu engagement notations (e.g., '1万+') to numbers"""
    if isinstance(val, str):
        if '万+' in val:
            return float(val.replace('万+', '')) * 10000
        elif '万' in val:
            return float(val.replace('万', '')) * 10000
    return float(val)

def load_and_preprocess(filepath):
    """Loads dataset and applies preprocessing"""
    df = pd.read_csv(filepath)
    
    # Clean text columns
    text_cols = ['title', 'content']
    for col in text_cols:
        df[col] = df[col].apply(clean_text)
    
    # Convert engagement metrics
    engagement_cols = ['collects', 'comments', 'shares', 'likes']
    for col in engagement_cols:
        df[col] = df[col].apply(convert_engagement)
    
    # Handle missing values
    df.fillna({'post_type': 'unknown', 'engagement_level': 'medium'}, inplace=True)
    
    return df

def extract_features(df):
    """Extracts features for modeling"""
    # Behavioral features
    behavioral = df[['collects', 'comments', 'shares', 'likes']]
    
    # Text features using TF-IDF
    tfidf = TfidfVectorizer(max_features=100)
    text_features = tfidf.fit_transform(df['content'])
    
    # Combine features
    features = np.hstack([behavioral.values, text_features.toarray()])
    return StandardScaler().fit_transform(features)

def cluster_users(features, n_clusters=4):
    """Performs K-Means clustering"""
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(features)
    return clusters

def topic_modeling(df, n_topics=5):
    """Performs topic modeling using NMF"""
    tfidf = TfidfVectorizer(max_features=500)
    tfidf_matrix = tfidf.fit_transform(df['content'])
    
    nmf = NMF(n_components=n_topics, random_state=42)
    topic_probs = nmf.fit_transform(tfidf_matrix)
    
    # Get top words per topic
    feature_names = tfidf.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(nmf.components_):
        topics.append([feature_names[i] for i in topic.argsort()[:-6:-1]])
    
    return topic_probs, topics

def visualize_results(df, clusters, topic_probs):
    """Creates visualizations"""
    # Behavioral features by cluster
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=clusters, y=df['likes'])
    plt.title('Engagement Distribution by Cluster')
    plt.show()
    
    # Topic visualization
    plt.figure(figsize=(10, 6))
    sns.heatmap(topic_probs[:10], cm