"""
Test suite for data loading functionality.
"""
import pytest
import pandas as pd
from sqlalchemy import create_engine
import os
from src.data_loader import DataLoader

@pytest.fixture
def sample_data():
    """Create sample campaign data."""
    return pd.DataFrame({
        'campaign_id': [1, 2, 3],
        'campaign_name': ['Test1', 'Test2', 'Test3'],
        'channel': ['Email', 'Social', 'Search'],
        'cost': [100, 200, 300],
        'impressions': [1000, 2000, 3000],
        'clicks': [100, 200, 300],
        'conversions': [10, 20, 30],
        'revenue': [200, 400, 600],
        'date': ['2023-01-01', '2023-01-02', '2023-01-03']
    })

@pytest.fixture
def test_db():
    """Create test database connection."""
    engine = create_engine('sqlite:///:memory:')
    return engine

def test_load_campaigns(test_db, sample_data):
    """Test loading campaign data."""
    # Setup
    sample_data.to_sql('campaigns', test_db, index=False)

    # Create loader with test config
    loader = DataLoader()
    loader.engine = test_db

    # Test
    result = loader.load_campaigns()
    assert isinstance(result, pd.DataFrame)
    assert len(result) == len(sample_data)
    assert all(result.columns == sample_data.columns)

def test_save_to_csv(tmp_path, sample_data):
    """Test saving data to CSV."""
    # Setup
    loader = DataLoader()
    output_file = "test_output.csv"

    # Test
    loader.save_to_csv(sample_data, output_file, tmp_path)
    saved_data = pd.read_csv(tmp_path / output_file)

    assert os.path.exists(tmp_path / output_file)
    assert len(saved_data) == len(sample_data)

def test_invalid_sql_file():
    """Test handling of invalid SQL file."""
    loader = DataLoader()
    with pytest.raises(FileNotFoundError):
        loader.load_sql_file("nonexistent.sql")
