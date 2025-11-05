"""
ROI calculator module for marketing campaign analysis.
"""
import os
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Dict, List
import yaml
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logger = logging.getLogger(__name__)

class ROICalculator:
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize ROI calculator with configuration."""
        # Handle config path - convert to absolute if relative
        if not os.path.isabs(config_path):
            config_path = os.path.join(Path(__file__).parent.parent, config_path)

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

    def calculate_campaign_roi(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate ROI metrics for campaigns."""
        try:
            df = df.copy()

            # Calculate basic ROI metrics
            df['roi'] = ((df['revenue'] - df['cost']) / df['cost']) * 100
            df['profit'] = df['revenue'] - df['cost']
            df['roas'] = df['revenue'] / df['cost']

            # Calculate efficiency metrics
            df['cpc'] = df['cost'] / df['clicks']
            df['cpa'] = df['cost'] / df['conversions']
            df['conversion_value'] = df['revenue'] / df['conversions']

            # Ensure output directories exist
            os.makedirs(self.config['paths']['processed_data'], exist_ok=True)

            # Save channel performance summary
            channel_summary = self.analyze_channel_performance(df)
            summary_path = os.path.join(self.config['paths']['processed_data'], 'channel_performance_summary.csv')
            channel_summary.to_csv(summary_path)
            logger.info(f"Saved channel performance summary to {summary_path}")

            # Save detailed ROI analysis
            roi_path = os.path.join(self.config['paths']['processed_data'], 'roi_analysis.csv')
            df.to_csv(roi_path, index=False)
            logger.info(f"Saved ROI analysis to {roi_path}")

            return df
        except Exception as e:
            logger.error(f"Error in calculate_campaign_roi: {str(e)}")
            raise

    def analyze_channel_performance(self, df: pd.DataFrame) -> pd.DataFrame:
        """Analyze ROI performance by channel."""
        try:
            channel_metrics = df.groupby('channel').agg({
                'cost': 'sum',
                'revenue': 'sum',
                'conversions': 'sum',
                'profit': 'sum',
                'roi': 'mean',
                'roas': 'mean',
                'impressions': 'sum',
                'clicks': 'sum'
            }).round(2)

            # Calculate channel contribution
            total_profit = channel_metrics['profit'].sum()
            channel_metrics['profit_contribution'] = (channel_metrics['profit'] / total_profit * 100).round(1)

            # Calculate CTR and Conversion Rate
            channel_metrics['ctr'] = (channel_metrics['clicks'] / channel_metrics['impressions'] * 100).round(2)
            channel_metrics['conversion_rate'] = (channel_metrics['conversions'] / channel_metrics['clicks'] * 100).round(2)

            return channel_metrics
        except Exception as e:
            logger.error(f"Error in analyze_channel_performance: {str(e)}")
            raise

    def generate_roi_report(self, df: pd.DataFrame) -> Dict:
        """Generate comprehensive ROI analysis report."""
        try:
            report = {
                'overall_metrics': {
                    'total_cost': df['cost'].sum(),
                    'total_revenue': df['revenue'].sum(),
                    'total_profit': df['profit'].sum(),
                    'overall_roi': df['roi'].mean(),
                    'overall_roas': df['roas'].mean()
                },
                'channel_performance': self.analyze_channel_performance(df).to_dict(),
                'top_campaigns': df.nlargest(5, 'roi')[
                    ['campaign_name', 'channel', 'cost', 'revenue', 'roi']
                ].to_dict('records'),
                'bottom_campaigns': df.nsmallest(5, 'roi')[
                    ['campaign_name', 'channel', 'cost', 'revenue', 'roi']
                ].to_dict('records')
            }

            return report
        except Exception as e:
            logger.error(f"Error in generate_roi_report: {str(e)}")
            raise

    def plot_roi_analysis(self, df: pd.DataFrame, output_dir: str) -> None:
        """Generate ROI analysis visualizations."""
        # Set visualization style - use valid matplotlib style
        style = self.config['visualization'].get('style', 'default')
        valid_styles = ['default', 'seaborn-v0_8', 'ggplot', 'bmh', 'fivethirtyeight']
        if style not in valid_styles:
            style = 'default'

        try:
            plt.style.use(style)
        except:
            plt.style.use('default')

        # ROI by channel
        plt.figure(figsize=self.config['visualization']['figure_size'])
        channel_roi = df.groupby('channel')['roi'].mean().sort_values()
        sns.barplot(x=channel_roi.values, y=channel_roi.index)
        plt.title('Average ROI by Channel')
        plt.xlabel('ROI (%)')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/roi_by_channel.png",
                   dpi=self.config['visualization']['dpi'])
        plt.close()

        # Cost vs Revenue scatter
        plt.figure(figsize=self.config['visualization']['figure_size'])
        plt.scatter(df['cost'], df['revenue'], alpha=0.5)
        plt.xlabel('Cost ($)')
        plt.ylabel('Revenue ($)')
        plt.title('Campaign Cost vs Revenue')

        # Add ROI reference lines
        max_cost = df['cost'].max()
        plt.plot([0, max_cost], [0, max_cost], '--', color='red',
                label='Break Even (ROI = 0%)')
        plt.plot([0, max_cost], [0, 2*max_cost], '--', color='green',
                label='ROI = 100%')

        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{output_dir}/cost_vs_revenue.png",
                   dpi=self.config['visualization']['dpi'])
        plt.close()

        # ROI distribution
        plt.figure(figsize=self.config['visualization']['figure_size'])
        sns.histplot(data=df, x='roi', bins=30)
        plt.title('ROI Distribution')
        plt.xlabel('ROI (%)')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/roi_distribution.png",
                   dpi=self.config['visualization']['dpi'])
        plt.close()

    def export_summary(self, df: pd.DataFrame, output_path: str) -> None:
        """Export ROI analysis summary to CSV."""
        # Prepare summary data
        summary = pd.DataFrame({
            'metric': [
                'Total Cost',
                'Total Revenue',
                'Total Profit',
                'Average ROI',
                'Average ROAS',
                'Best Performing Channel',
                'Worst Performing Channel'
            ],
            'value': [
                f"${df['cost'].sum():,.2f}",
                f"${df['revenue'].sum():,.2f}",
                f"${df['profit'].sum():,.2f}",
                f"{df['roi'].mean():.1f}%",
                f"{df['roas'].mean():.2f}",
                df.groupby('channel')['roi'].mean().idxmax(),
                df.groupby('channel')['roi'].mean().idxmin()
            ]
        })

        # Export to CSV
        summary.to_csv(output_path, index=False)

    def validate_data(self, df: pd.DataFrame) -> bool:
        """Validate input data for ROI calculations."""
        required_columns = ['campaign_name', 'channel', 'cost', 'revenue', 'impressions', 'clicks', 'conversions']

        if df.empty:
            raise ValueError("Input DataFrame is empty")

        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        if (df['cost'] <= 0).any():
            raise ValueError("Found campaigns with zero or negative cost")

        if (df['revenue'] < 0).any():
            raise ValueError("Found campaigns with negative revenue")

        return True

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)

    # Example usage
    from data_loader import DataLoader
    from data_cleaner import DataCleaner

    # Load and clean data
    loader = DataLoader()
    cleaner = DataCleaner()

    campaigns_df = cleaner.clean_campaign_data(loader.load_campaigns())

    # Calculate ROI metrics
    calculator = ROICalculator()

    # Validate data before processing
    if calculator.validate_data(campaigns_df):
        roi_df = calculator.calculate_campaign_roi(campaigns_df)
        report = calculator.generate_roi_report(roi_df)
        print("\nROI Analysis Report:")
        print(f"Overall ROI: {report['overall_metrics']['overall_roi']:.1f}%")
        print(f"Total Profit: ${report['overall_metrics']['total_profit']:,.2f}")
