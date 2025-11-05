# Database Setup Guide

This project now uses MySQL database to store and access campaign and customer data instead of local CSV files.

## Prerequisites

- MySQL Server 5.7+ or 8.0+
- Python 3.8+
- Required Python packages (installed automatically by run_analysis.sh)

## Database Schema

### Campaigns Table
```sql
CREATE TABLE campaigns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    campaign_name VARCHAR(255) NOT NULL,
    channel VARCHAR(100) NOT NULL,
    cost DECIMAL(15, 2) NOT NULL,
    impressions INT NOT NULL,
    clicks INT NOT NULL,
    conversions INT NOT NULL,
    revenue DECIMAL(15, 2) NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Customers Table
```sql
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    age INT NOT NULL,
    gender VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    sessions INT NOT NULL,
    avg_session_duration DECIMAL(10, 2) NOT NULL,
    pages_per_session DECIMAL(10, 2) NOT NULL,
    transactions INT NOT NULL,
    revenue DECIMAL(15, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Setup Instructions

### Step 1: Configure Database Connection

Edit `config/database_config.yaml` with your MySQL credentials:

```yaml
mysql:
  host: "localhost"
  user: "root"
  password: "your_password_here"  # Replace with your actual password
  database: "marketing_db"
  port: 3306
```

### Step 2: Create Database and Tables

Run the database setup script:

```bash
python3 setup_database.py
```

This will:
- Create the `marketing_db` database (if it doesn't exist)
- Create the `campaigns` and `customers` tables
- Verify the setup

### Step 3: Import Data (Optional)

If you have existing CSV data in `data/raw/`, you can migrate it:

```bash
python3 migrate_data.py
```

This will import data from:
- `data/raw/marketing_campaign_raw.csv` → `campaigns` table
- `data/raw/customer_data_raw.csv` → `customers` table

### Step 4: Run Analysis

Once the database is set up and populated, run the analysis:

```bash
./run_analysis.sh
```

## Manual Data Import

### Insert Campaign Data

```sql
INSERT INTO campaigns (campaign_name, channel, cost, impressions, clicks, conversions, revenue, date)
VALUES 
('Summer Sale', 'Social Media', 5000.00, 100000, 5000, 250, 25000.00, '2024-06-01'),
('Email Campaign', 'Email', 2000.00, 50000, 3000, 150, 15000.00, '2024-06-15'),
('Google Ads', 'Search', 8000.00, 200000, 10000, 500, 50000.00, '2024-07-01');
```

### Insert Customer Data

```sql
INSERT INTO customers (age, gender, country, sessions, avg_session_duration, pages_per_session, transactions, revenue)
VALUES 
(25, 'Female', 'USA', 10, 120.5, 3.5, 2, 150.00),
(35, 'Male', 'UK', 15, 180.0, 5.0, 3, 300.00),
(45, 'Female', 'Canada', 8, 90.0, 2.5, 1, 75.00);
```

## Troubleshooting

### Connection Error

If you get a connection error:

1. Check MySQL is running:
   ```bash
   mysql --version
   sudo service mysql status  # Linux
   brew services list | grep mysql  # macOS
   ```

2. Verify credentials:
   ```bash
   mysql -u root -p
   ```

3. Check firewall/port settings

### Import Errors

If data import fails:

1. Check CSV file exists and has correct columns
2. Verify data types match table schema
3. Check for NULL values in required fields

### Permission Issues

If you get permission errors:

```sql
GRANT ALL PRIVILEGES ON marketing_db.* TO 'your_user'@'localhost';
FLUSH PRIVILEGES;
```

## Data Validation

After setup, verify data is loaded:

```sql
USE marketing_db;

-- Check campaign count
SELECT COUNT(*) FROM campaigns;

-- Check customer count
SELECT COUNT(*) FROM customers;

-- View sample data
SELECT * FROM campaigns LIMIT 5;
SELECT * FROM customers LIMIT 5;
```

## Architecture Changes

### Before (File-based)
```
data/raw/
  ├── marketing_campaign_raw.csv
  └── customer_data_raw.csv
        ↓
  DataLoader reads CSV
        ↓
  Analysis Pipeline
```

### After (Database)
```
MySQL Database
  ├── campaigns table
  └── customers table
        ↓
  DataLoader queries DB via SQLAlchemy
        ↓
  Analysis Pipeline
```

## Benefits

✅ **Centralized Data**: Single source of truth  
✅ **Scalability**: Handle larger datasets efficiently  
✅ **Data Integrity**: Constraints and validation  
✅ **Concurrent Access**: Multiple users/processes  
✅ **Data Security**: Database-level authentication  
✅ **Query Performance**: Indexed columns for faster access  

## Additional Commands

### Backup Database

```bash
mysqldump -u root -p marketing_db > backup.sql
```

### Restore Database

```bash
mysql -u root -p marketing_db < backup.sql
```

### Reset Database

```bash
mysql -u root -p -e "DROP DATABASE IF EXISTS marketing_db;"
python3 setup_database.py
```

## Support

For issues or questions:
1. Check logs in terminal output
2. Verify database configuration
3. Ensure all prerequisites are installed
4. Check MySQL error logs

