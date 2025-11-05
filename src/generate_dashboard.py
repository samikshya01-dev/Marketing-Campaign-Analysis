#!/usr/bin/env python3
"""
Generate dynamic HTML dashboard from actual campaign data.
This script reads the processed data and creates an interactive dashboard.
"""
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

def load_data():
    """Load processed campaign data."""
    base_path = Path(__file__).parent

    # Load ROI analysis
    roi_path = base_path / 'data' / 'processed' / 'roi_analysis.csv'
    roi_df = pd.read_csv(roi_path)

    # Load channel performance
    channel_path = base_path / 'data' / 'processed' / 'channel_performance_summary.csv'
    channel_df = pd.read_csv(channel_path)

    return roi_df, channel_df

def calculate_metrics(roi_df, channel_df):
    """Calculate key metrics from data."""
    metrics = {
        'total_cost': roi_df['cost'].sum(),
        'total_revenue': roi_df['revenue'].sum(),
        'total_profit': roi_df['profit'].sum(),
        'total_conversions': roi_df['conversions'].sum(),
        'avg_roi': roi_df['roi'].mean(),
        'avg_roas': roi_df['roas'].mean(),
        'total_campaigns': len(roi_df),
        'total_impressions': roi_df['impressions'].sum(),
        'total_clicks': roi_df['clicks'].sum(),
        'avg_ctr': roi_df['ctr'].mean()
    }
    return metrics

def generate_html_dashboard(roi_df, channel_df, metrics):
    """Generate HTML dashboard with actual data."""

    # Get top campaigns
    top_campaigns = roi_df.nlargest(6, 'roi')[['campaign_name', 'channel', 'date', 'cost', 'revenue', 'roi']]

    # Prepare channel data for charts
    channel_labels = channel_df['channel'].tolist()
    channel_revenue = channel_df['revenue'].tolist()
    channel_roi = channel_df['roi'].tolist()
    channel_conversions = channel_df['conversions'].tolist()

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Marketing Campaign Analysis - Live Dashboard</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
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
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .update-badge {{
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 20px;
            display: inline-block;
            margin-top: 10px;
            font-size: 0.9em;
        }}
        .content {{
            padding: 40px;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            transition: transform 0.3s ease;
        }}
        .metric-card:hover {{
            transform: translateY(-5px);
        }}
        .metric-label {{
            font-size: 0.95em;
            opacity: 0.9;
            margin-bottom: 10px;
            font-weight: 500;
        }}
        .metric-value {{
            font-size: 1.8em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .metric-subtitle {{
            font-size: 0.85em;
            opacity: 0.8;
        }}
        .section {{
            margin: 40px 0;
        }}
        .section-title {{
            font-size: 1.8em;
            color: #1e3c72;
            margin-bottom: 20px;
            border-left: 5px solid #667eea;
            padding-left: 15px;
        }}
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .chart-container {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        .chart-title {{
            font-size: 1.2em;
            font-weight: 600;
            color: #1e3c72;
            margin-bottom: 15px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: #f8f9fa;
            border-radius: 10px;
            overflow: hidden;
        }}
        th {{
            background-color: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 15px;
            border-bottom: 1px solid #e5e7eb;
        }}
        tr:hover {{
            background-color: #f0f1ff;
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
        .highlight {{
            background-color: #fef3c7;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: 600;
        }}
        .badge {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        .badge-success {{
            background-color: #d1fae5;
            color: #065f46;
        }}
        .badge-warning {{
            background-color: #fef3c7;
            color: #92400e;
        }}
        .badge-info {{
            background-color: #dbeafe;
            color: #1e40af;
        }}
        .insights-section {{
            background: #eff6ff;
            border-left: 5px solid #3b82f6;
            padding: 25px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        .insights-title {{
            font-size: 1.3em;
            color: #1e3c72;
            margin-bottom: 15px;
            font-weight: 600;
        }}
        .insights-list {{
            list-style: none;
            padding: 0;
        }}
        .insights-list li {{
            padding: 10px 0;
            color: #374151;
            line-height: 1.6;
        }}
        .insights-list li:before {{
            content: "✓ ";
            color: #3b82f6;
            font-weight: bold;
            margin-right: 10px;
        }}
        .footer {{
            background: #f3f4f6;
            padding: 20px;
            text-align: center;
            color: #6b7280;
            border-top: 1px solid #e5e7eb;
            margin-top: 40px;
        }}
        .data-source {{
            background: #e0e7ff;
            border: 1px solid #818cf8;
            padding: 12px 15px;
            border-radius: 8px;
            margin: 20px 0;
            color: #3730a3;
            font-size: 0.95em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Marketing Campaign Analysis Dashboard</h1>
            <p>Live Data Dashboard - All Values in Indian Rupees (Rs.)</p>
            <div class="update-badge">
                🔄 Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </div>
        </div>

        <div class="content">
            <div class="data-source">
                <strong>📁 Data Source:</strong> This dashboard is dynamically generated from actual campaign data stored in <code>data/processed/roi_analysis.csv</code> and <code>channel_performance_summary.csv</code>. All metrics reflect real campaign performance.
            </div>

            <!-- Key Metrics Section -->
            <div class="section">
                <div class="section-title">📈 Key Performance Metrics</div>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">Total Marketing Cost</div>
                        <div class="metric-value">Rs. {metrics['total_cost']:,.2f}</div>
                        <div class="metric-subtitle">{metrics['total_campaigns']} campaigns</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Total Revenue Generated</div>
                        <div class="metric-value">Rs. {metrics['total_revenue']:,.2f}</div>
                        <div class="metric-subtitle">{metrics['total_conversions']:,.0f} conversions</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Total Profit</div>
                        <div class="metric-value">Rs. {metrics['total_profit']:,.2f}</div>
                        <div class="metric-subtitle">{(metrics['total_profit']/metrics['total_revenue']*100):.1f}% margin</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Average ROI</div>
                        <div class="metric-value">{metrics['avg_roi']:.2f}%</div>
                        <div class="metric-subtitle">Return on Investment</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Average ROAS</div>
                        <div class="metric-value">{metrics['avg_roas']:.2f}x</div>
                        <div class="metric-subtitle">Return on Ad Spend</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Average CTR</div>
                        <div class="metric-value">{metrics['avg_ctr']:.2f}%</div>
                        <div class="metric-subtitle">{metrics['total_clicks']:,.0f} total clicks</div>
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
"""

    # Add channel rows
    for _, row in channel_df.iterrows():
        # Determine performance badge
        roi_val = row['roi']
        if roi_val >= 400:
            performance = '<span class="badge badge-success">⭐⭐⭐⭐⭐ Excellent</span>'
        elif roi_val >= 300:
            performance = '<span class="badge badge-success">⭐⭐⭐⭐ Very Good</span>'
        elif roi_val >= 200:
            performance = '<span class="badge badge-info">⭐⭐⭐ Good</span>'
        else:
            performance = '<span class="badge badge-warning">⭐⭐ Average</span>'

        html_content += f"""
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

    # Find best and worst performers
    best_channel = channel_df.loc[channel_df['roi'].idxmax()]
    worst_channel = channel_df.loc[channel_df['roi'].idxmin()]
    highest_revenue = channel_df.loc[channel_df['revenue'].idxmax()]

    html_content += f"""
                    </tbody>
                </table>
            </div>

            <!-- Insights Section -->
            <div class="insights-section">
                <div class="insights-title">💡 Key Insights (From Actual Data)</div>
                <ul class="insights-list">
                    <li><strong>Top Performer:</strong> {best_channel['channel']} campaigns deliver the highest ROI at {best_channel['roi']:.2f}%, making it the most efficient channel.</li>
                    <li><strong>Revenue Leader:</strong> {highest_revenue['channel']} contributes the most revenue at Rs. {highest_revenue['revenue']:,.2f}, accounting for {(highest_revenue['revenue']/metrics['total_revenue']*100):.1f}% of total revenue.</li>
                    <li><strong>Total Profitability:</strong> Overall campaign profitability stands at Rs. {metrics['total_profit']:,.2f} with an average ROI of {metrics['avg_roi']:.2f}%.</li>
                    <li><strong>Conversion Performance:</strong> Total conversions across all channels: {metrics['total_conversions']:,.0f} with an average CTR of {metrics['avg_ctr']:.2f}%.</li>
                    <li><strong>Channel Distribution:</strong> Operating across {len(channel_df)} marketing channels with {metrics['total_campaigns']} total campaigns.</li>
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
"""

    # Add top campaign rows
    for _, campaign in top_campaigns.iterrows():
        html_content += f"""
                        <tr>
                            <td>{campaign['campaign_name']}</td>
                            <td><span class="badge badge-info">{campaign['channel']}</span></td>
                            <td>{campaign['date']}</td>
                            <td>Rs. {campaign['cost']:,.2f}</td>
                            <td>Rs. {campaign['revenue']:,.2f}</td>
                            <td><span class="highlight">{campaign['roi']:.2f}%</span></td>
                        </tr>
"""

    html_content += f"""
                    </tbody>
                </table>
            </div>

            <!-- Footer -->
            <div class="footer">
                <p><strong>Marketing Campaign Analysis System</strong> | Dynamic Dashboard with Real-Time Data</p>
                <p style="margin-top: 10px; font-size: 0.9em;">Generated from: <code>data/processed/roi_analysis.csv</code> ({len(roi_df)} campaigns) and <code>channel_performance_summary.csv</code> ({len(channel_df)} channels)</p>
                <p style="margin-top: 10px; font-size: 0.9em;">Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                <p style="margin-top: 15px; color: #9ca3af; font-size: 0.85em;">
                    For detailed insights: <code>outputs/reports/executive_summary.html</code> | 
                    Run: <code>./run_analysis.sh</code> to refresh data
                </p>
            </div>
        </div>
    </div>

    <script>
        // Prepare data from Python
        const channelLabels = {json.dumps(channel_labels)};
        const channelRevenue = {json.dumps(channel_revenue)};
        const channelROI = {json.dumps(channel_roi)};
        const channelCost = {json.dumps(channel_df['cost'].tolist())};
        const channelConversions = {json.dumps(channel_conversions)};

        // Color palette
        const colors = [
            '#667eea',
            '#764ba2',
            '#f093fb',
            '#4facfe',
            '#43e97b'
        ];

        // ROI Chart
        const roiCtx = document.getElementById('roiChart').getContext('2d');
        new Chart(roiCtx, {{
            type: 'bar',
            data: {{
                labels: channelLabels,
                datasets: [{{
                    label: 'ROI (%)',
                    data: channelROI,
                    backgroundColor: colors,
                    borderRadius: 8,
                    borderSkipped: false
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top'
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return context.dataset.label + ': ' + context.parsed.y.toFixed(2) + '%';
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return value + '%';
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Revenue Distribution Chart
        const revenueCtx = document.getElementById('revenueChart').getContext('2d');
        new Chart(revenueCtx, {{
            type: 'doughnut',
            data: {{
                labels: channelLabels.map((label, i) => label + ' (Rs. ' + channelRevenue[i].toLocaleString() + ')'),
                datasets: [{{
                    data: channelRevenue,
                    backgroundColor: colors,
                    borderColor: '#fff',
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'bottom'
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return 'Rs. ' + context.parsed.toLocaleString() + ' (' + percentage + '%)';
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Cost vs Revenue Chart
        const costRevenueCtx = document.getElementById('costRevenueChart').getContext('2d');
        new Chart(costRevenueCtx, {{
            type: 'bar',
            data: {{
                labels: channelLabels,
                datasets: [
                    {{
                        label: 'Cost (Rs.)',
                        data: channelCost,
                        backgroundColor: '#ef4444',
                        borderRadius: 8
                    }},
                    {{
                        label: 'Revenue (Rs.)',
                        data: channelRevenue,
                        backgroundColor: '#10b981',
                        borderRadius: 8
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top'
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return context.dataset.label + ': Rs. ' + context.parsed.y.toLocaleString();
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return 'Rs. ' + value.toLocaleString();
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Conversion Chart
        const conversionCtx = document.getElementById('conversionChart').getContext('2d');
        new Chart(conversionCtx, {{
            type: 'line',
            data: {{
                labels: channelLabels,
                datasets: [{{
                    label: 'Total Conversions',
                    data: channelConversions,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top'
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return 'Conversions: ' + context.parsed.y.toLocaleString();
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return value.toLocaleString();
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

    return html_content

def main():
    """Main execution function."""
    print("🔄 Generating dynamic dashboard from actual campaign data...")

    # Load data
    roi_df, channel_df = load_data()
    print(f"✓ Loaded {len(roi_df)} campaigns and {len(channel_df)} channels")

    # Calculate metrics
    metrics = calculate_metrics(roi_df, channel_df)
    print(f"✓ Calculated metrics: Total Revenue = Rs. {metrics['total_revenue']:,.2f}")

    # Generate HTML
    html_content = generate_html_dashboard(roi_df, channel_df, metrics)

    # Save to file
    output_path = Path(__file__).parent / 'outputs' / 'dashboards' / 'live_dashboard.html'
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✓ Dashboard generated: {output_path}")
    print(f"\n📊 Dashboard Stats:")
    print(f"  • Total Campaigns: {metrics['total_campaigns']}")
    print(f"  • Total Cost: Rs. {metrics['total_cost']:,.2f}")
    print(f"  • Total Revenue: Rs. {metrics['total_revenue']:,.2f}")
    print(f"  • Average ROI: {metrics['avg_roi']:.2f}%")
    print(f"\n💡 Open the dashboard: open {output_path}")

if __name__ == "__main__":
    main()

