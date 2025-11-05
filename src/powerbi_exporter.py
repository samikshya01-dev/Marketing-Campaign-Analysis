"""
Power BI data export module.
Prepares cleaned data in optimized format for Power BI import.
"""
import logging
import os
import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class PowerBIExporter:
    """Export data to Power BI compatible formats."""

    def __init__(self, output_dir: str):
        """
        Initialize Power BI exporter.

        Args:
            output_dir: Directory to export Power BI files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.dashboards_dir = self.output_dir / "dashboards"
        self.dashboards_dir.mkdir(parents=True, exist_ok=True)

    def export_campaign_data(self, campaign_df: pd.DataFrame) -> str:
        """
        Export campaign data for Power BI import.

        Args:
            campaign_df: Campaign data DataFrame

        Returns:
            Path to exported file
        """
        try:
            # Add calculated columns for Power BI
            campaign_df = self._add_powerbi_columns(campaign_df, 'campaign')

            # Export to CSV
            output_path = self.dashboards_dir / "campaign_data_powerbi.csv"
            campaign_df.to_csv(output_path, index=False)

            logger.info(f"Campaign data exported to Power BI format: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Error exporting campaign data: {str(e)}")
            raise

    def export_customer_data(self, customer_df: pd.DataFrame) -> str:
        """
        Export customer segmentation data for Power BI.

        Args:
            customer_df: Customer segmentation DataFrame

        Returns:
            Path to exported file
        """
        try:
            # Add calculated columns
            customer_df = self._add_powerbi_columns(customer_df, 'customer')

            # Export to CSV
            output_path = self.dashboards_dir / "customer_segments_powerbi.csv"
            customer_df.to_csv(output_path, index=False)

            logger.info(f"Customer data exported to Power BI format: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Error exporting customer data: {str(e)}")
            raise

    def export_roi_analysis(self, roi_df: pd.DataFrame) -> str:
        """
        Export ROI analysis data for Power BI.

        Args:
            roi_df: ROI analysis DataFrame

        Returns:
            Path to exported file
        """
        try:
            # Format currency columns
            currency_cols = ['revenue', 'cost', 'roi_amount']
            for col in currency_cols:
                if col in roi_df.columns:
                    roi_df[col] = roi_df[col].astype(float)

            # Export to CSV
            output_path = self.dashboards_dir / "roi_analysis_powerbi.csv"
            roi_df.to_csv(output_path, index=False)

            logger.info(f"ROI analysis exported to Power BI format: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Error exporting ROI data: {str(e)}")
            raise

    def export_channel_performance(self, channel_df: pd.DataFrame) -> str:
        """
        Export channel performance summary for Power BI.

        Args:
            channel_df: Channel performance DataFrame

        Returns:
            Path to exported file
        """
        try:
            # Add channel-level metrics
            channel_df = self._calculate_channel_metrics(channel_df)

            # Export to CSV
            output_path = self.dashboards_dir / "channel_performance_powerbi.csv"
            channel_df.to_csv(output_path, index=False)

            logger.info(f"Channel performance exported to Power BI format: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Error exporting channel performance: {str(e)}")
            raise

    def _add_powerbi_columns(self, df: pd.DataFrame, data_type: str) -> pd.DataFrame:
        """
        Add calculated columns needed for Power BI visualizations.

        Args:
            df: DataFrame to enhance
            data_type: Type of data ('campaign', 'customer', etc.)

        Returns:
            Enhanced DataFrame
        """
        df = df.copy()

        # Add timestamp for Power BI refresh tracking
        df['PowerBI_UpdateTime'] = datetime.now().isoformat()

        if data_type == 'campaign':
            # Add ROI category
            if 'roi_percentage' in df.columns:
                df['ROI_Category'] = pd.cut(
                    df['roi_percentage'],
                    bins=[-np.inf, 0, 50, 100, np.inf],
                    labels=['Loss', 'Low', 'Medium', 'High']
                )

            # Add revenue tier
            if 'revenue' in df.columns:
                df['Revenue_Tier'] = pd.qcut(
                    df['revenue'].rank(method='first'),
                    q=4,
                    labels=['Low', 'Medium', 'High', 'Very High'],
                    duplicates='drop'
                )

            # Add conversion rate category
            if 'conversion_rate' in df.columns:
                df['Conversion_Category'] = pd.cut(
                    df['conversion_rate'],
                    bins=[0, 2, 5, 10, 100],
                    labels=['Very Low', 'Low', 'Medium', 'High'],
                    include_lowest=True
                )

        elif data_type == 'customer':
            # Add customer value category
            if 'revenue' in df.columns:
                df['Customer_Value'] = pd.qcut(
                    df['revenue'].rank(method='first'),
                    q=3,
                    labels=['Low', 'Medium', 'High'],
                    duplicates='drop'
                )

            # Add engagement level
            if 'avg_session_duration' in df.columns:
                df['Engagement_Level'] = pd.cut(
                    df['avg_session_duration'],
                    bins=[0, 60, 180, 300, np.inf],
                    labels=['Low', 'Medium', 'High', 'Very High'],
                    include_lowest=True
                )

        return df

    def _calculate_channel_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate additional channel-level metrics for Power BI.

        Args:
            df: Channel data DataFrame

        Returns:
            Enhanced DataFrame with metrics
        """
        df = df.copy()

        # Calculate market share
        if 'revenue' in df.columns:
            total_revenue = df['revenue'].sum()
            df['Revenue_Market_Share_%'] = (df['revenue'] / total_revenue * 100).round(2)

        # Calculate conversion efficiency
        if 'conversions' in df.columns and 'sessions' in df.columns:
            df['Conversion_Efficiency'] = (df['conversions'] / df['sessions'] * 100).round(2)

        # Calculate revenue per user
        if 'revenue' in df.columns and 'users' in df.columns:
            df['Revenue_Per_User'] = (df['revenue'] / df['users']).round(2)

        # Add performance ranking
        if 'revenue' in df.columns:
            df['Revenue_Rank'] = df['revenue'].rank(ascending=False).astype(int)

        return df

    def generate_powerbi_metadata(self) -> str:
        """
        Generate Power BI metadata JSON file.

        Returns:
            Path to metadata file
        """
        try:
            metadata = {
                "dashboard_name": "Marketing Campaign Analysis",
                "version": "1.0.0",
                "created_date": datetime.now().isoformat(),
                "data_sources": [
                    {
                        "name": "Campaign Data",
                        "file": "campaign_data_powerbi.csv",
                        "type": "CSV",
                        "update_frequency": "Daily"
                    },
                    {
                        "name": "Customer Segments",
                        "file": "customer_segments_powerbi.csv",
                        "type": "CSV",
                        "update_frequency": "Weekly"
                    },
                    {
                        "name": "ROI Analysis",
                        "file": "roi_analysis_powerbi.csv",
                        "type": "CSV",
                        "update_frequency": "Daily"
                    },
                    {
                        "name": "Channel Performance",
                        "file": "channel_performance_powerbi.csv",
                        "type": "CSV",
                        "update_frequency": "Daily"
                    }
                ],
                "pages": [
                    {
                        "name": "Executive Summary",
                        "description": "High-level KPIs and trends"
                    },
                    {
                        "name": "Channel Analysis",
                        "description": "Channel performance and ROI comparison"
                    },
                    {
                        "name": "Customer Insights",
                        "description": "Customer segmentation and behavior analysis"
                    },
                    {
                        "name": "Conversion Funnel",
                        "description": "Funnel analysis and drop-off rates"
                    },
                    {
                        "name": "Trend Analysis",
                        "description": "Weekly and monthly trends"
                    }
                ],
                "key_measures": [
                    {
                        "name": "Total Revenue",
                        "formula": "SUM(Campaign[revenue])",
                        "format": "Currency"
                    },
                    {
                        "name": "Total Conversions",
                        "formula": "SUM(Campaign[conversions])",
                        "format": "Number"
                    },
                    {
                        "name": "Conversion Rate",
                        "formula": "DIVIDE(SUM(Campaign[conversions]), SUM(Campaign[sessions])) * 100",
                        "format": "Percentage"
                    },
                    {
                        "name": "Average ROI",
                        "formula": "AVERAGE(Campaign[roi_percentage])",
                        "format": "Percentage"
                    }
                ]
            }

            output_path = self.dashboards_dir / "powerbi_metadata.json"
            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=2)

            logger.info(f"Power BI metadata generated: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Error generating Power BI metadata: {str(e)}")
            raise

    def export_all(self, campaign_df: pd.DataFrame, customer_df: pd.DataFrame,
                   roi_df: pd.DataFrame, channel_df: pd.DataFrame) -> dict:
        """
        Export all data for Power BI in one call.

        Args:
            campaign_df: Campaign data
            customer_df: Customer data
            roi_df: ROI analysis data
            channel_df: Channel performance data

        Returns:
            Dictionary with all export paths
        """
        try:
            logger.info("Starting Power BI data export...")

            exports = {
                "campaign_data": self.export_campaign_data(campaign_df),
                "customer_segments": self.export_customer_data(customer_df),
                "roi_analysis": self.export_roi_analysis(roi_df),
                "channel_performance": self.export_channel_performance(channel_df),
                "metadata": self.generate_powerbi_metadata()
            }

            logger.info("Power BI data export completed successfully")
            return exports
        except Exception as e:
            logger.error(f"Error in Power BI export: {str(e)}")
            raise

