#!/bin/bash

# Marketing Campaign Analysis Pipeline Runner
# This script orchestrates the complete data analytics pipeline
# Pipeline Flow: Setup → Extract → Transform → Analyze → Report

set -e  # Exit on error

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Marketing Campaign Analytics Pipeline v2.0      ║${NC}"
echo -e "${BLUE}║   Enterprise Data Analytics Platform              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo ""

# ============================================================================
# STAGE 0: ENVIRONMENT SETUP
# ============================================================================
echo -e "${CYAN}[STAGE 0/5] Environment Setup${NC}"
echo ""

# Check if Python is installed
echo -e "${YELLOW}→ Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Error: Python 3 is not installed${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ ${PYTHON_VERSION} found${NC}"

# Check if virtual environment exists
echo -e "${YELLOW}→ Checking virtual environment...${NC}"
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}  Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}→ Activating virtual environment...${NC}"
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo -e "${GREEN}✓ Virtual environment activated${NC}"
else
    echo -e "${RED}✗ Error: Virtual environment activation script not found${NC}"
    exit 1
fi

# Verify pip is available
if ! command -v pip &> /dev/null; then
    echo -e "${RED}✗ Error: pip not found in virtual environment${NC}"
    echo -e "${YELLOW}  Recreating virtual environment...${NC}"
    rm -rf venv
    python3 -m venv venv
    source venv/bin/activate
fi

# Install/update dependencies
if [ -f "requirements.txt" ]; then
    echo -e "${YELLOW}→ Installing/updating dependencies...${NC}"
    pip install --upgrade pip -q
    pip install -q -r requirements.txt
    echo -e "${GREEN}✓ All dependencies installed${NC}"
fi

echo ""
echo -e "${GREEN}✓ Stage 0 Complete: Environment Ready${NC}"
echo ""

# Parse command line arguments
EXPORT_POWERBI=""
SKIP_ERRORS=""
CONFIG_PATH=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --export-powerbi)
            EXPORT_POWERBI="--export-powerbi"
            shift
            ;;
        --skip-errors)
            SKIP_ERRORS="--skip-errors"
            shift
            ;;
        --config)
            CONFIG_PATH="--config $2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --export-powerbi     Export data for Power BI"
            echo "  --skip-errors        Skip non-critical errors"
            echo "  --config <path>      Path to custom configuration file"
            echo "  -h, --help           Show this help message"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Usage: $0 [--export-powerbi] [--skip-errors] [--config <path>]"
            echo "Run '$0 --help' for more information."
            exit 1
            ;;
    esac
done

# ============================================================================
# PIPELINE EXECUTION
# ============================================================================

echo -e "${BLUE}════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  STARTING DATA ANALYTICS PIPELINE                   ${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${CYAN}Pipeline Stages:${NC}"
echo -e "  [1] Extract   → Load data from MySQL database"
echo -e "  [2] Transform → Clean and validate data"
echo -e "  [3] Analyze   → EDA, Segmentation, ROI calculation"
echo -e "  [4] Report    → Generate PDF/HTML reports"
echo -e "  [5] Export    → Power BI dashboard integration"
echo ""

# Start timing
START_TIME=$(date +%s)

# Run the Python analytics pipeline
python3 src/main.py $CONFIG_PATH $EXPORT_POWERBI $SKIP_ERRORS

# Capture exit status
PIPELINE_STATUS=$?

# Generate live dashboard if pipeline succeeded
if [ $PIPELINE_STATUS -eq 0 ]; then
    echo ""
    echo -e "${CYAN}→ Generating live dashboard from actual data...${NC}"
    python3 generate_dashboard.py 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Live dashboard generated: outputs/dashboards/live_dashboard.html${NC}"
    fi
fi

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# ============================================================================
# PIPELINE RESULTS
# ============================================================================

# Check exit status
if [ $PIPELINE_STATUS -eq 0 ]; then
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║         PIPELINE COMPLETED SUCCESSFULLY            ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
    echo ""

    echo -e "${CYAN}⏱  Execution Time: ${DURATION} seconds${NC}"
    echo ""

    echo -e "${YELLOW}📊 Pipeline Stages Completed:${NC}"
    echo -e "  ${GREEN}✓${NC} [1/5] Extract   - Data loaded from database"
    echo -e "  ${GREEN}✓${NC} [2/5] Transform - Data cleaned and validated"
    echo -e "  ${GREEN}✓${NC} [3/5] Analyze   - EDA, ML segmentation, ROI calculated"
    echo -e "  ${GREEN}✓${NC} [4/5] Report    - PDF and HTML reports generated"
    if [ -n "$EXPORT_POWERBI" ]; then
        echo -e "  ${GREEN}✓${NC} [5/5] Export    - Power BI files exported"
    else
        echo -e "  ${YELLOW}○${NC} [5/5] Export    - Skipped (use --export-powerbi flag)"
    fi
    echo ""

    echo -e "${YELLOW}📁 Output Locations:${NC}"
    echo -e "  ${CYAN}→${NC} Processed Data:   ${GREEN}data/processed/${NC}"
    echo -e "     • clean_campaign_data.csv"
    echo -e "     • clean_customer_data.csv"
    echo -e "     • customer_segments.csv"
    echo -e "     • roi_analysis.csv"
    echo ""
    echo -e "  ${CYAN}→${NC} Visualizations:   ${GREEN}outputs/visualizations/${NC}"
    echo -e "     • channel_metrics.png"
    echo -e "     • roi_by_channel.png"
    echo -e "     • customer_segments.png"
    echo -e "     • conversion_funnel.png"
    echo -e "     • ... and more"
    echo ""
    echo -e "  ${CYAN}→${NC} Reports:          ${GREEN}outputs/reports/${NC}"
    echo -e "     • executive_summary.pdf"
    echo -e "     • executive_summary.html"
    echo -e "     • campaign_insights_summary.csv"
    echo ""
    echo -e "  ${CYAN}→${NC} Live Dashboard:   ${GREEN}outputs/dashboards/${NC}"
    echo -e "     • live_dashboard.html (Dynamic data visualization)"
    echo ""
    if [ -n "$EXPORT_POWERBI" ]; then
        echo -e "  ${CYAN}→${NC} Dashboards:       ${GREEN}outputs/dashboards/${NC}"
        echo -e "     • campaign_data_powerbi.csv"
        echo -e "     • channel_performance_powerbi.csv"
        echo -e "     • customer_segments_powerbi.csv"
        echo -e "     • roi_analysis_powerbi.csv"
        echo ""
    fi

    echo -e "${CYAN}💡 Next Steps:${NC}"
    echo -e "  • View live dashboard: ${YELLOW}open outputs/dashboards/live_dashboard.html${NC}"
    echo -e "  • View reports:        ${YELLOW}open outputs/reports/executive_summary.html${NC}"
    echo -e "  • Check visualizations: ${YELLOW}open outputs/visualizations/${NC}"
    if [ -n "$EXPORT_POWERBI" ]; then
        echo -e "  • Load Power BI:      ${YELLOW}open outputs/dashboards/marketing_dashboard.pbix${NC}"
    fi
    echo ""

else
    echo ""
    echo -e "${RED}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║            PIPELINE EXECUTION FAILED               ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${RED}⏱  Failed after ${DURATION} seconds${NC}"
    echo ""
    echo -e "${YELLOW}🔍 Troubleshooting:${NC}"
    echo -e "  1. Check database connection: ${CYAN}python3 scripts/database/test_database.py${NC}"
    echo -e "  2. Verify configuration: ${CYAN}cat config/database_config.yaml${NC}"
    echo -e "  3. Check logs above for error details"
    echo -e "  4. Run with skip errors: ${CYAN}./run_analysis.sh --skip-errors${NC}"
    echo ""
    deactivate
    exit 1
fi

# Deactivate virtual environment
deactivate

