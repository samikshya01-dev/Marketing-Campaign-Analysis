"""
Database setup script for marketing campaign analysis.
Creates the database and tables with proper schema.
"""
import yaml
import logging
from sqlalchemy import create_engine, text, inspect
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_db_config():
    """Load database configuration."""
    config_path = Path(__file__).parent / 'config' / 'database_config.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def create_database(config):
    """Create the database if it doesn't exist."""
    mysql_config = config['mysql']

    # Connect without database to create it
    connection_string = f"mysql+pymysql://{mysql_config['user']}:{mysql_config['password']}@{mysql_config['host']}:{mysql_config['port']}"
    engine = create_engine(connection_string, echo=False)

    try:
        with engine.connect() as conn:
            # Check if database exists
            result = conn.execute(text(f"SHOW DATABASES LIKE '{mysql_config['database']}'"))
            if result.fetchone():
                logger.info(f"Database '{mysql_config['database']}' already exists")
            else:
                conn.execute(text(f"CREATE DATABASE {mysql_config['database']}"))
                conn.commit()
                logger.info(f"Database '{mysql_config['database']}' created successfully")
    finally:
        engine.dispose()

def create_tables(config):
    """Create the campaigns and customers tables."""
    mysql_config = config['mysql']
    connection_string = config['connection_string'].format(
        user=mysql_config['user'],
        password=mysql_config['password'],
        host=mysql_config['host'],
        port=mysql_config['port'],
        database=mysql_config['database']
    )

    engine = create_engine(connection_string, echo=False)

    try:
        with engine.connect() as conn:
            # Create campaigns table
            campaigns_table = """
            CREATE TABLE IF NOT EXISTS campaigns (
                id INT AUTO_INCREMENT PRIMARY KEY,
                campaign_name VARCHAR(255) NOT NULL,
                channel VARCHAR(100) NOT NULL,
                cost DECIMAL(15, 2) NOT NULL,
                impressions INT NOT NULL,
                clicks INT NOT NULL,
                conversions INT NOT NULL,
                revenue DECIMAL(15, 2) NOT NULL,
                date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_channel (channel),
                INDEX idx_date (date),
                INDEX idx_campaign_name (campaign_name)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            conn.execute(text(campaigns_table))
            conn.commit()
            logger.info("Table 'campaigns' created successfully")

            # Create customers table
            customers_table = """
            CREATE TABLE IF NOT EXISTS customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                age INT NOT NULL,
                gender VARCHAR(20) NOT NULL,
                country VARCHAR(100) NOT NULL,
                sessions INT NOT NULL,
                avg_session_duration DECIMAL(10, 2) NOT NULL,
                pages_per_session DECIMAL(10, 2) NOT NULL,
                transactions INT NOT NULL,
                revenue DECIMAL(15, 2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_country (country),
                INDEX idx_age (age),
                INDEX idx_gender (gender)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            conn.execute(text(customers_table))
            conn.commit()
            logger.info("Table 'customers' created successfully")

    finally:
        engine.dispose()

def verify_tables(config):
    """Verify that tables were created successfully."""
    mysql_config = config['mysql']
    connection_string = config['connection_string'].format(
        user=mysql_config['user'],
        password=mysql_config['password'],
        host=mysql_config['host'],
        port=mysql_config['port'],
        database=mysql_config['database']
    )

    engine = create_engine(connection_string, echo=False)

    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        logger.info(f"Tables in database: {tables}")

        if 'campaigns' in tables:
            logger.info("✓ Table 'campaigns' exists")
            columns = [col['name'] for col in inspector.get_columns('campaigns')]
            logger.info(f"  Columns: {columns}")
        else:
            logger.error("✗ Table 'campaigns' not found")

        if 'customers' in tables:
            logger.info("✓ Table 'customers' exists")
            columns = [col['name'] for col in inspector.get_columns('customers')]
            logger.info(f"  Columns: {columns}")
        else:
            logger.error("✗ Table 'customers' not found")

    finally:
        engine.dispose()

def main():
    """Main setup function."""
    try:
        logger.info("Starting database setup...")

        # Load configuration
        config = load_db_config()

        # Create database
        logger.info("Step 1: Creating database...")
        create_database(config)

        # Create tables
        logger.info("Step 2: Creating tables...")
        create_tables(config)

        # Verify
        logger.info("Step 3: Verifying setup...")
        verify_tables(config)

        logger.info("=" * 60)
        logger.info("Database setup completed successfully!")
        logger.info("=" * 60)
        logger.info("\nNext steps:")
        logger.info("1. Insert your campaign and customer data into the database")
        logger.info("2. Run the analysis using: ./run_analysis.sh")
        logger.info("\nExample SQL to insert data:")
        logger.info("""
INSERT INTO campaigns (campaign_name, channel, cost, impressions, clicks, conversions, revenue, date)
VALUES ('Summer Sale', 'Social Media', 5000.00, 100000, 5000, 250, 25000.00, '2024-06-01');

INSERT INTO customers (age, gender, country, sessions, avg_session_duration, pages_per_session, transactions, revenue)
VALUES (25, 'Female', 'USA', 10, 120.5, 3.5, 2, 150.00);
        """)

    except Exception as e:
        logger.error(f"Error during database setup: {str(e)}")
        logger.error("\nPlease check:")
        logger.error("1. MySQL server is running")
        logger.error("2. Database credentials in config/database_config.yaml are correct")
        logger.error("3. User has permission to create databases and tables")
        raise

if __name__ == "__main__":
    main()

