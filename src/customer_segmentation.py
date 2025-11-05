"""
Customer segmentation module using K-Means clustering.
"""
import os
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import yaml
from typing import Tuple, List, Dict
import matplotlib.pyplot as plt
import seaborn as sns
import warnings


class CustomerSegmentation:
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize customer segmentation with configuration."""
        # Handle config path - convert to absolute if relative
        if not os.path.isabs(config_path):
            config_path = os.path.join(Path(__file__).parent.parent, config_path)

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.n_clusters = self.config['model']['clustering']['n_clusters']
        self.random_state = self.config['model']['clustering']['random_state']
        self.features = self.config['model']['clustering']['features']

        # Suppress warnings
        warnings.filterwarnings('ignore', category=FutureWarning)

    def prepare_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, StandardScaler]:
        """Prepare features for clustering."""
        # Select and scale features
        X = df[self.features].copy()
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        return pd.DataFrame(X_scaled, columns=self.features), scaler

    def segment_customers(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, KMeans]:
        """Perform customer segmentation using K-means clustering."""
        # Prepare features
        X, scaler = self.prepare_features(df)

        # Fit K-means with explicit n_init
        kmeans = KMeans(
            n_clusters=self.n_clusters,
            random_state=self.random_state,
            n_init=10  # Explicitly set n_init to suppress warning
        )
        df['cluster'] = kmeans.fit_predict(X)

        # Add segment labels
        df['segment'] = df['cluster'].map(self._get_segment_labels(df))

        return df, kmeans

    def _get_segment_labels(self, df: pd.DataFrame) -> Dict[int, str]:
        """Map cluster numbers to meaningful segment labels."""
        # Calculate average metrics for each cluster
        cluster_metrics = df.groupby('cluster').agg({
            'revenue': 'mean',
            'transactions': 'mean',
            'sessions': 'mean'
        })

        # Sort clusters by revenue to assign labels
        cluster_metrics = cluster_metrics.sort_values('revenue', ascending=False)

        # Map clusters to segment labels
        labels = {
            cluster_metrics.index[0]: "High-Value Buyers",
            cluster_metrics.index[1]: "Deal Seekers",
            cluster_metrics.index[2]: "Casual Visitors"
        }

        return labels

    def plot_segments(self, df: pd.DataFrame, output_dir: str) -> None:
        """Generate visualizations for customer segments."""
        # Set visualization style - use valid matplotlib style
        style = self.config['visualization'].get('style', 'default')
        valid_styles = ['default', 'seaborn-v0_8', 'ggplot', 'bmh', 'fivethirtyeight']
        if style not in valid_styles:
            style = 'default'

        try:
            plt.style.use(style)
        except:
            plt.style.use('default')

        # Create scatter plot of segments
        plt.figure(figsize=self.config['visualization']['figure_size'])
        sns.scatterplot(
            data=df,
            x='revenue',
            y='transactions',
            hue='segment',
            size='sessions',
            sizes=(50, 400),
            alpha=0.6
        )
        plt.title('Customer Segments')
        plt.xlabel('Revenue')
        plt.ylabel('Transactions')
        plt.savefig(f"{output_dir}/customer_segments.png",
                   dpi=self.config['visualization']['dpi'])
        plt.close()

        # Create segment profile boxplots
        plt.figure(figsize=self.config['visualization']['figure_size'])
        df.boxplot(column=self.features, by='segment')
        plt.title('Segment Profiles')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/segment_profiles.png",
                   dpi=self.config['visualization']['dpi'])
        plt.close()

    def get_segment_profiles(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate segment profile summary."""
        profiles = df.groupby('segment').agg({
            'sessions': 'mean',
            'pages_per_session': 'mean',
            'transactions': 'mean',
            'revenue': ['mean', 'sum', 'count'],
            'avg_session_duration': 'mean'
        }).round(2)

        # Calculate segment percentages
        total_customers = len(df)
        profiles['segment_percentage'] = (profiles[('revenue', 'count')] / total_customers * 100).round(1)

        return profiles


if __name__ == "__main__":
    # Example usage
    from data_loader import DataLoader
    from data_cleaner import DataCleaner

    # Load and clean data
    loader = DataLoader()
    cleaner = DataCleaner()

    customers_df = cleaner.clean_customer_data(loader.load_customers())

    # Perform segmentation
    segmentation = CustomerSegmentation()
    segmented_df, model = segmentation.segment_customers(customers_df)

    # Generate visualizations
    segmentation.plot_segments(segmented_df, "outputs/visualizations")

    # Save results
    loader.save_to_csv(segmented_df, "customer_segments.csv", "data/processed")

    # Print segment profiles
    profiles = segmentation.get_segment_profiles(segmented_df)
    print("\nSegment Profiles:")
    print(profiles)
