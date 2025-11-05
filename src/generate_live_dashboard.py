#!/usr/bin/env python3
"""
Generate live dashboard HTML directly from database.
This ensures we show all 39 campaigns.
"""
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import sys

def main():
    try:
        # Load data directly from database
        sys.path.insert(0, '')
        from data_loader import DataLoader

        print("Loading data from database...")
        loader = DataLoader()
        campaigns_df = loader.load_campaigns()

        print(f"✓ Loaded {len(campaigns_df)} campaigns from database")

        # Calculate metrics from raw data
        campaigns_df['roi'] = ((campaigns_df['revenue'] - campaigns_df['cost']) / campaigns_df['cost'] * 100)
        campaigns_df['roas'] = campaigns_df['revenue'] / campaigns_df['cost']
        campaigns_df['profit'] = campaigns_df['revenue'] - campaigns_df['cost']
        campaigns_df['ctr'] = (campaigns_df['clicks'] / campaigns_df['impressions'] * 100)
        campaigns_df['conversion_rate'] = (campaigns_df['conversions'] / campaigns_df['clicks'] * 100)

        # Calculate overall metrics
        total_cost = campaigns_df['cost'].sum()
        total_revenue = campaigns_df['revenue'].sum()
        total_profit = campaigns_df['profit'].sum()
        avg_roi = campaigns_df['roi'].mean()
        avg_roas = campaigns_df['roas'].mean()
        total_campaigns = len(campaigns_df)
        total_conversions = campaigns_df['conversions'].sum()
        total_clicks = campaigns_df['clicks'].sum()
        total_impressions = campaigns_df['impressions'].sum()
        avg_ctr = campaigns_df['ctr'].mean()

        # Channel performance
        channel_summary = campaigns_df.groupby('channel').agg({
            'cost': 'sum',
            'revenue': 'sum',
            'profit': 'sum',
            'conversions': 'sum',
            'impressions': 'sum',
            'clicks': 'sum'
        }).reset_index()

        channel_summary['roi'] = ((channel_summary['revenue'] - channel_summary['cost']) / channel_summary['cost'] * 100)
        channel_summary['ctr'] = (channel_summary['clicks'] / channel_summary['impressions'] * 100)
        channel_summary = channel_summary.sort_values('roi', ascending=False)

        # Top campaigns
        top_campaigns = campaigns_df.nlargest(6, 'roi')[['campaign_name', 'channel', 'date', 'cost', 'revenue', 'roi']]

        # Best performers
        best_channel_name = channel_summary.iloc[0]['channel']
        best_channel_roi = channel_summary.iloc[0]['roi']
        highest_revenue_channel = channel_summary.nlargest(1, 'revenue').iloc[0]['channel']
        highest_revenue_value = channel_summary.nlargest(1, 'revenue').iloc[0]['revenue']

        print(f"✓ Total Cost: Rs. {total_cost:,.2f}")
        print(f"✓ Total Revenue: Rs. {total_revenue:,.2f}")
        print(f"✓ Average ROI: {avg_roi:.2f}%")

        # Generate HTML
        html_content = generate_dashboard_html(
            total_cost, total_revenue, total_profit, avg_roi, avg_roas,
            total_campaigns, total_conversions, total_clicks, avg_ctr,
            channel_summary, top_campaigns, best_channel_name, best_channel_roi,
            highest_revenue_channel, highest_revenue_value
        )

        # Save to file
        output_path = Path('../outputs/dashboards/live_dashboard.html')
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✓ Dashboard generated: {output_path}")
        print(f"\nOpen dashboard: open {output_path}")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def generate_dashboard_html(total_cost, total_revenue, total_profit, avg_roi, avg_roas,
                            total_campaigns, total_conversions, total_clicks, avg_ctr,
                            channel_summary, top_campaigns, best_channel_name, best_channel_roi,
                            highest_revenue_channel, highest_revenue_value):
    """Generate the complete HTML dashboard."""

    now = datetime.now().strftime('%B %d, %Y at %I:%M %p')

    # Build channel rows HTML
    channel_rows_html = ""
    for _, row in channel_summary.iterrows():
        roi_val = row['roi']
        if roi_val >= 400:
            performance = '<span class="badge badge-success">⭐⭐⭐⭐⭐ Excellent</span>'
        elif roi_val >= 300:
            performance = '<span class="badge badge-success">⭐⭐⭐⭐ Very Good</span>'
        elif roi_val >= 200:
            performance = '<span class="badge badge-info">⭐⭐⭐ Good</span>'
        else:
            performance = '<span class="badge badge-warning">⭐⭐ Average</span>'

        channel_rows_html += f"""
                        <tr>
                            <td><strong>{row['channel']}</strong></td>
                            <td>Rs. {row['cost']:,.2f}</td>
                            <td>Rs. {row['revenue']:,.2f}</td>
                            <td>Rs. {row['profit']:,.2f}</td>
                            <td><span class="highlight">{row['roi']:.2f}%</span></td>
                            <td>{int(row['conversions']):,}</td>
                            <td>{performance}</td>
                        </tr>
"""

    # Build top campaigns HTML
    campaign_rows_html = ""
    for _, campaign in top_campaigns.iterrows():
        campaign_rows_html += f"""
                        <tr>
                            <td>{campaign['campaign_name']}</td>
                            <td><span class="badge badge-info">{campaign['channel']}</span></td>
                            <td>{campaign['date']}</td>
                            <td>Rs. {campaign['cost']:,.2f}</td>
                            <td>Rs. {campaign['revenue']:,.2f}</td>
                            <td><span class="highlight">{campaign['roi']:.2f}%</span></td>
                        </tr>
"""

    # Prepare data for charts
    channel_labels = channel_summary['channel'].tolist()
    channel_revenue = channel_summary['revenue'].tolist()
    channel_roi = channel_summary['roi'].tolist()
    channel_cost = channel_summary['cost'].tolist()
    channel_conversions = channel_summary['conversions'].tolist()

    # Generate complete HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Marketing Campaign Dashboard - Live Data</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; min-height: 100vh; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ font-size: 1.1em; opacity: 0.9; }}
        .update-badge {{ background: rgba(255, 255, 255, 0.2); padding: 8px 16px; border-radius: 20px; display: inline-block; margin-top: 10px; font-size: 0.9em; }}
        .content {{ padding: 40px; }}
        .data-source {{ background: #e0e7ff; border: 1px solid #818cf8; padding: 12px 15px; border-radius: 8px; margin: 20px 0; color: #3730a3; font-size: 0.95em; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; text-align: center; box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); transition: transform 0.3s ease; }}
        .metric-card:hover {{ transform: translateY(-5px); }}
        .metric-label {{ font-size: 0.95em; opacity: 0.9; margin-bottom: 10px; font-weight: 500; }}
        .metric-value {{ font-size: 1.8em; font-weight: bold; margin-bottom: 5px; }}
        .metric-subtitle {{ font-size: 0.85em; opacity: 0.8; }}
        .section {{ margin: 40px 0; }}
        .section-title {{ font-size: 1.8em; color: #1e3c72; margin-bottom: 20px; border-left: 5px solid #667eea; padding-left: 15px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; background: #f8f9fa; border-radius: 10px; overflow: hidden; }}
        th {{ background-color: #667eea; color: white; padding: 15px; text-align: left; font-weight: 600; }}
        td {{ padding: 15px; border-bottom: 1px solid #e5e7eb; }}
        tr:hover {{ background-color: #f0f1ff; }}
        tr:last-child td {{ border-bottom: none; }}
        .highlight {{ background-color: #fef3c7; padding: 2px 6px; border-radius: 4px; font-weight: 600; }}
        .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 0.85em; font-weight: 600; }}
        .badge-success {{ background-color: #d1fae5; color: #065f46; }}
        .badge-warning {{ background-color: #fef3c7; color: #92400e; }}
        .badge-info {{ background-color: #dbeafe; color: #1e40af; }}
        .insights-section {{ background: #eff6ff; border-left: 5px solid #3b82f6; padding: 25px; border-radius: 10px; margin: 20px 0; }}
        .insights-title {{ font-size: 1.3em; color: #1e3c72; margin-bottom: 15px; font-weight: 600; }}
        .insights-list {{ list-style: none; padding: 0; }}
        .insights-list li {{ padding: 10px 0; color: #374151; line-height: 1.6; }}
        .insights-list li:before {{ content: "✓ "; color: #3b82f6; font-weight: bold; margin-right: 10px; }}
        .charts-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); gap: 20px; margin: 20px 0; }}
        .chart-container {{ background: #f8f9fa; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); }}
        .chart-title {{ font-size: 1.2em; font-weight: 600; color: #1e3c72; margin-bottom: 15px; }}
        .footer {{ background: #f3f4f6; padding: 20px; text-align: center; color: #6b7280; border-top: 1px solid #e5e7eb; margin-top: 40px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Live Marketing Campaign Dashboard</h1>
            <p>Real-Time Data from Database | All Values in Indian Rupees (Rs.)</p>
            <div class="update-badge">
                🔄 Last Updated: {now}
            </div>
        </div>

        <div class="content">
            <div class="data-source">
                <strong>📁 Data Source:</strong> This dashboard is dynamically generated from actual campaign data in MySQL database.
                Showing all <strong>{total_campaigns} campaigns</strong> directly from the database (no duplicates removed).
            </div>

            <!-- Key Metrics Section -->
            <div class="section">
                <div class="section-title">📈 Key Performance Metrics</div>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">Total Marketing Cost</div>
                        <div class="metric-value">Rs. {total_cost:,.2f}</div>
                        <div class="metric-subtitle">{total_campaigns} campaigns</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Total Revenue Generated</div>
                        <div class="metric-value">Rs. {total_revenue:,.2f}</div>
                        <div class="metric-subtitle">{total_conversions:,.0f} conversions</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Total Profit</div>
                        <div class="metric-value">Rs. {total_profit:,.2f}</div>
                        <div class="metric-subtitle">{(total_profit/total_revenue*100):.1f}% margin</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Average ROI</div>
                        <div class="metric-value">{avg_roi:.2f}%</div>
                        <div class="metric-subtitle">Return on Investment</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Average ROAS</div>
                        <div class="metric-value">{avg_roas:.2f}x</div>
                        <div class="metric-subtitle">Return on Ad Spend</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Average CTR</div>
                        <div class="metric-value">{avg_ctr:.2f}%</div>
                        <div class="metric-subtitle">{total_clicks:,.0f} total clicks</div>
                    </div>
                </div>
            </div>

            <!-- Channel Performance Section -->
            <div class="section">
                <div class="section-title">🎯 Channel Performance Analysis</div>
                <table>
                    <thead>
                        <tr>
                            <th>Marketing Channel</th>
                            <th>Total Cost (Rs.)</th>
                            <th>Total Revenue (Rs.)</th>
                            <th>Profit (Rs.)</th>
                            <th>ROI (%)</th>
                            <th>Conversions</th>
                            <th>Performance</th>
                        </tr>
                    </thead>
                    <tbody>
{channel_rows_html}
                    </tbody>
                </table>
            </div>

            <!-- Insights Section -->
            <div class="insights-section">
                <div class="insights-title">💡 Key Insights (From Actual Database)</div>
                <ul class="insights-list">
                    <li><strong>Top Performer:</strong> {best_channel_name} campaigns deliver the highest ROI at {best_channel_roi:.2f}%, making it the most efficient channel.</li>
                    <li><strong>Revenue Leader:</strong> {highest_revenue_channel} contributes the most revenue at Rs. {highest_revenue_value:,.2f}, accounting for {(highest_revenue_value/total_revenue*100):.1f}% of total revenue.</li>
                    <li><strong>Total Profitability:</strong> Overall campaign profitability stands at Rs. {total_profit:,.2f} with an average ROI of {avg_roi:.2f}%.</li>
                    <li><strong>Conversion Performance:</strong> Total conversions across all channels: {total_conversions:,.0f} with an average CTR of {avg_ctr:.2f}%.</li>
                    <li><strong>Campaign Volume:</strong> Operating across {len(channel_summary)} marketing channels with {total_campaigns} total campaigns in database.</li>
                </ul>
            </div>

            <!-- Visualization Charts -->
            <div class="section">
                <div class="section-title">📊 Visual Analytics</div>
                <div class="charts-grid">
                    <div class="chart-container">
                        <div class="chart-title">ROI by Channel (%)</div>
                        <canvas id="roiChart"></canvas>
                    </div>
                    <div class="chart-container">
                        <div class="chart-title">Revenue Distribution (Rs.)</div>
                        <canvas id="revenueChart"></canvas>
                    </div>
                </div>
                <div class="charts-grid">
                    <div class="chart-container">
                        <div class="chart-title">Cost vs Revenue by Channel (Rs.)</div>
                        <canvas id="costRevenueChart"></canvas>
                    </div>
                    <div class="chart-container">
                        <div class="chart-title">Conversions by Channel</div>
                        <canvas id="conversionChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- Top Campaigns -->
            <div class="section">
                <div class="section-title">🏆 Top Performing Campaigns</div>
                <table>
                    <thead>
                        <tr>
                            <th>Campaign Name</th>
                            <th>Channel</th>
                            <th>Date</th>
                            <th>Cost (Rs.)</th>
                            <th>Revenue (Rs.)</th>
                            <th>ROI (%)</th>
                        </tr>
                    </thead>
                    <tbody>
{campaign_rows_html}
                    </tbody>
                </table>
            </div>

            <!-- Footer -->
            <div class="footer">
                <p><strong>Marketing Campaign Analysis System</strong> | Live Dashboard with Real-Time Database Data</p>
                <p style="margin-top: 10px; font-size: 0.9em;">Data Source: MySQL Database | Total Campaigns: {total_campaigns} | Channels: {len(channel_summary)}</p>
                <p style="margin-top: 10px; font-size: 0.9em;">Last Updated: {now}</p>
            </div>
        </div>
    </div>

    <script>
        // Chart.js visualizations with actual data
        const colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b'];

        // ROI Chart
        new Chart(document.getElementById('roiChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(channel_labels)},
                datasets: [{{
                    label: 'ROI (%)',
                    data: {json.dumps(channel_roi)},
                    backgroundColor: colors,
                    borderRadius: 8
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ position: 'top' }} }},
                scales: {{ y: {{ beginAtZero: true, ticks: {{ callback: v => v + '%' }} }} }}
            }}
        }});

        // Revenue Distribution Chart
        new Chart(document.getElementById('revenueChart'), {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps([f"{l} (Rs. {v:,.0f})" for l, v in zip(channel_labels, channel_revenue)])},
                datasets: [{{
                    data: {json.dumps(channel_revenue)},
                    backgroundColor: colors,
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ position: 'bottom' }},
                    tooltip: {{
                        callbacks: {{
                            label: ctx => {{
                                const total = ctx.dataset.data.reduce((a,b) => a+b, 0);
                                const pct = ((ctx.parsed / total) * 100).toFixed(1);
                                return 'Rs. ' + ctx.parsed.toLocaleString() + ' (' + pct + '%)';
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Cost vs Revenue Chart
        new Chart(document.getElementById('costRevenueChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(channel_labels)},
                datasets: [
                    {{ label: 'Cost (Rs.)', data: {json.dumps(channel_cost)}, backgroundColor: '#ef4444', borderRadius: 8 }},
                    {{ label: 'Revenue (Rs.)', data: {json.dumps(channel_revenue)}, backgroundColor: '#10b981', borderRadius: 8 }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ position: 'top' }} }},
                scales: {{ y: {{ beginAtZero: true, ticks: {{ callback: v => 'Rs. ' + v.toLocaleString() }} }} }}
            }}
        }});

        // Conversion Chart
        new Chart(document.getElementById('conversionChart'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(channel_labels)},
                datasets: [{{
                    label: 'Total Conversions',
                    data: {json.dumps(channel_conversions)},
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ position: 'top' }} }},
                scales: {{ y: {{ beginAtZero: true, ticks: {{ callback: v => v.toLocaleString() }} }} }}
            }}
        }});
    </script>
</body>
</html>
"""
    return html

if __name__ == "__main__":
    main()

