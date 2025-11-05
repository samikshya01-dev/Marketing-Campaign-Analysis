"""
Test suite for data cleaning functionality.
"""
import pytest
import pandas as pd
import numpy as np
from src.data_cleaner import DataCleaner

@pytest.fixture
def sample_campaign_data():
    """Create sample campaign data with issues to clean."""
    return pd.DataFrame({
        'campaign_name': ['Test_Campaign_1', 'Test_Campaign_2', None, 'Test_Campaign_4'],
        'channel': ['Email', 'Social', None, 'Search'],
        'cost': [100, 200, np.nan, 400],
        'impressions': [1000, 2000, 3000, 4000],
        'clicks': [100, np.nan, 300, 400],
        'conversions': [10, 20, 30, 40],
        'revenue': [200, 400, 600, np.nan]
    })

@pytest.fixture
def sample_customer_data():
    """Create sample customer data with issues to clean."""
    return pd.DataFrame({
        'age': [25, np.nan, 35, 40],
        'gender': ['M', 'F', None, 'M'],
        'country': ['USA', 'UK', None, 'USA'],
        'sessions': [10, 20, -1, 30],
        'avg_session_duration': [120, 240, np.nan, 1000000],
        'pages_per_session': [5, np.nan, 15, 25],
        'transactions': [2, 4, -1, 6],
        'revenue': [200, 400, np.nan, 800]
    })

def test_clean_campaign_data(sample_campaign_data):
    """Test campaign data cleaning."""
    cleaner = DataCleaner()
    cleaned = cleaner.clean_campaign_data(sample_campaign_data)

    # Check if missing values are handled
    assert cleaned['campaign_name'].isnull().sum() == 0
    assert cleaned['channel'].isnull().sum() == 0

    # Check if numeric columns are properly cleaned
    assert cleaned['cost'].isnull().sum() == 0
    assert cleaned['clicks'].isnull().sum() == 0
    assert cleaned['revenue'].isnull().sum() == 0

    # Check if campaign names are standardized
    assert not any('_' in name for name in cleaned['campaign_name'] if pd.notna(name))

def test_clean_customer_data(sample_customer_data):
    """Test customer data cleaning."""
    cleaner = DataCleaner()
    cleaned = cleaner.clean_customer_data(sample_customer_data)

    # Check if missing values are handled
    assert cleaned['age'].isnull().sum() == 0
    assert cleaned['gender'].isnull().sum() == 0
    assert cleaned['country'].isnull().sum() == 0

    # Check if numeric values are within valid ranges
    assert all(cleaned['sessions'] >= cleaner.min_sessions)
    assert all(cleaned['revenue'] >= cleaner.min_revenue)

    # Check if categorical values are standardized
    assert all(cleaned['gender'].isin(['M', 'F']))
    assert all(cleaned['country'].str.isupper())

def test_handle_outliers():
    """Test outlier handling."""
    cleaner = DataCleaner()
    data = pd.DataFrame({
        'value': [1, 2, 3, 100, 1000, -500]  # Contains outliers
    })

    cleaned = cleaner._handle_outliers(data, ['value'])

    # Check if extreme values are capped
    assert cleaned['value'].max() < 1000
    assert cleaned['value'].min() > -500

def test_data_quality_report(sample_campaign_data):
    """Test data quality report generation."""
    cleaner = DataCleaner()
    report = cleaner.get_data_quality_report(sample_campaign_data)

    assert 'total_records' in report
    assert 'missing_values' in report
    assert 'duplicates' in report
    assert 'numeric_columns_stats' in report
