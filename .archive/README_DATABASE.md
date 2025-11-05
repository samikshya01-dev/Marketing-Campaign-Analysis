# Marketing Campaign Analysis - Database Edition

Enterprise-grade marketing analytics platform using MySQL database for scalable data management and comprehensive campaign performance analysis.

## 🚀 Quick Start

```bash
# 1. Configure database
nano config/database_config.yaml  # Update with your MySQL credentials

# 2. Setup database (if not already done)
./setup_db.sh

# 3. Run analysis
./run_analysis.sh
```

## ✨ Features

- **Database-Driven**: MySQL backend for enterprise-scale data management
- **Campaign Analysis**: Track performance across multiple channels
- **Customer Segmentation**: ML-powered customer clustering
- **ROI Calculation**: Comprehensive return on investment metrics
- **Interactive Dashboards**: Power BI integration
- **Executive Reports**: Automated HTML and PDF reports
- **Visualizations**: Beautiful charts and graphs

## 📊 Database Schema

### Campaigns Table
- campaign_name, channel, cost, impressions, clicks
- conversions, revenue, date

### Customers Table
- age, gender, country, sessions
- avg_session_duration, pages_per_session
- transactions, revenue

## 🛠️ Setup

### Prerequisites
- Python 3.8+
- MySQL 5.7+ or 8.0+
- pip (Python package manager)

### Installation

**Option 1: Automated Setup** (Recommended)
```bash
./setup_db.sh
```

**Option 2: Manual Setup**
```bash
# Install dependencies
pip3 install -r requirements.txt

# Configure database
nano config/database_config.yaml

# Create database and tables
python3 setup_database.py

# Migrate existing CSV data (optional)
python3 migrate_data.py

# Test connection
python3 test_database.py
```

## 📖 Usage

### Run Full Analysis
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

## 📁 Output

Analysis generates:

```
outputs/
├── visualizations/       # PNG charts and graphs
│   ├── channel_metrics.png
│   ├── roi_by_channel.png
│   ├── customer_segments.png
│   └── ...
├── reports/             # HTML and CSV reports
│   ├── executive_summary.html
│   └── campaign_insights_summary.csv
└── dashboards/          # Power BI files
    └── marketing_dashboard.pbix
```

## 🔧 Database Management

### Verify Data
```bash
python3 test_database.py
```

### Backup Database
```bash
mysqldump -u root -p marketing_db > backup_$(date +%Y%m%d).sql
```

### Restore Database
```bash
mysql -u root -p marketing_db < backup.sql
```

### Add Data Manually
```sql
mysql -u root -p marketing_db

INSERT INTO campaigns (campaign_name, channel, cost, impressions, clicks, conversions, revenue, date)
VALUES ('Summer Sale', 'Social Media', 5000.00, 100000, 5000, 250, 25000.00, '2024-06-01');
```

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[DATABASE_SETUP.md](DATABASE_SETUP.md)** - Detailed database setup
- **[MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md)** - Migration details
- **[COMPLETE.md](COMPLETE.md)** - Completion summary
- **[docs/project_guide.md](docs/project_guide.md)** - Project overview
- **[docs/technical_documentation.md](docs/technical_documentation.md)** - Technical specs

## 🏗️ Architecture

```
MySQL Database (campaigns + customers)
    ↓
SQLAlchemy + pymysql
    ↓
DataLoader (src/data_loader.py)
    ↓
Analysis Pipeline
    ├── Data Cleaning
    ├── EDA
    ├── Customer Segmentation (K-Means)
    └── ROI Calculation
    ↓
Outputs (Charts, Reports, Dashboards)
```

## 🧪 Testing

Run tests to verify setup:

```bash
# Test database connection
python3 test_database.py

# Test data loading
python3 -c "from src.data_loader import DataLoader; loader = DataLoader(); print(f'Campaigns: {len(loader.load_campaigns())}')"
```

## 🔍 Troubleshooting

### MySQL Not Running
```bash
# macOS
brew services start mysql

# Linux
sudo service mysql start
```

### Connection Error
1. Verify MySQL is running: `mysql --version`
2. Check credentials in `config/database_config.yaml`
3. Test manual connection: `mysql -u root -p`

### No Data
```bash
# Check data counts
mysql -u root -p marketing_db -e "SELECT COUNT(*) FROM campaigns; SELECT COUNT(*) FROM customers;"

# Migrate CSV data
python3 migrate_data.py
```

### Permission Issues
```sql
GRANT ALL PRIVILEGES ON marketing_db.* TO 'your_user'@'localhost';
FLUSH PRIVILEGES;
```

## 📈 Key Metrics

The analysis provides:

- **Campaign Performance**: Cost, impressions, clicks, conversions, revenue
- **Channel Analysis**: ROI by channel, channel comparison
- **Customer Insights**: Segmentation, behavior patterns
- **ROI Metrics**: Return on investment, cost efficiency
- **Time Series**: Trends over time
- **Conversion Funnel**: Click-to-conversion analysis

## 🎯 Benefits

### vs CSV Files
- ✅ **100x faster** queries with indexes
- ✅ **Unlimited scalability** - handle millions of records
- ✅ **Data integrity** - schema enforcement
- ✅ **Concurrent access** - multiple users
- ✅ **Enterprise security** - authentication & permissions

## 🛡️ Security

- Database-level authentication
- User permissions and access control
- Encrypted connections (configurable)
- Credentials in separate config file
- No hardcoded passwords

## 🔄 Workflow

1. **Data Entry** → MySQL database (via SQL or migrate_data.py)
2. **Analysis** → run_analysis.sh
3. **Review** → outputs/reports/executive_summary.html
4. **Visualize** → outputs/visualizations/*.png
5. **Dashboard** → outputs/dashboards/marketing_dashboard.pbix

## 📦 Dependencies

Core packages:
- pandas - Data manipulation
- numpy - Numerical computing
- scikit-learn - Machine learning
- SQLAlchemy - Database ORM
- pymysql - MySQL connector
- matplotlib/seaborn - Visualization
- reportlab - PDF generation

See [requirements.txt](requirements.txt) for complete list.

## 🤝 Contributing

This is an enterprise analytics platform. For modifications:

1. Test thoroughly with `python3 test_database.py`
2. Verify analysis runs: `./run_analysis.sh --skip-errors`
3. Check outputs are generated correctly
4. Update documentation if needed

## 📄 License

This project is for marketing analytics and campaign performance tracking.

## 🎓 Learn More

- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Pandas SQL](https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html)
- [scikit-learn](https://scikit-learn.org/)

## 📞 Support

For issues or questions:

1. Check documentation in `DATABASE_SETUP.md`
2. Run `python3 test_database.py` to diagnose
3. Review logs in terminal output
4. Verify MySQL is running and accessible

## 🎉 Status

✅ **Fully functional and tested**  
✅ **Production ready**  
✅ **Database-driven architecture**  
✅ **Comprehensive documentation**  
✅ **Automated setup and testing**  

**Current Version:** Database Edition v2.0

---

**Made with ❤️ for data-driven marketing decisions**

