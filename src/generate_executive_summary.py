"""
Executive Summary PDF Generator for Marketing Campaign Analysis.
Generates dynamic PDF reports with rupees (₹) currency.
"""
import os
from pathlib import Path
import pandas as pd
from typing import Dict
import yaml
import logging
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, white
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False
    print("Warning: reportlab not installed. PDF generation will be limited.")

logger = logging.getLogger(__name__)


class ExecutiveSummaryGenerator:
    """Generate executive summary PDF reports with dynamic data."""

    def __init__(self, config_path: str = "config/config.yaml", currency_symbol: str = "Rs."):
        """Initialize the executive summary generator."""
        # Handle config path - convert to absolute if relative
        if not os.path.isabs(config_path):
            config_path = os.path.join(Path(__file__).parent.parent, config_path)

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.currency_symbol = currency_symbol

        if HAS_REPORTLAB:
            self.styles = getSampleStyleSheet()
            self._create_custom_styles()
        else:
            self.styles = None

    def _create_custom_styles(self):
        """Create custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#1F2937'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#374151'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=HexColor('#4B5563'),
            spaceAfter=6
        ))

    def _format_currency(self, value: float) -> str:
        """Format value as Indian rupees."""
        return f"{self.currency_symbol}{value:,.2f}"

    def _format_percentage(self, value: float) -> str:
        """Format value as percentage."""
        return f"{value:.2f}%"

    def _load_roi_data(self) -> Dict:
        """Load ROI analysis data from CSV."""
        try:
            roi_csv_path = os.path.join(
                self.config['paths']['processed_data'],
                'roi_analysis.csv'
            )

            if not os.path.exists(roi_csv_path):
                logger.warning(f"ROI analysis file not found at {roi_csv_path}")
                return self._create_empty_roi_dict()

            df = pd.read_csv(roi_csv_path)

            # Calculate metrics dynamically
            channel_perf_df = df.groupby('channel').agg({
                'cost': 'sum',
                'revenue': 'sum',
                'profit': 'sum',
                'roi': 'mean'
            }).round(2)

            # Convert to proper dictionary format {channel: {metric: value}}
            channel_performance = {}
            for channel in channel_perf_df.index:
                channel_performance[channel] = {
                    'cost': channel_perf_df.loc[channel, 'cost'],
                    'revenue': channel_perf_df.loc[channel, 'revenue'],
                    'profit': channel_perf_df.loc[channel, 'profit'],
                    'roi': channel_perf_df.loc[channel, 'roi']
                }

            roi_data = {
                'total_cost': df['cost'].sum(),
                'total_revenue': df['revenue'].sum(),
                'total_profit': df['profit'].sum(),
                'average_roi': df['roi'].mean(),
                'average_roas': df['roas'].mean(),
                'best_channel': df.groupby('channel')['roi'].mean().idxmax(),
                'worst_channel': df.groupby('channel')['roi'].mean().idxmin(),
                'total_campaigns': len(df),
                'total_conversions': df['conversions'].sum() if 'conversions' in df.columns else 0,
                'channel_performance': channel_performance
            }

            return roi_data
        except Exception as e:
            logger.error(f"Error loading ROI data: {str(e)}")
            return self._create_empty_roi_dict()

    def _create_empty_roi_dict(self) -> Dict:
        """Create empty ROI dictionary for when data is unavailable."""
        return {
            'total_cost': 0,
            'total_revenue': 0,
            'total_profit': 0,
            'average_roi': 0,
            'average_roas': 0,
            'best_channel': 'N/A',
            'worst_channel': 'N/A',
            'total_campaigns': 0,
            'total_conversions': 0,
            'channel_performance': {}
        }

    def _create_header_table(self) -> Table:
        """Create header table with key metrics."""
        roi_data = self._load_roi_data()

        # Create header data
        header_data = [
            ['Metric', 'Value'],
            ['Total Cost', self._format_currency(roi_data['total_cost'])],
            ['Total Revenue', self._format_currency(roi_data['total_revenue'])],
            ['Total Profit', self._format_currency(roi_data['total_profit'])],
            ['Average ROI', self._format_percentage(roi_data['average_roi'])],
            ['Average ROAS', f"{roi_data['average_roas']:.2f}x"],
            ['Total Campaigns', str(roi_data['total_campaigns'])],
            ['Total Conversions', str(int(roi_data['total_conversions']))],
        ]

        # Create table with styling
        table = Table(header_data, colWidths=[2.5 * inch, 2.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1F2937')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F3F4F6')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#D1D5DB')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#F9FAFB')])
        ]))

        return table

    def _create_channel_performance_table(self) -> Table:
        """Create channel performance analysis table."""
        roi_data = self._load_roi_data()
        channel_perf = roi_data['channel_performance']

        # Create table data
        table_data = [
            ['Channel', 'Total Cost', 'Total Revenue', 'Profit', 'Avg ROI']
        ]

        if channel_perf:
            for channel, metrics in channel_perf.items():
                table_data.append([
                    channel,
                    self._format_currency(metrics['cost']),
                    self._format_currency(metrics['revenue']),
                    self._format_currency(metrics['profit']),
                    self._format_percentage(metrics['roi'])
                ])
        else:
            table_data.append(['No data available', '', '', '', ''])

        # Create table with styling
        table = Table(table_data, colWidths=[1.3 * inch, 1.1 * inch, 1.3 * inch, 1.1 * inch, 1.2 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#3B82F6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F0F9FF')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#93C5FD')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#F8FAFC')])
        ]))

        return table

    def _create_insights_section(self) -> list:
        """Create insights and recommendations section."""
        roi_data = self._load_roi_data()
        elements = []

        # Title
        elements.append(Paragraph("Key Insights & Recommendations", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.15 * inch))

        # Insights content
        insights = [
            f"<b>Overall Performance:</b> Total Revenue of {self._format_currency(roi_data['total_revenue'])} "
            f"generated from an investment of {self._format_currency(roi_data['total_cost'])}, "
            f"resulting in a profit of {self._format_currency(roi_data['total_profit'])}.",

            f"<b>Best Performing Channel:</b> The <i>{roi_data['best_channel']}</i> channel demonstrates "
            f"the highest ROI and should be prioritized for budget allocation.",

            f"<b>Average Return Metrics:</b> Average ROI of {self._format_percentage(roi_data['average_roi'])} "
            f"and ROAS of {roi_data['average_roas']:.2f}x across all campaigns.",

            "<b>Recommendations:</b> Focus marketing efforts on high-performing channels, optimize underperforming "
            "campaigns with A/B testing, and consider reallocating budget from low-ROI channels.",

            "<b>Customer Insights:</b> Analyze customer segments to identify high-value buyers and tailor campaigns "
            "to improve conversion rates and customer lifetime value."
        ]

        for insight in insights:
            elements.append(Paragraph(insight, self.styles['CustomBody']))
            elements.append(Spacer(1, 0.1 * inch))

        return elements

    def generate_pdf(self, output_path: str = None) -> str:
        """Generate executive summary PDF."""
        if not HAS_REPORTLAB:
            logger.error("reportlab is not installed. Please install it with: pip install reportlab")
            raise ImportError("reportlab is not installed. Please install it with: pip install reportlab")

        try:
            if output_path is None:
                output_dir = self.config['paths']['reports']
            else:
                output_dir = os.path.dirname(output_path) or self.config['paths']['reports']

            os.makedirs(output_dir, exist_ok=True)

            if output_path is None:
                output_path = os.path.join(output_dir, 'executive_summary.pdf')

            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=0.75 * inch,
                leftMargin=0.75 * inch,
                topMargin=0.75 * inch,
                bottomMargin=0.75 * inch
            )

            # Build document elements
            elements = []

            # Title
            elements.append(Paragraph(
                "Marketing Campaign Analysis",
                self.styles['CustomTitle']
            ))
            elements.append(Paragraph(
                "Executive Summary Report",
                self.styles['CustomHeading']
            ))
            elements.append(Spacer(1, 0.2 * inch))

            # Date
            report_date = datetime.now().strftime("%B %d, %Y")
            elements.append(Paragraph(
                f"Report Generated: {report_date}",
                self.styles['CustomBody']
            ))
            elements.append(Spacer(1, 0.25 * inch))

            # Key Metrics Section
            elements.append(Paragraph("Key Performance Metrics", self.styles['CustomHeading']))
            elements.append(Spacer(1, 0.1 * inch))
            elements.append(self._create_header_table())
            elements.append(Spacer(1, 0.3 * inch))

            # Channel Performance Section
            elements.append(Paragraph("Channel Performance Analysis", self.styles['CustomHeading']))
            elements.append(Spacer(1, 0.1 * inch))
            elements.append(self._create_channel_performance_table())
            elements.append(Spacer(1, 0.3 * inch))

            # Insights Section
            elements.extend(self._create_insights_section())

            # Footer
            elements.append(Spacer(1, 0.2 * inch))
            elements.append(Paragraph(
                "Generated by Marketing Campaign Analysis System | All values in Indian Rupees (Rs.)",
                self.styles['Normal']
            ))

            # Build PDF
            doc.build(elements)
            logger.info(f"Executive summary PDF generated: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error generating executive summary PDF: {str(e)}")
            raise

    def generate_html_report(self, output_path: str = None) -> str:
        """Generate an alternative HTML report (for web viewing)."""
        try:
            if output_path is None:
                output_dir = self.config['paths']['reports']
            else:
                output_dir = os.path.dirname(output_path) or self.config['paths']['reports']

            os.makedirs(output_dir, exist_ok=True)

            if output_path is None:
                output_path = os.path.join(output_dir, 'executive_summary.html')

            roi_data = self._load_roi_data()
            report_date = datetime.now().strftime("%B %d, %Y")

            # Build channel rows
            channel_rows = ""
            if roi_data['channel_performance']:
                for channel, metrics in roi_data['channel_performance'].items():
                    # metrics is a dict with 'cost', 'revenue', 'profit', 'roi' keys
                    cost = metrics.get('cost', 0) if isinstance(metrics, dict) else 0
                    revenue = metrics.get('revenue', 0) if isinstance(metrics, dict) else 0
                    profit = metrics.get('profit', 0) if isinstance(metrics, dict) else 0
                    roi = metrics.get('roi', 0) if isinstance(metrics, dict) else 0

                    channel_rows += f"""
                    <tr>
                        <td>{channel}</td>
                        <td>{self._format_currency(cost)}</td>
                        <td>{self._format_currency(revenue)}</td>
                        <td>{self._format_currency(profit)}</td>
                        <td>{self._format_percentage(roi)}</td>
                    </tr>
                    """
            else:
                channel_rows = "<tr><td colspan='5'>No data available</td></tr>"

            # HTML template
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Marketing Campaign Analysis - Executive Summary</title>
                <style>
                    * {{
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 20px;
                        min-height: 100vh;
                    }}
                    .container {{
                        max-width: 1000px;
                        margin: 0 auto;
                        background: white;
                        border-radius: 10px;
                        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
                        padding: 40px;
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 30px;
                        border-bottom: 3px solid #3b82f6;
                        padding-bottom: 20px;
                    }}
                    .header h1 {{
                        font-size: 2.5em;
                        color: #1f2937;
                        margin-bottom: 5px;
                    }}
                    .header p {{
                        font-size: 1.1em;
                        color: #6b7280;
                    }}
                    .date {{
                        font-size: 0.9em;
                        color: #9ca3af;
                        margin-top: 10px;
                    }}
                    .metrics-grid {{
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                        gap: 20px;
                        margin: 30px 0;
                    }}
                    .metric-card {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 20px;
                        border-radius: 8px;
                        text-align: center;
                    }}
                    .metric-label {{
                        font-size: 0.9em;
                        opacity: 0.9;
                        margin-bottom: 8px;
                    }}
                    .metric-value {{
                        font-size: 1.5em;
                        font-weight: bold;
                    }}
                    .section {{
                        margin: 30px 0;
                    }}
                    .section h2 {{
                        font-size: 1.5em;
                        color: #1f2937;
                        margin-bottom: 15px;
                        border-left: 4px solid #3b82f6;
                        padding-left: 10px;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin: 15px 0;
                    }}
                    th {{
                        background-color: #3b82f6;
                        color: white;
                        padding: 12px;
                        text-align: left;
                        font-weight: 600;
                    }}
                    td {{
                        padding: 10px 12px;
                        border-bottom: 1px solid #e5e7eb;
                    }}
                    tr:hover {{
                        background-color: #f9fafb;
                    }}
                    .insights {{
                        background-color: #eff6ff;
                        border-left: 4px solid #3b82f6;
                        padding: 15px;
                        margin: 15px 0;
                        border-radius: 4px;
                    }}
                    .insights p {{
                        margin: 10px 0;
                        color: #1e40af;
                        line-height: 1.6;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 40px;
                        padding-top: 20px;
                        border-top: 1px solid #e5e7eb;
                        color: #9ca3af;
                        font-size: 0.9em;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Marketing Campaign Analysis</h1>
                        <p>Executive Summary Report</p>
                        <div class="date">Report Generated: {report_date}</div>
                    </div>

                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div class="metric-label">Total Cost</div>
                            <div class="metric-value">{self._format_currency(roi_data['total_cost'])}</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Total Revenue</div>
                            <div class="metric-value">{self._format_currency(roi_data['total_revenue'])}</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Total Profit</div>
                            <div class="metric-value">{self._format_currency(roi_data['total_profit'])}</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Average ROI</div>
                            <div class="metric-value">{self._format_percentage(roi_data['average_roi'])}</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Average ROAS</div>
                            <div class="metric-value">{roi_data['average_roas']:.2f}x</div>
                        </div>
                    </div>

                    <div class="section">
                        <h2>Channel Performance Analysis</h2>
                        <table>
                            <thead>
                                <tr>
                                    <th>Channel</th>
                                    <th>Total Cost</th>
                                    <th>Total Revenue</th>
                                    <th>Profit</th>
                                    <th>Avg ROI</th>
                                </tr>
                            </thead>
                            <tbody>
                                {channel_rows}
                            </tbody>
                        </table>
                    </div>

                    <div class="section">
                        <h2>Key Insights & Recommendations</h2>
                        <div class="insights">
                            <p><strong>Overall Performance:</strong> Total Revenue of {self._format_currency(roi_data['total_revenue'])} 
                            generated from an investment of {self._format_currency(roi_data['total_cost'])}, 
                            resulting in a profit of {self._format_currency(roi_data['total_profit'])}.</p>
                        </div>
                        <div class="insights">
                            <p><strong>Best Performing Channel:</strong> The <em>{roi_data['best_channel']}</em> channel demonstrates 
                            the highest ROI and should be prioritized for budget allocation.</p>
                        </div>
                        <div class="insights">
                            <p><strong>Average Return Metrics:</strong> Average ROI of {self._format_percentage(roi_data['average_roi'])} 
                            and ROAS of {roi_data['average_roas']:.2f}x across all campaigns.</p>
                        </div>
                        <div class="insights">
                            <p><strong>Recommendations:</strong> Focus marketing efforts on high-performing channels, optimize underperforming 
                            campaigns with A/B testing, and consider reallocating budget from low-ROI channels.</p>
                        </div>
                    </div>

                    <div class="footer">
                        <p>Generated by Marketing Campaign Analysis System | All values in Indian Rupees (Rs.)</p>
                    </div>
                </div>
            </body>
            </html>
            """

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            logger.info(f"Executive summary HTML report generated: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error generating HTML report: {str(e)}")
            raise


if __name__ == "__main__":
    # Test the generator
    generator = ExecutiveSummaryGenerator()
    pdf_path = generator.generate_pdf()
    html_path = generator.generate_html_report()
    print(f"PDF generated: {pdf_path}")
    print(f"HTML generated: {html_path}")

