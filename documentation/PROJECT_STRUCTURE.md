# 📁 Project Structure & File Organization

## Complete Project Architecture

```
marketing-campaign-analysis/
│
├── 📄 README.md                          # Main project documentation
├── 📄 QUICKSTART.md                      # 5-minute setup guide
├── 📄 requirements.txt                   # Python dependencies
├── 🔧 run_analysis.sh                    # Main execution script
├── ⚙️ .gitignore                         # Git ignore patterns
│
├── 📂 src/                               # Source code (Core Application)
│   ├── __init__.py
│   ├── main.py                           # Entry point & orchestration
│   ├── data_loader.py                    # Database connector (Repository pattern)
│   ├── data_cleaner.py                   # Data validation & preprocessing
│   ├── eda_analysis.py                   # Exploratory data analysis
│   ├── customer_segmentation.py          # ML-based customer clustering
│   ├── roi_calculator.py                 # ROI & financial metrics
│   ├── powerbi_exporter.py               # Power BI integration
│   └── generate_executive_summary.py     # Report generation (PDF/HTML)
│
├── 📂 scripts/                           # Utility scripts
│   ├── database/                         # Database management
│   │   ├── setup_database.py            # Create database & tables
│   │   ├── migrate_data.py              # CSV to database migration
│   │   ├── test_database.py             # Connection verification
│   │   └── setup_db.sh                  # Interactive setup automation
│   │
│   └── utilities/                        # Helper scripts (future)
│
├── 📂 config/                            # Configuration files
│   ├── config.yaml                       # Application configuration
│   └── database_config.yaml              # Database credentials
│
├── 📂 data/                              # Data directory
│   ├── raw/                              # Raw data (optional, for migration)
│   └── processed/                        # Processed outputs
│       ├── clean_campaign_data.csv
│       ├── clean_customer_data.csv
│       ├── customer_segments.csv
│       ├── roi_analysis.csv
│       └── channel_performance_summary.csv
│
├── 📂 outputs/                           # Generated outputs
│   ├── visualizations/                   # Charts & graphs (PNG)
│   │   ├── channel_metrics.png
│   │   ├── roi_by_channel.png
│   │   ├── customer_segments.png
│   │   ├── conversion_funnel.png
│   │   ├── cost_vs_revenue.png
│   │   ├── roi_distribution.png
│   │   ├── segment_profiles.png
│   │   └── time_series.png
│   │
│   ├── reports/                          # PDF & HTML reports
│   │   ├── executive_summary.pdf         # Automated PDF report (4.3 KB, 2 pages)
│   │   ├── executive_summary.html        # Interactive HTML report (9.7 KB)
│   │   └── campaign_insights_summary.csv
│   │
│   └── dashboards/                       # Power BI files
│       ├── marketing_dashboard.pbix
│       ├── powerbi_measures.dax
│       ├── POWERBI_README.md
│       └── dashboards/
│           ├── campaign_data_powerbi.csv
│           ├── channel_performance_powerbi.csv
│           ├── customer_segments_powerbi.csv
│           ├── roi_analysis_powerbi.csv
│           └── powerbi_metadata.json
│
├── 📂 tests/                             # Unit tests
│   ├── __init__.py
│   ├── test_data_loader.py              # DataLoader tests
│   └── test_data_cleaner.py             # DataCleaner tests
│
├── 📂 documentation/                     # Comprehensive documentation
│   │
│   ├── architecture/                     # System design documents
│   │   ├── SYSTEM_DESIGN.md             # Architecture & design patterns
│   │   ├── DATABASE_SCHEMA.md            # Database design (future)
│   │   └── DATA_PIPELINE.md             # ETL pipeline documentation
│   │
│   ├── api/                              # API documentation
│   │   └── API_DOCUMENTATION.md          # Module interfaces (future)
│   │
│   ├── guides/                           # User & developer guides
│   │   ├── USER_GUIDE.md                 # Complete usage guide (future)
│   │   ├── CONFIGURATION.md              # Setup & config guide (future)
│   │   ├── DEVELOPMENT.md                # Contributing guidelines (future)
│   │   └── CONTRIBUTING.md               # Contribution guide (future)
│   │
│   ├── TECH_STACK.md                     # Technology choices & rationale
│   └── INTERVIEW_PREPARATION.md          # Interview Q&A guide
│
├── 📂 docs/                              # Legacy documentation (reference)
│   ├── data_dictionary.md
│   ├── project_guide.md
│   └── technical_documentation.md
│
├── 📂 .archive/                          # Archived files (not in use)
│   ├── COMPLETE.md
│   ├── MIGRATION_SUMMARY.md
│   ├── PDF_FIX_SUMMARY.md
│   ├── REPORTLAB_FIX.md
│   ├── DATABASE_SETUP.md
│   ├── test_pdf_generation.py
│   └── test_pdf_gen.py
│
├── 📂 venv/                              # Python virtual environment (ignored)
└── 📂 .idea/                             # IDE configuration (ignored)
```

---

## 📊 File Count Summary

| Category | Count | Size | Purpose |
|----------|-------|------|---------|
| **Source Code** | 9 files | ~5 KB each | Core application logic |
| **Scripts** | 4 files | ~6 KB each | Database & utility scripts |
| **Configuration** | 2 files | ~1 KB each | App & DB config |
| **Documentation** | 6 files | ~50 KB total | Architecture, guides, interviews |
| **Tests** | 2 files | ~2 KB each | Unit tests |
| **Outputs** | ~15 files | ~20 MB total | Reports, charts, dashboards |
| **Total (Active)** | **~40 files** | **~25 MB** | Production files |

---

## 🎯 Key Files Explained

### Core Application Files

#### `src/main.py` (Entry Point)
**Purpose**: Orchestrates the entire analysis pipeline  
**Key Functions**:
- `main(args)` - Main execution flow
- `setup_logging()` - Configure logging
- `load_config()` - Load YAML configuration
- `create_directories()` - Ensure output dirs exist

**Execution Flow**:
1. Setup & configuration loading
2. Initialize all components
3. Load data from database
4. Clean and validate data
5. Run analysis (EDA, Segmentation, ROI)
6. Generate reports (PDF, HTML, Power BI)

---

#### `src/data_loader.py` (Database Layer)
**Purpose**: Repository pattern for database access  
**Pattern**: Repository Pattern  
**Key Methods**:
- `load_campaigns()` - Query campaigns table
- `load_customers()` - Query customers table
- `save_to_csv()` - Export DataFrames
- `close()` - Cleanup connections

**Features**:
- SQLAlchemy ORM for abstraction
- Connection pooling (10 connections)
- Context manager support
- Type hints for safety

---

#### `src/data_cleaner.py` (Data Quality)
**Purpose**: Data validation and preprocessing  
**Key Methods**:
- `clean_campaign_data()` - Clean campaigns
- `clean_customer_data()` - Clean customers
- `_handle_missing_values()` - Imputation strategies
- `_remove_duplicates()` - Deduplication
- `_validate_data_types()` - Type checking

**Validation Rules**:
- Required fields must exist
- Numeric fields >= 0
- Clicks <= Impressions
- Revenue >= Cost (business rule)

---

#### `src/customer_segmentation.py` (ML Engine)
**Purpose**: ML-based customer clustering  
**Algorithm**: K-Means clustering  
**Key Methods**:
- `segment_customers()` - Apply clustering
- `plot_segments()` - Visualize clusters
- `get_segment_profiles()` - Analyze clusters
- `_preprocess_features()` - Feature scaling

**Features Used**:
- Age, sessions, duration, pages, transactions, revenue
- StandardScaler for normalization
- Elbow method for optimal K
- Silhouette score for validation

---

#### `src/roi_calculator.py` (Financial Metrics)
**Purpose**: Calculate ROI and financial KPIs  
**Key Methods**:
- `calculate_campaign_roi()` - Campaign-level metrics
- `plot_roi_analysis()` - ROI visualizations
- `generate_roi_report()` - Summary statistics
- `export_summary()` - CSV export

**Metrics Calculated**:
- ROI, ROAS, Profit
- CTR, Conversion Rate
- CPC, CPA, Conversion Value

---

#### `src/eda_analysis.py` (Analytics)
**Purpose**: Exploratory data analysis and visualization  
**Key Methods**:
- `plot_campaign_performance()` - Channel charts
- `generate_eda_report()` - Summary statistics
- `_create_time_series_plots()` - Trends
- `_create_distribution_plots()` - Distributions

**Visualizations**:
- Time series: Revenue, cost trends
- Bar charts: Channel comparisons
- Scatter plots: Cost vs revenue
- Histograms: ROI distributions

---

#### `src/generate_executive_summary.py` (Reporting)
**Purpose**: Automated report generation  
**Key Methods**:
- `generate_pdf()` - Create PDF report
- `generate_html_report()` - Create HTML report
- `_create_metrics_table()` - Key metrics
- `_create_channel_performance_table()` - Channel data

**Features**:
- Professional PDF with ReportLab
- Interactive HTML with styling
- Indian Rupees (Rs.) formatting
- Multi-page layout

---

#### `src/powerbi_exporter.py` (BI Integration)
**Purpose**: Export data for Power BI  
**Key Methods**:
- `export_all()` - Export all datasets
- `_export_campaigns()` - Campaign data
- `_export_customers()` - Customer segments
- `_create_metadata()` - Export metadata

**Exports**:
- campaign_data_powerbi.csv
- channel_performance_powerbi.csv
- customer_segments_powerbi.csv
- roi_analysis_powerbi.csv
- powerbi_metadata.json

---

### Script Files

#### `scripts/database/setup_database.py`
**Purpose**: Create database and tables  
**Features**:
- Automatic database creation
- Table schema with indexes
- Verification and validation
- Error handling with helpful messages

---

#### `scripts/database/migrate_data.py`
**Purpose**: Migrate CSV data to database  
**Features**:
- Reads data/raw/*.csv files
- Validates column names
- Batch inserts for performance
- Shows sample data after migration

---

#### `scripts/database/test_database.py`
**Purpose**: Verify database connection  
**Features**:
- Tests connection to MySQL
- Loads sample data
- Shows statistics
- Verifies data integrity

---

#### `scripts/database/setup_db.sh`
**Purpose**: Interactive setup automation  
**Features**:
- Checks prerequisites (Python, MySQL)
- Installs dependencies
- Runs setup_database.py
- Optionally runs migrate_data.py
- Provides next steps

---

### Configuration Files

#### `config/config.yaml`
**Purpose**: Application configuration  
**Contents**:
```yaml
paths:
  raw_data: "data/raw"
  processed_data: "data/processed"
  visualizations: "outputs/visualizations"
  reports: "outputs/reports"
  dashboards: "outputs/dashboards"

analysis:
  segmentation:
    n_clusters: 3
    algorithm: "kmeans"
  
  visualization:
    dpi: 300
    figsize: [12, 8]
```

---

#### `config/database_config.yaml`
**Purpose**: Database credentials  
**Contents**:
```yaml
mysql:
  host: "localhost"
  user: "root"
  password: "your_password"
  database: "marketing_db"
  port: 3306

connection_string: "mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
```

**Security**: Never commit with real passwords!

---

### Documentation Files

#### `README.md` (Main Documentation)
**Purpose**: Project overview and quick reference  
**Sections**:
- Overview & features
- Architecture diagram
- Tech stack
- Quick start guide
- Project structure
- Usage examples

---

#### `QUICKSTART.md`
**Purpose**: 5-minute setup guide  
**Sections**:
- Prerequisites
- Installation steps
- Running analysis
- Troubleshooting

---

#### `documentation/TECH_STACK.md`
**Purpose**: Technology choices and rationale  
**Sections**:
- Core technologies
- Database layer
- Data processing
- ML layer
- Visualization
- Reporting
- Performance benchmarks

---

#### `documentation/INTERVIEW_PREPARATION.md`
**Purpose**: Interview Q&A preparation  
**Sections**:
- Project overview questions
- Technical architecture
- Database design
- Data processing
- Machine learning
- Performance optimization
- Challenges & solutions
- Behavioral questions
- Code walkthrough
- Metrics & impact

---

#### `documentation/architecture/SYSTEM_DESIGN.md`
**Purpose**: System architecture and design patterns  
**Sections**:
- High-level architecture
- Design patterns used
- Data flow architecture
- Database architecture
- Module architecture
- Security considerations
- Scalability strategies

---

#### `documentation/architecture/DATA_PIPELINE.md`
**Purpose**: ETL pipeline documentation  
**Sections**:
- Pipeline overview
- Extraction phase
- Transformation phase
- Analysis phase
- Report generation
- Monitoring & metrics

---

## 🎨 Code Organization Principles

### 1. **Separation of Concerns**
- **Data Layer**: `data_loader.py` handles all database operations
- **Business Logic**: `roi_calculator.py`, `customer_segmentation.py`
- **Presentation**: `generate_executive_summary.py`, `powerbi_exporter.py`

### 2. **Single Responsibility**
Each module has one clear purpose:
- `DataLoader` → Database access
- `DataCleaner` → Data quality
- `EDAAnalyzer` → Visualization
- `CustomerSegmentation` → ML clustering
- `ROICalculator` → Financial metrics

### 3. **Dependency Injection**
```python
# All components receive config_path
loader = DataLoader(config_path="config/config.yaml")
cleaner = DataCleaner(config_path="config/config.yaml")
```

### 4. **Naming Conventions**
- **Classes**: PascalCase (`DataLoader`, `ROICalculator`)
- **Functions**: snake_case (`load_campaigns`, `calculate_roi`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_CONNECTIONS`, `DEFAULT_CLUSTERS`)
- **Private Methods**: _leading_underscore (`_validate_data`, `_create_engine`)

### 5. **Project Structure Patterns**
```
src/           # Application code
scripts/       # Operational scripts
config/        # Configuration
data/          # Data files
outputs/       # Generated files
tests/         # Unit tests
documentation/ # Docs
```

---

## 🔄 Data Flow Through Files

```
1. run_analysis.sh
   └─> src/main.py (entry point)
       │
       ├─> config/config.yaml (load config)
       ├─> config/database_config.yaml (DB config)
       │
       ├─> src/data_loader.py
       │   └─> MySQL Database → campaigns, customers
       │
       ├─> src/data_cleaner.py
       │   └─> data/processed/*.csv
       │
       ├─> src/eda_analysis.py
       │   └─> outputs/visualizations/*.png
       │
       ├─> src/customer_segmentation.py
       │   └─> data/processed/customer_segments.csv
       │
       ├─> src/roi_calculator.py
       │   └─> data/processed/roi_analysis.csv
       │
       ├─> src/generate_executive_summary.py
       │   ├─> outputs/reports/executive_summary.pdf
       │   └─> outputs/reports/executive_summary.html
       │
       └─> src/powerbi_exporter.py
           └─> outputs/dashboards/*.csv
```

---

## 📦 Dependency Tree

```
Application (main.py)
├── Data Layer
│   ├── SQLAlchemy → pymysql → MySQL
│   └── Pandas → NumPy
│
├── Processing Layer
│   ├── Pandas (data manipulation)
│   └── NumPy (numerical computing)
│
├── ML Layer
│   └── Scikit-learn → NumPy
│
├── Visualization Layer
│   ├── Matplotlib
│   ├── Seaborn → Matplotlib
│   └── Plotly
│
├── Reporting Layer
│   └── ReportLab
│
└── Configuration Layer
    └── PyYAML
```

---

## 🚀 Execution Flow

### Standard Run
```bash
./run_analysis.sh
```

**What Happens**:
1. Activates virtual environment
2. Installs/updates dependencies
3. Runs `python3 src/main.py`
4. Generates all outputs
5. Displays completion message

### With Power BI Export
```bash
./run_analysis.sh --export-powerbi
```

**Additional Step**:
- Exports CSV files to `outputs/dashboards/`

### Custom Config
```bash
./run_analysis.sh --config config/custom_config.yaml
```

**Different Configuration**:
- Uses custom paths
- Different analysis parameters

---

## 📊 Output Files Explained

### Visualizations (PNG, 300 DPI)
- `channel_metrics.png` - Performance by channel
- `roi_by_channel.png` - ROI comparison
- `customer_segments.png` - Cluster visualization
- `conversion_funnel.png` - Click → Conversion funnel
- `cost_vs_revenue.png` - Cost/revenue scatter
- `roi_distribution.png` - ROI histogram
- `segment_profiles.png` - Cluster profiles
- `time_series.png` - Trends over time

### Reports
- `executive_summary.pdf` - Professional PDF report (4.3 KB, 2 pages)
- `executive_summary.html` - Interactive HTML (9.7 KB)
- `campaign_insights_summary.csv` - Key metrics CSV

### Dashboards
- `marketing_dashboard.pbix` - Power BI dashboard
- `campaign_data_powerbi.csv` - Raw campaign data
- `channel_performance_powerbi.csv` - Channel aggregations
- `customer_segments_powerbi.csv` - Customer clusters
- `roi_analysis_powerbi.csv` - ROI metrics
- `powerbi_metadata.json` - Export metadata

---

## 🎓 Best Practices Implemented

### Code Quality
✅ Type hints for function signatures  
✅ Docstrings for all classes and methods  
✅ Consistent naming conventions  
✅ Error handling with try-except  
✅ Logging at appropriate levels  

### Project Organization
✅ Clear directory structure  
✅ Separation of concerns  
✅ Configuration-driven  
✅ Modular design  
✅ Comprehensive documentation  

### Data Engineering
✅ ETL pipeline with clear stages  
✅ Data validation at every step  
✅ Proper error handling  
✅ Performance optimization  
✅ Scalability considerations  

---

**Document Version**: 1.0  
**Last Updated**: November 4, 2025  
**Maintained By**: Architecture Team

