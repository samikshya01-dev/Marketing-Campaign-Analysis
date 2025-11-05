#!/bin/bash

# Database Setup Script for Marketing Campaign Analysis

set -e  # Exit on error

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Marketing Campaign Analysis - Database Setup    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo -e "${RED}Error: MySQL is not installed${NC}"
    echo -e "${YELLOW}Please install MySQL first:${NC}"
    echo -e "  macOS: brew install mysql"
    echo -e "  Linux: sudo apt-get install mysql-server"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 found${NC}"
echo -e "${GREEN}✓ MySQL found${NC}"
echo ""

# Check if MySQL is running
if ! pgrep -x mysqld > /dev/null 2>&1 && ! pgrep -x mysql > /dev/null 2>&1; then
    echo -e "${YELLOW}MySQL server is not running. Starting MySQL...${NC}"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew services start mysql 2>/dev/null || echo -e "${YELLOW}Please start MySQL manually${NC}"
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo service mysql start 2>/dev/null || echo -e "${YELLOW}Please start MySQL manually${NC}"
    fi
    sleep 3
fi

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip3 install -q sqlalchemy pymysql pyyaml pandas 2>/dev/null || pip install -q sqlalchemy pymysql pyyaml pandas
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Step 1: Configure database
echo -e "${BLUE}Step 1: Database Configuration${NC}"
echo -e "${YELLOW}Please edit config/database_config.yaml with your MySQL credentials${NC}"
echo -e "Current configuration:"
cat config/database_config.yaml | grep -A 5 "mysql:"
echo ""
read -p "Press Enter to continue after configuring the database, or Ctrl+C to exit..."
echo ""

# Step 2: Create database and tables
echo -e "${BLUE}Step 2: Creating Database and Tables${NC}"
python3 setup_database.py

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}Database setup failed!${NC}"
    echo -e "${YELLOW}Please check:${NC}"
    echo -e "  1. MySQL is running"
    echo -e "  2. Credentials in config/database_config.yaml are correct"
    echo -e "  3. User has permission to create databases"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ Database and tables created successfully!${NC}"
echo ""

# Step 3: Migrate data (optional)
echo -e "${BLUE}Step 3: Data Migration (Optional)${NC}"
echo -e "Do you want to migrate data from CSV files?"
echo -e "  - data/raw/marketing_campaign_raw.csv"
echo -e "  - data/raw/customer_data_raw.csv"
echo ""
read -p "Migrate CSV data? (y/n) [n]: " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 migrate_data.py

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Data migration completed!${NC}"
    else
        echo -e "${YELLOW}⚠ Data migration had issues. You can add data manually.${NC}"
    fi
else
    echo -e "${YELLOW}Skipping data migration. You can run 'python3 migrate_data.py' later.${NC}"
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║            Setup Completed Successfully!           ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo -e "  1. Ensure your database has campaign and customer data"
echo -e "  2. Run the analysis: ${GREEN}./run_analysis.sh${NC}"
echo ""
echo -e "${YELLOW}Useful Commands:${NC}"
echo -e "  • Check data: mysql -u root -p marketing_db -e 'SELECT COUNT(*) FROM campaigns;'"
echo -e "  • Run analysis: ./run_analysis.sh"
echo -e "  • Run with Power BI export: ./run_analysis.sh --export-powerbi"
echo -e "  • View help: ./run_analysis.sh --help"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo -e "  • Database Setup Guide: DATABASE_SETUP.md"
echo -e "  • Project Guide: docs/project_guide.md"
echo ""

