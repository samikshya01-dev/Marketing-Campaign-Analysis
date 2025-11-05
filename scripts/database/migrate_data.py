"""
Data migration script to import CSV data into MySQL database.
"""
import yaml
import logging
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_db_config():
    """Load database configuration."""
    config_path = Path(__file__).parent / 'config' / 'database_config.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def create_db_engine(config):
    """Create database engine."""
    mysql_config = config['mysql']
    connection_string = config['connection_string'].format(
        user=mysql_config['user'],
        password=mysql_config['password'],
        host=mysql_config['host'],
        port=mysql_config['port'],
        database=mysql_config['database']
    )
    return create_engine(connection_string, echo=False)

def migrate_campaigns(engine, csv_path='data/raw/marketing_campaign_raw.csv'):
    """Migrate campaign data from CSV to database."""
    try:
        csv_file = Path(__file__).parent / csv_path

        if not csv_file.exists():
            logger.warning(f"Campaign CSV file not found at {csv_file}")
            logger.info("Skipping campaign data migration. You can add data manually.")
            return 0

        logger.info(f"Reading campaign data from {csv_file}")
        df = pd.read_csv(csv_file)

        # Ensure required columns exist
        required_cols = ['campaign_name', 'channel', 'cost', 'impressions', 'clicks', 'conversions', 'revenue', 'date']
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            logger.error(f"Missing required columns in campaigns CSV: {missing_cols}")
            return 0

        # Select only required columns
        df = df[required_cols]

        # Convert date column
        df['date'] = pd.to_datetime(df['date']).dt.date

        # Insert into database
        records_inserted = df.to_sql('campaigns', engine, if_exists='append', index=False)
        logger.info(f"Successfully migrated {records_inserted} campaign records")
        return records_inserted

    except Exception as e:
        logger.error(f"Error migrating campaign data: {str(e)}")
        raise

def migrate_customers(engine, csv_path='data/raw/customer_data_raw.csv'):
    """Migrate customer data from CSV to database."""
    try:
        csv_file = Path(__file__).parent / csv_path

        if not csv_file.exists():
            logger.warning(f"Customer CSV file not found at {csv_file}")
            logger.info("Skipping customer data migration. You can add data manually.")
            return 0

        logger.info(f"Reading customer data from {csv_file}")
        df = pd.read_csv(csv_file)

        # Ensure required columns exist
        required_cols = ['age', 'gender', 'country', 'sessions', 'avg_session_duration', 'pages_per_session', 'transactions', 'revenue']
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            logger.error(f"Missing required columns in customers CSV: {missing_cols}")
            return 0

        # Select only required columns
        df = df[required_cols]

        # Insert into database
        records_inserted = df.to_sql('customers', engine, if_exists='append', index=False)
        logger.info(f"Successfully migrated {records_inserted} customer records")
        return records_inserted

    except Exception as e:
        logger.error(f"Error migrating customer data: {str(e)}")
        raise

def verify_migration(engine):
    """Verify data was migrated successfully."""
    try:
        # Check campaigns
        campaigns_count = pd.read_sql("SELECT COUNT(*) as count FROM campaigns", engine)
        logger.info(f"Total campaigns in database: {campaigns_count['count'].iloc[0]}")

        # Check customers
        customers_count = pd.read_sql("SELECT COUNT(*) as count FROM customers", engine)
        logger.info(f"Total customers in database: {customers_count['count'].iloc[0]}")

        # Show sample data
        logger.info("\nSample campaign data:")
        sample_campaigns = pd.read_sql("SELECT * FROM campaigns LIMIT 3", engine)
        print(sample_campaigns.to_string())

        logger.info("\nSample customer data:")
        sample_customers = pd.read_sql("SELECT * FROM customers LIMIT 3", engine)
        print(sample_customers.to_string())

    except Exception as e:
        logger.error(f"Error verifying migration: {str(e)}")
        raise

def main():
    """Main migration function."""
    try:
        logger.info("Starting data migration...")
        logger.info("=" * 60)

        # Load configuration
        config = load_db_config()

        # Create engine
        engine = create_db_engine(config)

        # Migrate campaigns
        logger.info("Step 1: Migrating campaign data...")
        campaigns_migrated = migrate_campaigns(engine)

        # Migrate customers
        logger.info("\nStep 2: Migrating customer data...")
        customers_migrated = migrate_customers(engine)

        # Verify
        if campaigns_migrated > 0 or customers_migrated > 0:
            logger.info("\nStep 3: Verifying migration...")
            verify_migration(engine)

        # Close connection
        engine.dispose()

        logger.info("=" * 60)
        logger.info("Data migration completed successfully!")
        logger.info("=" * 60)

        if campaigns_migrated == 0 and customers_migrated == 0:
            logger.info("\nNo CSV files found to migrate.")
            logger.info("Please add your data directly to the database or place CSV files in:")
            logger.info("  - data/raw/marketing_campaign_raw.csv")
            logger.info("  - data/raw/customer_data_raw.csv")
        else:
            logger.info("\nYou can now run the analysis using: ./run_analysis.sh")

    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        logger.error("\nPlease ensure:")
        logger.error("1. Database and tables are set up (run setup_database.py first)")
        logger.error("2. CSV files have the correct column names")
        logger.error("3. Database connection is working")
        raise

if __name__ == "__main__":
    main()

