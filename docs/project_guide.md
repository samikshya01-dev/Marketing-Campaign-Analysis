# Project Guide

## Introduction
This guide provides step-by-step instructions for setting up, running, and maintaining the Marketing Campaign Analysis project. It covers data extraction from Google Analytics 4, data processing with Python, and visualization with Power BI.

## Table of Contents
1. [Project Setup](#project-setup)
2. [Data Collection](#data-collection)
3. [Analysis Pipeline](#analysis-pipeline)
4. [Visualization](#visualization)
5. [Maintenance](#maintenance)

## Project Setup

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher
- Power BI Desktop
- Git

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/marketing-campaign-analysis.git
cd marketing-campaign-analysis
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure database:
- Copy config/database_config.yaml.example to config/database_config.yaml
- Update database credentials

### Directory Structure
```
marketing-campaign-analysis/
├── data/               # Data files
├── sql/               # SQL queries
├── src/               # Python source code
├── notebooks/         # Jupyter notebooks
├── outputs/           # Generated outputs
├── tests/             # Unit tests
└── docs/              # Documentation
```

## Data Collection

### Google Analytics Setup

1. Access GA4 Property:
   - Open Google Analytics
   - Select your property
   - Navigate to Admin → Export → BigQuery Export

2. Export Data:
   - Choose date range
   - Select metrics
   - Export as CSV

### Database Setup

1. Create database:
```sql
CREATE DATABASE marketing_db;
```

2. Run initialization scripts:
```bash
mysql -u root -p marketing_db < sql/01_data_extraction.sql
mysql -u root -p marketing_db < sql/02_data_cleaning.sql
```

## Analysis Pipeline

### 1. Data Loading

Load data using data_loader.py:
```python
from src.data_loader import DataLoader

loader = DataLoader()
campaigns_df = loader.load_campaigns()
customers_df = loader.load_customers()
```

### 2. Data Cleaning

Clean and preprocess data:
```python
from src.data_cleaner import DataCleaner

cleaner = DataCleaner()
clean_campaigns = cleaner.clean_campaign_data(campaigns_df)
clean_customers = cleaner.clean_customer_data(customers_df)
```

### 3. Customer Segmentation

Perform customer segmentation:
```python
from src.customer_segmentation import CustomerSegmentation

segmentation = CustomerSegmentation()
segmented_df = segmentation.segment_customers(clean_customers)
```

### 4. ROI Analysis

Calculate ROI metrics:
```python
from src.roi_calculator import ROICalculator

calculator = ROICalculator()
roi_df = calculator.calculate_campaign_roi(clean_campaigns)
```

## Visualization

### Power BI Dashboard

1. Open marketing_dashboard.pbix
2. Connect to database:
   - Get Data → MySQL
   - Enter server details
   - Select required tables

3. Refresh data:
   - Home → Refresh
   - Set up scheduled refresh

### Dashboard Pages

1. Overview
   - KPI cards
   - Revenue trends
   - Channel performance

2. Campaign Analysis
   - Campaign ROI
   - Conversion funnel
   - Cost analysis

3. Customer Segments
   - Segment distribution
   - Behavioral patterns
   - Revenue contribution

4. Geographic Analysis
   - Country performance
   - Regional trends
   - Market penetration

## Maintenance

### Regular Tasks

1. Data Updates
```bash
# Update data
python src/main.py --refresh-data

# Verify data quality
python src/main.py --validate-data
```

2. Database Maintenance
```sql
-- Optimize tables
OPTIMIZE TABLE campaigns;
OPTIMIZE TABLE customers;

-- Update statistics
ANALYZE TABLE campaigns;
ANALYZE TABLE customers;
```

3. Backup
```bash
# Backup database
mysqldump -u root -p marketing_db > backup.sql

# Backup configuration
cp config/*.yaml config/backup/
```

### Troubleshooting

1. Data Issues
- Check logs in app.log
- Verify data quality metrics
- Run validation queries

2. Performance Issues
- Monitor query execution time
- Check system resources
- Optimize slow queries

3. Dashboard Issues
- Refresh data connections
- Clear cache
- Check for filter conflicts

## Best Practices

### Code Style
- Follow PEP 8
- Use type hints
- Document functions
- Write unit tests

### Data Quality
- Validate inputs
- Handle missing values
- Remove duplicates
- Check for outliers

### Analysis
- Document assumptions
- Validate results
- Use version control
- Keep audit trail

## Support

### Getting Help
- Check documentation
- Review common issues
- Contact support team

### Contributing
- Fork repository
- Create feature branch
- Submit pull request
- Update documentation

## References
- [Google Analytics API Documentation](https://developers.google.com/analytics)
- [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)
- [Power BI Documentation](https://docs.microsoft.com/en-us/power-bi/)
