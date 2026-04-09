import pandas as pd
from sklearn.cluster import KMeans
import joblib
from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Run ETL Customer Segmentation'

    def handle(self, *args, **kwargs):
        df = pd.read_csv('customer_prediction.csv')
        print("DATA LOADED:", df.shape)

        # Handle missing prev columns
        if 'prev_spending' not in df.columns:
            df['prev_spending'] = df['total_spending'] * 0.8
        if 'prev_rental' not in df.columns:
            df['prev_rental'] = df['rental_count'] - 1

        # Features
        features = df[['total_spending', 'rental_count', 'prev_spending', 'prev_rental']]

        # KMeans clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        df['cluster'] = kmeans.fit_predict(features)

        # Save model
        joblib.dump(kmeans, 'kmeans_model.pkl')
        print("KMeans model saved")

        # Cluster summary
        cluster_summary = df.groupby('cluster').agg({
            'total_spending': 'mean',
            'rental_count': 'mean',
            'prev_spending': 'mean',
            'prev_rental': 'mean'
        }).reset_index()
        cluster_summary.columns = ['cluster', 'avg_spending', 'avg_rental', 'avg_prev_spending', 'avg_prev_rental']
        cluster_summary.to_csv('cluster_summary.csv', index=False)
        print("cluster_summary.csv saved")

        # Segment labeling
        df['segment'] = df['cluster'].map({0:'Low Value',1:'Loyal',2:'High Value'})
        df.to_csv('customer_segmentation.csv', index=False)
        print("customer_segmentation.csv saved")
        print("ETL FINAL SUCCESS")