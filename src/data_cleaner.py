"""
Data cleaning module for marketing campaign analysis.
Handles data preprocessing, outlier detection, and feature engineering.
"""
import os
from pathlib import Path
import numpy as np
import pandas as pd
from typing import Tuple, List, Dict
from sklearn.preprocessing import StandardScaler
import yaml


class DataCleaner:
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize DataCleaner with configuration."""
        # Handle config path - convert to absolute if relative
        if not os.path.isabs(config_path):
            config_path = os.path.join(Path(__file__).parent.parent, config_path)

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.outlier_threshold = self.config['metrics']['outlier_threshold']
        self.min_sessions = self.config['metrics']['min_sessions']
        self.min_revenue = self.config['metrics']['min_revenue']

    def clean_campaign_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess campaign data."""
        df = df.copy()

        # Handle missing values
        df = self._handle_missing_values(df)

        # Remove duplicates
        df = df.drop_duplicates()

        # Handle outliers
        df = self._handle_outliers(df, ['cost', 'impressions', 'clicks', 'conversions', 'revenue'])

        # Calculate derived metrics
        df = self._calculate_campaign_metrics(df)

        # Standardize campaign names
        df['campaign_name'] = df['campaign_name'].apply(self._standardize_campaign_name)

        return df

    def clean_customer_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess customer data."""
        df = df.copy()

        # Handle missing values and duplicates
        df = self._handle_missing_values(df)
        df = df.drop_duplicates()

        # Basic validation
        df = df[df['sessions'] >= self.min_sessions]
        df = df[df['revenue'] >= self.min_revenue]

        # Handle outliers in numerical columns
        numeric_cols = ['age', 'sessions', 'avg_session_duration', 'pages_per_session', 'transactions', 'revenue']
        df = self._handle_outliers(df, numeric_cols)

        # Standardize categorical variables
        df['gender'] = df['gender'].str.upper()
        df['country'] = df['country'].str.upper()

        return df

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in DataFrame."""
        # For numeric columns, fill with median
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

        # For categorical columns, fill with mode
        categorical_cols = df.select_dtypes(include=['object']).columns
        df[categorical_cols] = df[categorical_cols].fillna(df[categorical_cols].mode().iloc[0])

        return df

    def _handle_outliers(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Handle outliers using IQR method."""
        for col in columns:
            if col in df.columns and df[col].dtype in ['int64', 'float64']:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - self.outlier_threshold * IQR
                upper_bound = Q3 + self.outlier_threshold * IQR

                # Cap outliers at bounds
                df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)

        return df

    def _calculate_campaign_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate derived campaign metrics."""
        # Avoid division by zero
        eps = 1e-10

        # Calculate basic metrics
        df['ctr'] = (df['clicks'] / (df['impressions'] + eps)) * 100
        df['conversion_rate'] = (df['conversions'] / (df['clicks'] + eps)) * 100
        df['cost_per_click'] = df['cost'] / (df['clicks'] + eps)
        df['cost_per_conversion'] = df['cost'] / (df['conversions'] + eps)

        # Calculate ROI and ROAS
        df['roi'] = ((df['revenue'] - df['cost']) / (df['cost'] + eps)) * 100
        df['roas'] = df['revenue'] / (df['cost'] + eps)

        return df

    def _standardize_campaign_name(self, name: str) -> str:
        """Standardize campaign name format."""
        if pd.isna(name):
            return "Unknown Campaign"

        # Remove special characters and extra spaces
        name = ' '.join(name.split())
        name = name.title()

        return name

    def get_data_quality_report(self, df: pd.DataFrame) -> Dict:
        """Generate data quality report."""
        return {
            'total_records': len(df),
            'missing_values': df.isnull().sum().to_dict(),
            'duplicates': len(df) - len(df.drop_duplicates()),
            'numeric_columns_stats': df.describe().to_dict()
        }


if __name__ == "__main__":
    # Example usage
    from data_loader import DataLoader

    # Load data
    loader = DataLoader()
    campaigns_df = loader.load_campaigns()
    customers_df = loader.load_customers()

    # Clean data
    cleaner = DataCleaner()
    clean_campaigns = cleaner.clean_campaign_data(campaigns_df)
    clean_customers = cleaner.clean_customer_data(customers_df)

    # Save cleaned data
    loader.save_to_csv(clean_campaigns, "clean_campaign_data.csv", "data/processed")
    loader.save_to_csv(clean_customers, "clean_customer_data.csv", "data/processed")
