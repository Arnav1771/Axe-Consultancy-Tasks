import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import schedule
import time

# Load customer data
def load_data():
    df = pd.read_csv('customer_data.csv')
    return df

# Pre-Processing of  data
def preprocess_data(df):
    df.dropna(inplace=True)
    df['purchase_amount'] = df['purchase_amount'].astype(float)
    return df

# Analyze data to identify trends
def analyze_data(df):
    purchase_trends = df.groupby('purchase_date')['purchase_amount'].sum()
    return purchase_trends

# Segment customers using KMeans clustering
def segment_customers(df):
    features = df[['purchase_amount', 'browsing_time']]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    kmeans = KMeans(n_clusters=3)
    df['segment'] = kmeans.fit_predict(scaled_features)
    return df

# Visualize the results
def visualize_data(df, purchase_trends):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=purchase_trends)
    plt.title('Purchase Trends Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Purchase Amount')
    plt.show()
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='purchase_amount', y='browsing_time', hue='segment', data=df)
    plt.title('Customer Segmentation')
    plt.xlabel('Purchase Amount')
    plt.ylabel('Browsing Time')
    plt.show()

# Main function to run the workflow
def run_analysis():
    df = load_data()
    df = preprocess_data(df)
    purchase_trends = analyze_data(df)
    df = segment_customers(df)
    visualize_data(df, purchase_trends)

# Schedule the script to run daily
schedule.every().day.at("00:00").do(run_analysis)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)