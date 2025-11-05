"""
Data loader module for marketing campaign analysis.
"""
import os
from pathlib import Path
from typing import Dict, Optional, Union
import pandas as pd
import yaml
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize DataLoader with configuration."""
        self.config = self._load_config(config_path)
        self.base_path = Path(__file__).parent.parent
        self.db_config = self._load_db_config()
        self.engine = self._create_db_engine()

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        if not os.path.isabs(config_path):
            config_path = os.path.join(Path(__file__).parent.parent, config_path)

        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _load_db_config(self) -> Dict:
        """Load database configuration from YAML file."""
        db_config_path = self.base_path / 'config' / 'database_config.yaml'
        try:
            with open(db_config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading database config: {str(e)}")
            raise

    def _create_db_engine(self):
        """Create SQLAlchemy database engine."""
        try:
            mysql_config = self.db_config['mysql']
            connection_template = self.db_config['connection_string']

            connection_string = connection_template.format(
                user=mysql_config['user'],
                password=mysql_config['password'],
                host=mysql_config['host'],
                port=mysql_config['port'],
                database=mysql_config['database']
            )

            engine = create_engine(connection_string, echo=False)
            logger.info("Database engine created successfully")
            return engine
        except Exception as e:
            logger.error(f"Error creating database engine: {str(e)}")
            raise

    def load_campaigns(self) -> pd.DataFrame:
        """Load campaign data from database."""
        try:
            query = """
                SELECT campaign_name, channel, cost, impressions, clicks, 
                       conversions, revenue, date
                FROM campaigns
                ORDER BY date
            """
            logger.info("Loading campaign data from database")
            df = pd.read_sql(query, self.engine)
            df['date'] = pd.to_datetime(df['date'])
            logger.info(f"Loaded {len(df)} campaign records from database")
            return df
        except SQLAlchemyError as e:
            logger.error(f"Database error loading campaign data: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error loading campaign data: {str(e)}")
            raise

    def load_customers(self) -> pd.DataFrame:
        """Load customer data from database."""
        try:
            query = """
                SELECT age, gender, country, sessions, avg_session_duration, 
                       pages_per_session, transactions, revenue
                FROM customers
            """
            logger.info("Loading customer data from database")
            df = pd.read_sql(query, self.engine)
            logger.info(f"Loaded {len(df)} customer records from database")
            return df
        except SQLAlchemyError as e:
            logger.error(f"Database error loading customer data: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error loading customer data: {str(e)}")
            raise

    def save_to_csv(self, df: pd.DataFrame, filename: str, output_dir: str = "data/processed") -> None:
        """Save DataFrame to CSV file."""
        try:
            output_path = self.base_path / output_dir / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(output_path, index=False)
            logger.info(f"Data saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving data to CSV: {str(e)}")
            raise

    def close(self):
        """Close database connection."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)

    # Example usage
    with DataLoader() as loader:
        campaigns_df = loader.load_campaigns()
        customers_df = loader.load_customers()
        print(f"Loaded {len(campaigns_df)} campaigns and {len(customers_df)} customers")
