#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Source: Freyasrepo/TT-Refugee-Adaptation (https://github.com/Freyasrepo/TT-Refugee-Adaptation)
Date: 2025-03-15
Description: Analyzes TikTok refugee migration to Xiaohongshu using unsupervised learning.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import NMF
import re
import matplotlib.pyplot as plt
import seaborn as sns

# Data Loading and Preprocessing
def load_and_clean_data(filepath):
    """Loads Xiaohongshu dataset and cleans text/numeric features."""
    df = pd.read_csv(filepath)
    
    # Clean text data
    df['content'] = df['content'].apply(lambda x: re.sub(r'[^\w\s]', '', str(x)))
    
    # Convert engagement metrics (e.g., '1万+' -> 10000)
    for col in ['collects', 'comments', 'shares', 'likes']:
        df[col] = df[col].apply(lambda x: float(x.replace('万+', '0000') if '万+' in str(x) else x))
    
    # Fill missing values
    df.fillna({'collects': 0, 'comments': 0, 'shares': 0, 'likes': 0}, inplace=True)
    
    return df

# Feature Extraction
def extract_features(df):
    """Extracts TF-IDF text features and behavioral metrics."""
    # TF-IDF Vectorization
    tfidf = TfidfVectorizer(max_features=100, stop_words=['的', '了', '我'])
    text_features = tfidf.fit_transform(df['content'])
    
    # Behavioral Features
    behavioral_features = df[['collects', 'comments', 'shares', 'likes']].values
    
    return text_features, behavioral_features

# Unsupervised Learning
def apply_clustering(text_features, behavioral_features, n_clusters=5):
    """Applies K-Means clustering and NMF topic modeling."""
    # Combined features normalization
    combined_features = np.hstack([text_features.toarray(), behavioral_features])
    
    # K-Means Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(combined_features)
    
    # NMF Topic Modeling (on text features)
    nmf = NMF(n_components=5, random_state=42)
    topics = nmf.fit_transform(text_features)
    
    return clusters, topics

# Visualization
def visualize_results(df, clusters):
    """Generates EDA visualizations."""
    plt.figure(figsize=(12, 6))
    
    # Distribution of Engagement Metrics
    plt.subplot(1, 2, 1)
    sns.boxplot(data=df[['likes', 'collects', 'comments', 'shares']])
    plt.title('Engagement Metrics Distribution')
    
    # Cluster Distribution
    plt.subplot(1, 2, 2)
    sns.countplot(x=clusters)
    plt.title('User Cluster Distribution')
    
    plt.tight_layout()
    plt.savefig('results.png')

# Main Execution
if __name__ == "__main__":
    # Configuration
    DATA_PATH = 'xiaohongshu_posts.csv'
    
    # Pipeline
    print("Loading and cleaning data...")
    df = load_and_clean_data(DATA_PATH)
    
    print("Extracting features...")
    text_features, behavioral_features = extract_features(df)
    
    print("Applying clustering algorithms...")
    clusters, topics = apply_clustering(text_features, behavioral_features)
    
    print("Generating visualizations...")
    df['cluster'] = clusters
    visualize_results(df, clusters)
    
    print("Analysis complete. Results saved to results.png")