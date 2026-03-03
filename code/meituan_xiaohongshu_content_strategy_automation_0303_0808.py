#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Source: Freya's Repo - TT-Refugee-Adaptation (https://github.com/Freyasrepo/TT-Refugee-Adaptation)
Date: April 2024
Description: Analyzes TikTok refugee migration to Xiaohongshu using unsupervised learning.
Focuses on behavioral patterns, content adaptation, and engagement metrics.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import NMF
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Data loading and preprocessing
def load_and_preprocess(filepath):
    """Load Xiaohongshu dataset and preprocess text/engagement metrics"""
    df = pd.read_csv(filepath)
    
    # Clean text: remove special chars and normalize
    df['clean_text'] = df['content'].apply(lambda x: re.sub(r'[^\w\s]', '', str(x)))
    
    # Convert engagement metrics ('1万+' -> 10000)
    for col in ['collects', 'comments', 'shares', 'likes']:
        df[col] = df[col].apply(lambda x: int(float(str(x).replace('万+', '')) * 10000) 
                                if '万+' in str(x) else int(float(str(x))))
    
    # Extract temporal features
    df['post_time'] = pd.to_datetime(df['post_time'])
    df['post_hour'] = df['post_time'].dt.hour
    df['post_day'] = df['post_time'].dt.day
    
    return df

# Feature extraction with TF-IDF
def extract_text_features(df, max_features=1000):
    """Extract keywords using TF-IDF"""
    tfidf = TfidfVectorizer(max_features=max_features, stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['clean_text'])
    return tfidf_matrix, tfidf

# Cluster analysis using K-Means
def cluster_users(tfidf_matrix, n_clusters=5):
    """Cluster users based on content similarity"""
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(tfidf_matrix)
    return clusters

# Topic modeling with NMF
def extract_topics(tfidf_matrix, tfidf, n_topics=5):
    """Extract dominant topics using Non-Negative Matrix Factorization"""
    nmf = NMF(n_components=n_topics, random_state=42)
    nmf_features = nmf.fit_transform(tfidf_matrix)
    
    # Get top words per topic
    feature_names = tfidf.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(nmf.components_):
        topics.append([feature_names[i] for i in topic.argsort()[:-10:-1]])
    
    return nmf_features, topics

# Visualization functions
def plot_engagement_distribution(df):
    """Plot distribution of engagement metrics"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    sns.histplot(df['likes'], ax=axes[0, 0], kde=True)
    sns.histplot(df['comments'], ax=axes[0, 1], kde=True)
    sns.histplot(df['shares'], ax=axes[1, 0], kde=True)
    sns.histplot(df['collects'], ax=axes[1, 1], kde=True)
    plt.tight_layout()
    plt.savefig('engagement_dist.png')

def plot_topic_words(topics):
    """Visualize top words per topic"""
    plt.figure(figsize=(10, 6))
    for i, topic in enumerate(topics):
        plt.barh(range(len(topic)), topic, label=f'Topic {i+1}')
    plt.yticks(range(len(topics[0])), topics[0])
    plt.ylabel('Top Keywords')
    plt.legend