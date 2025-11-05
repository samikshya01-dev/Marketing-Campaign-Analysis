"""
Test script to verify database connection and data loading.
Run this after setting up the database to ensure everything works.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_loader import DataLoader
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_database_connection():
    """Test database connection and data loading."""
    try:
        logger.info("=" * 60)
        logger.info("Testing Database Connection")
        logger.info("=" * 60)

        # Initialize DataLoader
        logger.info("\n1. Initializing DataLoader...")
        loader = DataLoader()
        logger.info("✓ DataLoader initialized successfully")

        # Test campaigns loading
        logger.info("\n2. Loading campaigns data...")
        campaigns_df = loader.load_campaigns()
        logger.info(f"✓ Loaded {len(campaigns_df)} campaign records")
        logger.info(f"   Columns: {list(campaigns_df.columns)}")
        logger.info(f"   Date range: {campaigns_df['date'].min()} to {campaigns_df['date'].max()}")

        # Show sample campaigns
        logger.info("\n   Sample campaigns:")
        print(campaigns_df.head(3).to_string())

        # Test customers loading
        logger.info("\n3. Loading customers data...")
        customers_df = loader.load_customers()
        logger.info(f"✓ Loaded {len(customers_df)} customer records")
        logger.info(f"   Columns: {list(customers_df.columns)}")

        # Show sample customers
        logger.info("\n   Sample customers:")
        print(customers_df.head(3).to_string())

        # Basic statistics
        logger.info("\n4. Data Statistics:")
        logger.info(f"   Total Revenue (Campaigns): ${campaigns_df['revenue'].sum():,.2f}")
        logger.info(f"   Total Cost (Campaigns): ${campaigns_df['cost'].sum():,.2f}")
        logger.info(f"   Total Conversions: {campaigns_df['conversions'].sum():,}")
        logger.info(f"   Unique Channels: {campaigns_df['channel'].nunique()}")
        logger.info(f"   Channels: {', '.join(campaigns_df['channel'].unique())}")

        logger.info(f"\n   Total Revenue (Customers): ${customers_df['revenue'].sum():,.2f}")
        logger.info(f"   Total Transactions: {customers_df['transactions'].sum():,}")
        logger.info(f"   Unique Countries: {customers_df['country'].nunique()}")

        # Close connection
        loader.close()
        logger.info("\n✓ Database connection closed")

        # Success message
        logger.info("\n" + "=" * 60)
        logger.info("✅ All tests passed! Database is ready.")
        logger.info("=" * 60)
        logger.info("\nYou can now run the full analysis:")
        logger.info("  ./run_analysis.sh")
        logger.info("  ./run_analysis.sh --export-powerbi")

        return True

    except FileNotFoundError as e:
        logger.error("\n❌ Configuration file not found")
        logger.error(f"   Error: {str(e)}")
        logger.error("\nPlease ensure config/database_config.yaml exists")
        return False

    except Exception as e:
        logger.error("\n❌ Test failed!")
        logger.error(f"   Error: {str(e)}")
        logger.error("\nTroubleshooting:")
        logger.error("  1. Check MySQL is running: mysql --version")
        logger.error("  2. Verify credentials in config/database_config.yaml")
        logger.error("  3. Ensure database and tables exist: python3 setup_database.py")
        logger.error("  4. Check if data is loaded: python3 migrate_data.py")
        logger.error("  5. Try manual connection: mysql -u root -p marketing_db")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)

