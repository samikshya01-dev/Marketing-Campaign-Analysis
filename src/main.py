"""
Main execution module for marketing campaign analysis.
"""
import argparse
from pathlib import Path
import yaml
import logging
import os
import sys

from data_loader import DataLoader
from data_cleaner import DataCleaner
from eda_analysis import EDAAnalyzer
from customer_segmentation import CustomerSegmentation
from roi_calculator import ROICalculator
from powerbi_exporter import PowerBIExporter
from generate_executive_summary import ExecutiveSummaryGenerator


def setup_logging():
    """Configure logging."""
    import sys

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create console handler with STDOUT (not STDERR)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Add formatter to handler
    console_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)

def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent

def get_config_path() -> str:
    """Get the absolute path to config file."""
    config_path = get_project_root() / "config" / "config.yaml"
    return str(config_path)

def load_config(config_path: str = None) -> dict:
    """Load main configuration."""
    try:
        if config_path is None:
            config_path = get_config_path()

        # Ensure absolute path
        if not os.path.isabs(config_path):
            config_path = os.path.join(get_project_root(), config_path)

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found at: {config_path}")

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Convert relative paths to absolute
        for key, path in config['paths'].items():
            if not os.path.isabs(path):
                config['paths'][key] = os.path.join(get_project_root(), path)

        return config
    except Exception as e:
        logging.error(f"Error loading configuration: {str(e)}")
        raise

def create_directories(config: dict) -> None:
    """Create necessary directories."""
    try:
        for path in config['paths'].values():
            Path(path).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.error(f"Error creating directories: {str(e)}")
        raise

def _generate_live_dashboard_from_db(loader, config):
    """Generate live dashboard HTML directly from database data."""
    import json
    from datetime import datetime
    import pandas as pd

    try:
        # Load fresh data from database (all 39 campaigns)
        campaigns_df = loader.load_campaigns()

        # Calculate metrics
        campaigns_df['roi'] = ((campaigns_df['revenue'] - campaigns_df['cost']) / campaigns_df['cost'] * 100)
        campaigns_df['roas'] = campaigns_df['revenue'] / campaigns_df['cost']
        campaigns_df['profit'] = campaigns_df['revenue'] - campaigns_df['cost']
        campaigns_df['ctr'] = (campaigns_df['clicks'] / campaigns_df['impressions'] * 100)

        # Overall metrics
        total_cost = float(campaigns_df['cost'].sum())
        total_revenue = float(campaigns_df['revenue'].sum())
        total_profit = float(campaigns_df['profit'].sum())
        avg_roi = float(campaigns_df['roi'].mean())
        avg_roas = float(campaigns_df['roas'].mean())
        total_campaigns = len(campaigns_df)
        total_conversions = int(campaigns_df['conversions'].sum())
        total_clicks = int(campaigns_df['clicks'].sum())
        avg_ctr = float(campaigns_df['ctr'].mean())

        # Channel performance
        channel_summary = campaigns_df.groupby('channel').agg({
            'cost': 'sum',
            'revenue': 'sum',
            'profit': 'sum',
            'conversions': 'sum'
        }).reset_index()
        channel_summary['roi'] = ((channel_summary['revenue'] - channel_summary['cost']) / channel_summary['cost'] * 100)
        channel_summary = channel_summary.sort_values('roi', ascending=False)

        # Top campaigns
        top_campaigns = campaigns_df.nlargest(6, 'roi')

        # Generate HTML content
        now = datetime.now().strftime('%B %d, %Y at %I:%M %p')

        # Build channel rows
        channel_rows = ""
        for _, row in channel_summary.iterrows():
            roi_val = row['roi']
            perf = '⭐⭐⭐⭐⭐ Excellent' if roi_val >= 400 else '⭐⭐⭐⭐ Very Good' if roi_val >= 300 else '⭐⭐⭐ Good'
            channel_rows += f"""<tr><td><strong>{row['channel']}</strong></td>
            <td>Rs. {row['cost']:,.2f}</td><td>Rs. {row['revenue']:,.2f}</td>
            <td>Rs. {row['profit']:,.2f}</td><td><span class="highlight">{row['roi']:.2f}%</span></td>
            <td>{int(row['conversions']):,}</td><td><span class="badge">{perf}</span></td></tr>"""

        # Build campaign rows
        campaign_rows = ""
        for _, camp in top_campaigns.iterrows():
            campaign_rows += f"""<tr><td>{camp['campaign_name']}</td>
            <td><span class="badge">{camp['channel']}</span></td><td>{camp['date']}</td>
            <td>Rs. {camp['cost']:,.2f}</td><td>Rs. {camp['revenue']:,.2f}</td>
            <td><span class="highlight">{camp['roi']:.2f}%</span></td></tr>"""

        # Chart data
        channel_labels = json.dumps(channel_summary['channel'].tolist())
        channel_roi = json.dumps(channel_summary['roi'].tolist())
        channel_revenue = json.dumps(channel_summary['revenue'].tolist())
        channel_cost = json.dumps(channel_summary['cost'].tolist())
        channel_conversions = json.dumps(channel_summary['conversions'].tolist())

        html_content = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Live Dashboard - {total_campaigns} Campaigns</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:20px}}
.container{{max-width:1400px;margin:0 auto;background:white;border-radius:15px;box-shadow:0 20px 60px rgba(0,0,0,0.3)}}
.header{{background:linear-gradient(135deg,#1e3c72 0%,#2a5298 100%);color:white;padding:40px;text-align:center}}
.header h1{{font-size:2.5em}}
.content{{padding:40px}}
.metrics-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px;margin:30px 0}}
.metric-card{{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:25px;border-radius:10px;text-align:center;box-shadow:0 5px 15px rgba(102,126,234,0.4)}}
.metric-value{{font-size:1.8em;font-weight:bold}}
.section-title{{font-size:1.8em;color:#1e3c72;margin:40px 0 20px;border-left:5px solid #667eea;padding-left:15px}}
table{{width:100%;border-collapse:collapse;background:#f8f9fa;border-radius:10px;overflow:hidden}}
th{{background:#667eea;color:white;padding:15px;text-align:left}}
td{{padding:15px;border-bottom:1px solid #e5e7eb}}
tr:hover{{background:#f0f1ff}}
.highlight{{background:#fef3c7;padding:2px 6px;border-radius:4px;font-weight:600}}
.badge{{padding:4px 8px;border-radius:4px;font-size:0.85em;background:#dbeafe;color:#1e40af}}
.charts-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(500px,1fr));gap:20px;margin:20px 0}}
.chart-container{{background:#f8f9fa;padding:20px;border-radius:10px}}
.insights{{background:#eff6ff;border-left:5px solid #3b82f6;padding:25px;border-radius:10px;margin:20px 0}}
.footer{{background:#f3f4f6;padding:20px;text-align:center;color:#6b7280;margin-top:40px}}
</style></head><body>
<div class="container">
<div class="header"><h1>📊 Live Marketing Dashboard</h1>
<p>Real-Time from MySQL Database | {total_campaigns} Campaigns | Updated: {now}</p></div>
<div class="content">
<div style="background:#e0e7ff;border:1px solid #818cf8;padding:12px;border-radius:8px;margin:20px 0;color:#3730a3">
<strong>📁 Data Source:</strong> MySQL Database | Showing all {total_campaigns} campaigns (no filtering)</div>
<div class="section-title">📈 Key Metrics</div>
<div class="metrics-grid">
<div class="metric-card"><div style="font-size:0.9em;opacity:0.9;margin-bottom:10px">Total Cost</div>
<div class="metric-value">Rs. {total_cost:,.2f}</div></div>
<div class="metric-card"><div style="font-size:0.9em;opacity:0.9;margin-bottom:10px">Total Revenue</div>
<div class="metric-value">Rs. {total_revenue:,.2f}</div></div>
<div class="metric-card"><div style="font-size:0.9em;opacity:0.9;margin-bottom:10px">Total Profit</div>
<div class="metric-value">Rs. {total_profit:,.2f}</div></div>
<div class="metric-card"><div style="font-size:0.9em;opacity:0.9;margin-bottom:10px">Average ROI</div>
<div class="metric-value">{avg_roi:.2f}%</div></div>
<div class="metric-card"><div style="font-size:0.9em;opacity:0.9;margin-bottom:10px">Average ROAS</div>
<div class="metric-value">{avg_roas:.2f}x</div></div>
<div class="metric-card"><div style="font-size:0.9em;opacity:0.9;margin-bottom:10px">Total Campaigns</div>
<div class="metric-value">{total_campaigns}</div></div>
</div>
<div class="section-title">🎯 Channel Performance</div>
<table><thead><tr><th>Channel</th><th>Cost</th><th>Revenue</th><th>Profit</th><th>ROI</th><th>Conversions</th><th>Status</th></tr></thead>
<tbody>{channel_rows}</tbody></table>
<div class="insights"><strong>💡 Key Insights:</strong><br>
• Database contains {total_campaigns} total campaigns across {len(channel_summary)} channels<br>
• Total Profitability: Rs. {total_profit:,.2f} ({avg_roi:.2f}% avg ROI)<br>
• Total Conversions: {total_conversions:,} ({avg_ctr:.2f}% avg CTR)<br>
• Data directly from MySQL - no duplicates removed
</div>
<div class="section-title">📊 Visual Analytics</div>
<div class="charts-grid">
<div class="chart-container"><canvas id="roiChart"></canvas></div>
<div class="chart-container"><canvas id="revenueChart"></canvas></div>
</div>
<div class="section-title">🏆 Top Campaigns by ROI</div>
<table><thead><tr><th>Campaign</th><th>Channel</th><th>Date</th><th>Cost</th><th>Revenue</th><th>ROI</th></tr></thead>
<tbody>{campaign_rows}</tbody></table>
<div class="footer"><strong>Live Dashboard</strong> | {total_campaigns} campaigns from database<br>
<small>Generated: {now}</small></div>
</div></div>
<script>
const colors=['#667eea','#764ba2','#f093fb','#4facfe','#43e97b'];
new Chart(document.getElementById('roiChart'),{{type:'bar',data:{{labels:{channel_labels},
datasets:[{{label:'ROI (%)',data:{channel_roi},backgroundColor:colors,borderRadius:8}}]}},
options:{{responsive:true,plugins:{{legend:{{position:'top'}}}},scales:{{y:{{beginAtZero:true}}}}}}}});
new Chart(document.getElementById('revenueChart'),{{type:'doughnut',data:{{
labels:{channel_labels},datasets:[{{data:{channel_revenue},backgroundColor:colors,borderWidth:2}}]}},
options:{{responsive:true,plugins:{{legend:{{position:'bottom'}}}}}}}});
</script></body></html>"""

        # Save dashboard
        dashboard_path = Path(config['paths']['dashboards']) / 'live_dashboard.html'
        dashboard_path.parent.mkdir(parents=True, exist_ok=True)

        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return str(dashboard_path)

    except Exception as e:
        logging.error(f"Dashboard generation error: {str(e)}")
        return None

def main(args):
    """Main execution function for the analytics pipeline."""
    # Setup
    setup_logging()
    logger = logging.getLogger(__name__)

    # Pipeline header
    logger.info("=" * 70)
    logger.info("MARKETING CAMPAIGN ANALYTICS PIPELINE")
    logger.info("=" * 70)

    # Load configuration
    config = load_config()
    config_path = get_config_path()
    create_directories(config)

    try:
        # ====================================================================
        # STAGE 1: DATA EXTRACTION
        # ====================================================================
        logger.info("")
        logger.info("[STAGE 1/5] DATA EXTRACTION - Loading from MySQL Database")
        logger.info("-" * 70)

        # Initialize data loader
        loader = DataLoader(config_path=config_path)

        # Load data from database
        campaigns_df = loader.load_campaigns()
        customers_df = loader.load_customers()

        logger.info(f"✓ Loaded {len(campaigns_df)} campaign records")
        logger.info(f"✓ Loaded {len(customers_df)} customer records")
        logger.info("✓ Stage 1 Complete: Data extraction successful")

        # ====================================================================
        # STAGE 2: DATA TRANSFORMATION
        # ====================================================================
        logger.info("")
        logger.info("[STAGE 2/5] DATA TRANSFORMATION - Cleaning and Validation")
        logger.info("-" * 70)

        # Initialize cleaner
        cleaner = DataCleaner(config_path=config_path)

        # Clean campaign data
        logger.info("→ Cleaning campaign data...")
        clean_campaigns = cleaner.clean_campaign_data(campaigns_df)
        logger.info(f"  ✓ Cleaned {len(clean_campaigns)} campaign records")

        # Clean customer data
        logger.info("→ Cleaning customer data...")
        clean_customers = cleaner.clean_customer_data(customers_df)
        logger.info(f"  ✓ Cleaned {len(clean_customers)} customer records")

        # Save cleaned data
        logger.info("→ Saving processed data...")
        loader.save_to_csv(clean_campaigns, "clean_campaign_data.csv", config['paths']['processed_data'])
        loader.save_to_csv(clean_customers, "clean_customer_data.csv", config['paths']['processed_data'])

        logger.info("✓ Stage 2 Complete: Data transformation successful")

        # ====================================================================
        # STAGE 3: DATA ANALYSIS
        # ====================================================================
        logger.info("")
        logger.info("[STAGE 3/5] DATA ANALYSIS - EDA, Segmentation, ROI")
        logger.info("-" * 70)

        # Initialize analyzers
        analyzer = EDAAnalyzer(config_path=config_path)
        segmentation = CustomerSegmentation(config_path=config_path)
        roi_calc = ROICalculator(config_path=config_path)

        # 3A: Exploratory Data Analysis
        logger.info("→ [3.1] Performing Exploratory Data Analysis...")
        analyzer.plot_campaign_performance(clean_campaigns, config['paths']['visualizations'])
        eda_report = analyzer.generate_eda_report(clean_campaigns)
        logger.info("  ✓ EDA completed - visualizations generated")

        # 3B: Customer Segmentation (ML)
        logger.info("→ [3.2] Performing ML-based Customer Segmentation...")
        segmented_df, model = segmentation.segment_customers(clean_customers)
        segmentation.plot_segments(segmented_df, config['paths']['visualizations'])
        segment_profiles = segmentation.get_segment_profiles(segmented_df)
        loader.save_to_csv(segmented_df, "customer_segments.csv", config['paths']['processed_data'])
        n_clusters = segmented_df['cluster'].nunique()
        logger.info(f"  ✓ Segmentation completed - {n_clusters} customer clusters identified")

        # 3C: ROI Analysis
        logger.info("→ [3.3] Calculating ROI and Financial Metrics...")
        roi_df = roi_calc.calculate_campaign_roi(clean_campaigns)
        roi_calc.plot_roi_analysis(roi_df, config['paths']['visualizations'])
        roi_report = roi_calc.generate_roi_report(roi_df)
        roi_calc.export_summary(roi_df, f"{config['paths']['reports']}/campaign_insights_summary.csv")
        avg_roi = roi_df['roi'].mean()
        logger.info(f"  ✓ ROI analysis completed - Average ROI: {avg_roi:.2f}%")

        logger.info("✓ Stage 3 Complete: Data analysis successful")

        # ====================================================================
        # STAGE 4: REPORT GENERATION
        # ====================================================================
        logger.info("")
        logger.info("[STAGE 4/5] REPORT GENERATION - PDF and HTML Reports")
        logger.info("-" * 70)

        try:
            summary_generator = ExecutiveSummaryGenerator(config_path=config_path)

            # Generate PDF report
            logger.info("→ Generating executive summary PDF...")
            try:
                pdf_path = summary_generator.generate_pdf()
                logger.info(f"  ✓ PDF report generated: {pdf_path}")
            except Exception as pdf_error:
                logger.warning(f"  ⚠ PDF generation failed: {str(pdf_error)}")
                if not args.skip_errors:
                    raise

            # Generate HTML report
            logger.info("→ Generating executive summary HTML...")
            html_path = summary_generator.generate_html_report()
            logger.info(f"  ✓ HTML report generated: {html_path}")

            logger.info("✓ Stage 4 Complete: Reports generated successfully")

        except Exception as e:
            logger.error(f"Report generation error: {str(e)}")
            if not args.skip_errors:
                raise

        # ====================================================================
        # STAGE 5: POWER BI EXPORT (Optional)
        # ====================================================================
        if args.export_powerbi:
            logger.info("")
            logger.info("[STAGE 5/5] POWER BI EXPORT - Dashboard Integration")
            logger.info("-" * 70)

            try:
                logger.info("→ Preparing data for Power BI export...")

                # Get available columns
                available_cols = clean_campaigns.columns.tolist()

                # Prepare channel performance summary with available columns
                agg_dict = {
                    'revenue': 'sum',
                    'conversions': 'sum',
                    'cost': 'sum',
                    'impressions': 'sum',
                    'clicks': 'sum'
                }

                # Add optional columns if available
                if 'sessions' in available_cols:
                    agg_dict['sessions'] = 'sum'
                if 'users' in available_cols:
                    agg_dict['users'] = 'sum'
                if 'pageviews' in available_cols:
                    agg_dict['pageviews'] = 'sum'
                if 'avg_session_duration' in available_cols:
                    agg_dict['avg_session_duration'] = 'mean'
                if 'pages_per_session' in available_cols:
                    agg_dict['pages_per_session'] = 'mean'
                if 'bounce_rate' in available_cols:
                    agg_dict['bounce_rate'] = 'mean'

                channel_summary = clean_campaigns.groupby('channel').agg(agg_dict).reset_index()

                # Calculate additional metrics
                if 'conversions' in channel_summary.columns and 'sessions' in channel_summary.columns:
                    channel_summary['conversion_rate'] = (channel_summary['conversions'] / channel_summary['sessions'] * 100).round(2)
                    channel_summary['overall_conversion_rate'] = (channel_summary['conversions'] / channel_summary['sessions'] * 100).round(2)

                if 'revenue' in channel_summary.columns and 'sessions' in channel_summary.columns:
                    channel_summary['avg_revenue_per_session'] = (channel_summary['revenue'] / channel_summary['sessions']).round(2)

                if 'revenue' in channel_summary.columns and 'conversions' in channel_summary.columns:
                    channel_summary['avg_order_value'] = (channel_summary['revenue'] / channel_summary['conversions']).round(2)

                # Export to Power BI
                logger.info("→ Exporting datasets to Power BI format...")
                exporter = PowerBIExporter(config['paths']['dashboards'])
                exports = exporter.export_all(
                    campaign_df=clean_campaigns,
                    customer_df=segmented_df,
                    roi_df=roi_df,
                    channel_df=channel_summary
                )
                logger.info(f"  ✓ Power BI exports created: {len(exports)} files")
                logger.info("✓ Stage 5 Complete: Power BI export successful")
            except Exception as e:
                logger.error(f"Power BI export error: {str(e)}")
                if not args.skip_errors:
                    raise
        else:
            logger.info("")
            logger.info("[STAGE 5/5] POWER BI EXPORT - Skipped")
            logger.info("  ℹ Use --export-powerbi flag to enable Power BI export")

        # ====================================================================
        # PIPELINE COMPLETION
        # ====================================================================

        # Generate live dashboard with actual data
        try:
            logger.info("→ Generating live HTML dashboard from database...")
            dashboard_path = _generate_live_dashboard_from_db(loader, config)
            if dashboard_path:
                logger.info(f"  ✓ Live dashboard: {dashboard_path}")
        except Exception as e:
            logger.warning(f"Could not generate live dashboard: {str(e)}")

        logger.info("")
        logger.info("=" * 70)
        logger.info("✓ PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 70)
        logger.info("")
        logger.info("Output Summary:")
        logger.info(f"  • Campaign records processed: {len(clean_campaigns)}")
        logger.info(f"  • Customer records processed: {len(clean_customers)}")
        logger.info(f"  • Customer segments identified: {n_clusters}")
        logger.info(f"  • Average ROI: {avg_roi:.2f}%")
        logger.info(f"  • Visualizations: outputs/visualizations/")
        logger.info(f"  • Reports: outputs/reports/")
        logger.info(f"  • Live Dashboard: outputs/dashboards/live_dashboard.html")
        if args.export_powerbi:
            logger.info(f"  • Power BI files: outputs/dashboards/")
        logger.info("")

    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Marketing Campaign Analysis")
    parser.add_argument('--config', default=None, help='Path to configuration file (optional)')
    parser.add_argument('--export-powerbi', action='store_true', help='Export data for Power BI')
    parser.add_argument('--skip-errors', action='store_true', help='Skip non-critical errors')
    args = parser.parse_args()

    main(args)
