"""
EDA module for marketing campaign analysis.
"""
import os
from pathlib import Path
from typing import Optional, Tuple, List
import warnings

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import yaml
from pandas.api.types import CategoricalDtype



class EDAAnalyzer:
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize EDA analyzer with configuration."""
        # Handle config path - convert to absolute if relative
        if not os.path.isabs(config_path):
            config_path = os.path.join(Path(__file__).parent.parent, config_path)

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Set visualization style - use valid matplotlib style
        style = self.config['visualization'].get('style', 'default')
        valid_styles = ['default', 'seaborn-v0_8', 'ggplot', 'bmh', 'fivethirtyeight']
        if style not in valid_styles:
            style = 'default'

        try:
            plt.style.use(style)
        except:
            plt.style.use('default')

        self.colors = sns.color_palette(self.config['visualization'].get('color_palette', 'husl'))

        # Suppress warnings
        warnings.filterwarnings('ignore', category=FutureWarning)

    def plot_campaign_performance(self, df: pd.DataFrame, output_dir: str) -> None:
        """Generate campaign performance visualizations."""
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Convert channel to categorical for better plotting
        df['channel'] = pd.Categorical(df['channel'])

        # Plot ROI by channel
        self._plot_roi_by_channel(df, output_path / 'roi_by_channel.png')

        # Plot conversion funnel
        self._plot_conversion_funnel(df, output_path / 'conversion_funnel.png')

        # Plot channel metrics
        self._plot_channel_metrics(df, output_path / 'channel_metrics.png')

        # Plot time series
        self._plot_time_series(df, output_path / 'time_series.png')

    def _plot_roi_by_channel(self, df: pd.DataFrame, output_path: Path) -> None:
        """Plot ROI analysis by channel."""
        plt.figure(figsize=self.config['visualization']['figure_size'])

        channel_roi = df.groupby('channel')['roi'].mean().sort_values(ascending=True)

        # Use newer seaborn API
        ax = sns.barplot(data=df, x='roi', y='channel', estimator='mean', errorbar=None)
        plt.title('Average ROI by Channel')
        plt.xlabel('ROI (%)')
        plt.ylabel('Channel')

        plt.tight_layout()
        plt.savefig(output_path, dpi=self.config['visualization']['dpi'])
        plt.close()

    def _plot_conversion_funnel(self, df: pd.DataFrame, output_path: Path) -> None:
        """Plot conversion funnel visualization."""
        plt.figure(figsize=self.config['visualization']['figure_size'])

        metrics = ['impressions', 'clicks', 'conversions']
        values = [df[metric].sum() for metric in metrics]

        plt.bar(metrics, values, color=self.colors)
        plt.title('Conversion Funnel')
        plt.ylabel('Count')

        # Add conversion rates
        for i in range(len(metrics)-1):
            rate = (values[i+1] / values[i]) * 100
            plt.text(i+0.5, (values[i] + values[i+1])/2,
                    f'{rate:.1f}%', ha='center')

        plt.tight_layout()
        plt.savefig(output_path, dpi=self.config['visualization']['dpi'])
        plt.close()

    def _plot_channel_metrics(self, df: pd.DataFrame, output_path: Path) -> None:
        """Plot channel performance metrics."""
        plt.figure(figsize=self.config['visualization']['figure_size'])

        metrics = ['ctr', 'conversion_rate', 'roi']
        channel_metrics = df.groupby('channel')[metrics].mean()

        ax = channel_metrics.plot(kind='bar', width=0.8)
        plt.title('Channel Performance Metrics')
        plt.xlabel('Channel')
        plt.ylabel('Percentage (%)')
        plt.legend(title='Metric', bbox_to_anchor=(1.05, 1))

        plt.tight_layout()
        plt.savefig(output_path, dpi=self.config['visualization']['dpi'])
        plt.close()

    def _plot_time_series(self, df: pd.DataFrame, output_path: Path) -> None:
        """Plot time series analysis of campaign performance."""
        plt.figure(figsize=self.config['visualization']['figure_size'])

        # Group by date and calculate daily metrics
        daily_metrics = df.groupby('date').agg({
            'revenue': 'sum',
            'conversions': 'sum',
            'roi': 'mean'
        }).reset_index()

        # Plot revenue and ROI trends
        fig, ax1 = plt.subplots(figsize=self.config['visualization']['figure_size'])

        ax1.set_xlabel('Date')
        ax1.set_ylabel('Revenue ($)', color=self.colors[0])
        ax1.plot(daily_metrics['date'], daily_metrics['revenue'],
                color=self.colors[0], label='Revenue')
        ax1.tick_params(axis='y', labelcolor=self.colors[0])

        ax2 = ax1.twinx()
        ax2.set_ylabel('ROI (%)', color=self.colors[1])
        ax2.plot(daily_metrics['date'], daily_metrics['roi'],
                color=self.colors[1], label='ROI')
        ax2.tick_params(axis='y', labelcolor=self.colors[1])

        plt.title('Daily Revenue and ROI Trends')
        fig.tight_layout()
        plt.savefig(output_path, dpi=self.config['visualization']['dpi'])
        plt.close()

    def generate_eda_report(self, df: pd.DataFrame) -> dict:
        """Generate EDA summary statistics."""
        return {
            'summary_stats': df.describe().to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'channel_performance': df.groupby('channel').agg({
                'impressions': 'sum',
                'clicks': 'sum',
                'conversions': 'sum',
                'revenue': 'sum',
                'roi': 'mean'
            }).to_dict()
        }


if __name__ == "__main__":
    # Example usage
    from data_loader import DataLoader
    from data_cleaner import DataCleaner

    # Load and clean data
    loader = DataLoader()
    cleaner = DataCleaner()

    campaigns_df = cleaner.clean_campaign_data(loader.load_campaigns())

    # Perform EDA
    analyzer = EDAAnalyzer()
    analyzer.plot_campaign_performance(campaigns_df, "outputs/visualizations")

    # Generate report
    report = analyzer.generate_eda_report(campaigns_df)
    print("EDA analysis completed. Check outputs/visualizations/ for plots.")
