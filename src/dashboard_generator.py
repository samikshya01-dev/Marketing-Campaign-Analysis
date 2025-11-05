"""
Generate live HTML dashboard from campaign data.
"""
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def generate_live_dashboard(config_path='config/config.yaml'):
    """Generate dynamic HTML dashboard from actual data."""
    try:
        import yaml

        # Load config
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        base_path = Path(config_path).parent.parent

        # Load data
        roi_path = base_path / 'data' / 'processed' / 'roi_analysis.csv'
        channel_path = base_path / 'data' / 'processed' / 'channel_performance_summary.csv'

        if not roi_path.exists() or not channel_path.exists():
            logger.warning("Data files not found for dashboard generation")
            return None

        roi_df = pd.read_csv(roi_path)
        channel_df = pd.read_csv(channel_path)

        # Calculate metrics
        metrics = {
            'total_cost': float(roi_df['cost'].sum()),
            'total_revenue': float(roi_df['revenue'].sum()),
            'total_profit': float(roi_df['profit'].sum()),
            'total_conversions': int(roi_df['conversions'].sum()),
            'avg_roi': float(roi_df['roi'].mean()),
            'avg_roas': float(roi_df['roas'].mean()),
            'total_campaigns': len(roi_df),
            'total_clicks': int(roi_df['clicks'].sum()),
            'avg_ctr': float(roi_df['ctr'].mean())
        }

        # Get top campaigns
        top_campaigns = roi_df.nlargest(6, 'roi')[['campaign_name', 'channel', 'date', 'cost', 'revenue', 'roi']]

        # Best performers
        best_channel = channel_df.loc[channel_df['roi'].idxmax()]
        highest_revenue = channel_df.loc[channel_df['revenue'].idxmax()]

        # Prepare data for charts
        channel_labels = channel_df['channel'].tolist()
        channel_revenue = channel_df['revenue'].tolist()
        channel_roi = channel_df['roi'].tolist()
        channel_cost = channel_df['cost'].tolist()
        channel_conversions = channel_df['conversions'].tolist()

        # Generate HTML (keeping the structure but with dynamic data)
        html = generate_dashboard_html(metrics, channel_df, top_campaigns, best_channel,
                                      highest_revenue, channel_labels, channel_revenue,
                                      channel_roi, channel_cost, channel_conversions)

        # Save
        output_path = base_path / 'outputs' / 'dashboards' / 'live_dashboard.html'
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        logger.info(f"Live dashboard generated: {output_path}")
        return str(output_path)

    except Exception as e:
        logger.error(f"Error generating dashboard: {str(e)}")
        return None

def generate_dashboard_html(metrics, channel_df, top_campaigns, best_channel,
                            highest_revenue, channel_labels, channel_revenue,
                            channel_roi, channel_cost, channel_conversions):
    """Generate the HTML content."""

    now = datetime.now().strftime('%B %d, %Y at %I:%M %p')

    # Build channel rows
    channel_rows = ""
    for _, row in channel_df.iterrows():
        roi_val = row['roi']
        if roi_val >= 400:
            performance = '<span class="badge badge-success">⭐⭐⭐⭐⭐ Excellent</span>'
        elif roi_val >= 300:
            performance = '<span class="badge badge-success">⭐⭐⭐⭐ Very Good</span>'
        elif roi_val >= 200:
            performance = '<span class="badge badge-info">⭐⭐⭐ Good</span>'
        else:
            performance = '<span class="badge badge-warning">⭐⭐ Average</span>'

        channel_rows += f"""
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

    # Build campaign rows
    campaign_rows = ""
    for _, campaign in top_campaigns.iterrows():
        campaign_rows += f"""
                        <tr>
                            <td>{campaign['campaign_name']}</td>
                            <td><span class="badge badge-info">{campaign['channel']}</span></td>
                            <td>{campaign['date']}</td>
                            <td>Rs. {campaign['cost']:,.2f}</td>
                            <td>Rs. {campaign['revenue']:,.2f}</td>
                            <td><span class="highlight">{campaign['roi']:.2f}%</span></td>
                        </tr>
"""

    # Return full HTML (using a condensed version for brevity)
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Live Dashboard</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:20px;min-height:100vh}}
.container{{max-width:1400px;margin:0 auto;background:white;border-radius:15px;box-shadow:0 20px 60px rgba(0,0,0,0.3);overflow:hidden}}
.header{{background:linear-gradient(135deg,#1e3c72 0%,#2a5298 100%);color:white;padding:40px;text-align:center}}
.header h1{{font-size:2.5em;margin-bottom:10px}}
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
.badge{{padding:4px 8px;border-radius:4px;font-size:0.85em}}
.badge-success{{background:#d1fae5;color:#065f46}}
.badge-info{{background:#dbeafe;color:#1e40af}}
.badge-warning{{background:#fef3c7;color:#92400e}}
.charts-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(500px,1fr));gap:20px;margin:20px 0}}
.chart-container{{background:#f8f9fa;padding:20px;border-radius:10px}}
.insights{{background:#eff6ff;border-left:5px solid #3b82f6;padding:25px;border-radius:10px;margin:20px 0}}
.footer{{background:#f3f4f6;padding:20px;text-align:center;color:#6b7280;margin-top:40px}}
</style></head><body>
<div class="container">
<div class="header">
<h1>📊 Live Marketing Dashboard</h1>
<p>Real-Time Data | Updated: {now}</p>
</div>
<div class="content">
<div class="section-title">📈 Key Metrics</div>
<div class="metrics-grid">
<div class="metric-card"><div style="font-size:0.9em;opacity:0.9;margin-bottom:10px">Total Cost</div>
<div class="metric-value">Rs. {metrics['total_cost']:,.2f}</div></div>
<div class="metric-card"><div style="font-size:0.9em;opacity:0.9;margin-bottom:10px">Total Revenue</div>
<div class="metric-value">Rs. {metrics['total_revenue']:,.2f}</div></div>
<div class="metric-card"><div style="font-size:0.9em;opacity:0.9;margin-bottom:10px">Total Profit</div>
<div class="metric-value">Rs. {metrics['total_profit']:,.2f}</div></div>
<div class="metric-card"><div style="font-size:0.9em;opacity:0.9;margin-bottom:10px">Average ROI</div>
<div class="metric-value">{metrics['avg_roi']:.2f}%</div></div>
<div class="metric-card"><div style="font-size:0.9em;opacity:0.9;margin-bottom:10px">Average ROAS</div>
<div class="metric-value">{metrics['avg_roas']:.2f}x</div></div>
<div class="metric-card"><div style="font-size:0.9em;opacity:0.9;margin-bottom:10px">Campaigns</div>
<div class="metric-value">{metrics['total_campaigns']}</div></div>
</div>
<div class="section-title">🎯 Channel Performance</div>
<table><thead><tr><th>Channel</th><th>Cost</th><th>Revenue</th><th>Profit</th><th>ROI</th><th>Conversions</th><th>Status</th></tr></thead>
<tbody>{channel_rows}</tbody></table>
<div class="insights">
<strong>💡 Key Insights:</strong><br>
• Top Performer: {best_channel['channel']} with {best_channel['roi']:.2f}% ROI<br>
• Revenue Leader: {highest_revenue['channel']} generating Rs. {highest_revenue['revenue']:,.2f}<br>
• Total Profitability: Rs. {metrics['total_profit']:,.2f} ({metrics['avg_roi']:.2f}% avg ROI)<br>
• Total Conversions: {metrics['total_conversions']:,} across {len(channel_df)} channels
</div>
<div class="section-title">📊 Visual Analytics</div>
<div class="charts-grid">
<div class="chart-container"><canvas id="roiChart"></canvas></div>
<div class="chart-container"><canvas id="revenueChart"></canvas></div>
</div>
<div class="section-title">🏆 Top Campaigns</div>
<table><thead><tr><th>Campaign</th><th>Channel</th><th>Date</th><th>Cost</th><th>Revenue</th><th>ROI</th></tr></thead>
<tbody>{campaign_rows}</tbody></table>
<div class="footer">
<strong>Live Dashboard</strong> | Generated from {metrics['total_campaigns']} campaigns<br>
<small>Data: roi_analysis.csv & channel_performance_summary.csv | {now}</small>
</div>
</div>
</div>
<script>
const colors=['#667eea','#764ba2','#f093fb','#4facfe','#43e97b'];
new Chart(document.getElementById('roiChart'),{{type:'bar',data:{{labels:{json.dumps(channel_labels)},
datasets:[{{label:'ROI (%)',data:{json.dumps(channel_roi)},backgroundColor:colors,borderRadius:8}}]}},
options:{{responsive:true,plugins:{{legend:{{position:'top'}}}},scales:{{y:{{beginAtZero:true}}}}}}}});
new Chart(document.getElementById('revenueChart'),{{type:'doughnut',data:{{
labels:{json.dumps([f"{l} (Rs. {v:,.0f})" for l,v in zip(channel_labels,channel_revenue)])},
datasets:[{{data:{json.dumps(channel_revenue)},backgroundColor:colors,borderWidth:2}}]}},
options:{{responsive:true,plugins:{{legend:{{position:'bottom'}}}}}}}});
</script>
</body></html>"""

if __name__ == "__main__":
    # Standalone execution
    result = generate_live_dashboard()
    if result:
        print(f"✓ Dashboard generated: {result}")
    else:
        print("✗ Dashboard generation failed")

