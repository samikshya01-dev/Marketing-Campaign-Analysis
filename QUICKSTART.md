# Quick Start Guide

Get started with the Marketing Campaign Analytics Platform in **5 minutes**.

## 🚀 Quick Setup (3 Steps)

### 1. Configure Database

Edit `config/database_config.yaml` with your MySQL credentials:

```yaml
mysql:
  host: "localhost"
  user: "root"
  password: "YOUR_MYSQL_PASSWORD"  # ← Change this!
  database: "marketing_db"
  port: 3306
```

### 2. Run Database Setup

```bash
./setup_db.sh
```

This automated script will:
- ✅ Check prerequisites (Python, MySQL)
- ✅ Install required packages
- ✅ Create database and tables
- ✅ Optionally migrate CSV data

### 3. Run Analysis

```bash
./run_analysis.sh
```

## 📋 Manual Setup (Alternative)

If you prefer manual control:

### Step 1: Install Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 2: Create Database

```bash
python3 setup_database.py
```

### Step 3: Add Data

**Option A: Migrate from CSV**
```bash
python3 migrate_data.py
```

**Option B: Insert Manually**
```sql
mysql -u root -p marketing_db

INSERT INTO campaigns (campaign_name, channel, cost, impressions, clicks, conversions, revenue, date)
VALUES ('Test Campaign', 'Social Media', 1000.00, 50000, 2500, 100, 5000.00, '2024-01-01');

INSERT INTO customers (age, gender, country, sessions, avg_session_duration, pages_per_session, transactions, revenue)
VALUES (30, 'Female', 'USA', 5, 150.0, 4.0, 1, 100.00);
```

### Step 4: Run Analysis

```bash
./run_analysis.sh
```

## 📊 Verify Setup

Check if data is loaded:

```bash
mysql -u root -p marketing_db -e "
SELECT 'Campaigns' as Table_Name, COUNT(*) as Count FROM campaigns
UNION ALL
SELECT 'Customers', COUNT(*) FROM customers;
"
```

Expected output:
```
+------------+-------+
| Table_Name | Count |
+------------+-------+
| Campaigns  |   XXX |
| Customers  |   XXX |
+------------+-------+
```

## 🎯 Running Analysis

### Basic Run
```bash
./run_analysis.sh
```

### With Power BI Export
```bash
./run_analysis.sh --export-powerbi
```

### Skip Non-Critical Errors
```bash
./run_analysis.sh --skip-errors
```

### Custom Configuration
```bash
./run_analysis.sh --config config/custom_config.yaml
```

### Show Help
```bash
./run_analysis.sh --help
```

## 📁 Output Files

After running the analysis, find results in:

```
outputs/
├── visualizations/
│   ├── channel_metrics.png
│   ├── roi_by_channel.png
│   ├── customer_segments.png
│   └── ... (more charts)
├── reports/
│   ├── executive_summary.html
│   └── campaign_insights_summary.csv
└── dashboards/
    ├── marketing_dashboard.pbix
    └── dashboards/
        ├── campaign_data_powerbi.csv
        ├── customer_segments_powerbi.csv
        └── ... (Power BI files)
```

## 🔧 Troubleshooting

### MySQL Not Running

**macOS:**
```bash
brew services start mysql
```

**Linux:**
```bash
sudo service mysql start
```

### Connection Error

Check credentials:
```bash
mysql -u root -p
```

If successful, update `config/database_config.yaml` with the same password.

### Permission Denied

Grant permissions:
```sql
GRANT ALL PRIVILEGES ON marketing_db.* TO 'your_user'@'localhost';
FLUSH PRIVILEGES;
```

### No Data Found

Check if tables are populated:
```bash
mysql -u root -p marketing_db -e "SELECT COUNT(*) FROM campaigns; SELECT COUNT(*) FROM customers;"
```

If empty, add data using:
```bash
python3 migrate_data.py
```

Or insert manually via SQL.

## 📚 Key Changes from CSV Version

| Aspect | Old (CSV) | New (Database) |
|--------|-----------|----------------|
| Data Source | `data/raw/*.csv` | MySQL tables |
| Data Access | `pd.read_csv()` | `pd.read_sql()` |
| Scalability | Limited | High |
| Concurrent Access | No | Yes |
| Data Integrity | Basic | Enforced |
| Query Speed | Slow for large files | Fast with indexes |

## 🔄 Workflow

```
┌─────────────────────┐
│  MySQL Database     │
│  - campaigns        │
│  - customers        │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  DataLoader         │
│  (SQLAlchemy)       │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  Data Cleaning      │
│  (DataCleaner)      │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  Analysis           │
│  - EDA              │
│  - Segmentation     │
│  - ROI Calculation  │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  Outputs            │
│  - Visualizations   │
│  - Reports          │
│  - Dashboards       │
└─────────────────────┘
```

## 💡 Tips

1. **Backup regularly**: Use `mysqldump` to backup your data
2. **Index frequently queried columns**: Already done in setup
3. **Monitor performance**: Check MySQL slow query log
4. **Use transactions**: For bulk inserts
5. **Keep credentials secure**: Never commit `database_config.yaml` with real passwords

## 📖 Additional Resources

- [DATABASE_SETUP.md](DATABASE_SETUP.md) - Detailed setup guide
- [docs/project_guide.md](docs/project_guide.md) - Full project documentation
- [docs/technical_documentation.md](docs/technical_documentation.md) - Technical details

## 🆘 Need Help?

1. Check logs in terminal output
2. Review `DATABASE_SETUP.md` for detailed troubleshooting
3. Verify MySQL is running and accessible
4. Ensure all dependencies are installed
5. Check database credentials in `config/database_config.yaml`

## ✅ Success Checklist

- [ ] MySQL installed and running
- [ ] Database configuration updated
- [ ] Database and tables created
- [ ] Data populated (campaigns and customers)
- [ ] Analysis runs without errors
- [ ] Output files generated
- [ ] Visualizations created
- [ ] Reports accessible

**Ready to analyze! 🎉**

