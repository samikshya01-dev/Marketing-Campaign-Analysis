# Technical Documentation

## System Architecture

### Data Flow
1. Data Extraction (GA4 → MySQL)
2. Data Processing (Python)
3. Analysis & Modeling
4. Visualization (Power BI)

### Components

#### 1. Data Loader (`src/data_loader.py`)
- Manages database connections using SQLAlchemy
- Handles data extraction and storage
- Supports both CSV and direct database operations

```python
from data_loader import DataLoader
loader = DataLoader()
campaigns_df = loader.load_campaigns()
```

#### 2. Data Cleaner (`src/data_cleaner.py`)
- Preprocesses raw data
- Handles missing values and outliers
- Standardizes formats

Key functions:
```python
def clean_campaign_data(df):
    # Handles campaign data cleaning
    pass

def clean_customer_data(df):
    # Handles customer data cleaning
    pass
```

#### 3. Customer Segmentation (`src/customer_segmentation.py`)
- Implements K-means clustering
- Features:
  - sessions
  - pages_per_session
  - transactions
  - revenue
- Outputs customer segments

#### 4. ROI Calculator (`src/roi_calculator.py`)
- Calculates campaign performance metrics
- Generates ROI reports
- Produces visualization data

## Database Schema

### campaigns
```sql
CREATE TABLE campaigns (
    campaign_id INT PRIMARY KEY AUTO_INCREMENT,
    campaign_name VARCHAR(100),
    channel VARCHAR(50),
    cost DECIMAL(10,2),
    impressions INT,
    clicks INT,
    conversions INT,
    revenue DECIMAL(10,2),
    date DATE
);
```

### customers
```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    age INT,
    gender VARCHAR(10),
    country VARCHAR(50),
    sessions INT,
    avg_session_duration DECIMAL(10,2),
    pages_per_session DECIMAL(10,2),
    transactions INT,
    revenue DECIMAL(10,2)
);
```

## Configuration

### Database Config (`config/database_config.yaml`)
```yaml
mysql:
  host: localhost
  user: root
  password: yourpassword
  database: marketing_db
```

### Analysis Config (`config/config.yaml`)
```yaml
paths:
  raw_data: data/raw/
  processed_data: data/processed/
  outputs: outputs/

model:
  clustering:
    n_clusters: 3
    random_state: 42
```

## Dependencies
- Python 3.8+
- MySQL 8.0+
- Required packages in requirements.txt

## Data Processing Pipeline

### 1. Data Extraction
```python
# Load campaign data
campaigns_df = loader.load_campaigns()

# Load customer data
customers_df = loader.load_customers()
```

### 2. Data Cleaning
```python
# Clean campaign data
clean_campaigns = cleaner.clean_campaign_data(campaigns_df)

# Clean customer data
clean_customers = cleaner.clean_customer_data(customers_df)
```

### 3. Customer Segmentation
```python
# Perform clustering
segmentation = CustomerSegmentation()
segmented_df = segmentation.segment_customers(clean_customers)
```

### 4. ROI Analysis
```python
# Calculate ROI metrics
calculator = ROICalculator()
roi_df = calculator.calculate_campaign_roi(clean_campaigns)
```

## Error Handling

### Database Errors
```python
try:
    df = loader.load_campaigns()
except SQLAlchemyError as e:
    logging.error(f"Database error: {e}")
```

### Data Validation
```python
def validate_data(df):
    assert all(df['revenue'] >= 0), "Negative revenue found"
    assert all(df['clicks'] <= df['impressions']), "Clicks > Impressions"
```

## Testing

### Unit Tests
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_data_cleaner.py
```

### Test Coverage
```bash
pytest --cov=src tests/
```

## Performance Optimization

### Database
- Indexed columns: campaign_id, date, channel
- Partitioned tables by date
- Optimized queries in SQL files

### Python
- Vectorized operations with pandas
- Efficient memory usage with generators
- Parallel processing where applicable

## Monitoring & Logging

### Logging Configuration
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Key Metrics
- Data processing time
- Memory usage
- Error rates
- Query performance

## Deployment

### Requirements
- Python 3.8+
- MySQL 8.0+
- 8GB RAM minimum
- 50GB storage

### Installation Steps
1. Clone repository
2. Install dependencies
3. Configure database
4. Run setup scripts
5. Verify installation

## Maintenance

### Regular Tasks
- Database backups
- Log rotation
- Cache clearing
- Performance monitoring

### Troubleshooting
- Check logs in app.log
- Verify database connectivity
- Validate input data
- Monitor system resources
