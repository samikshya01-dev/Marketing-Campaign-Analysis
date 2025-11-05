#!/usr/bin/env python3
"""Test PDF generation"""
import sys
sys.path.insert(0, 'src')

from generate_executive_summary import ExecutiveSummaryGenerator

try:
    print("Creating generator...")
    generator = ExecutiveSummaryGenerator()

    print("Generating PDF...")
    pdf_path = generator.generate_pdf()
    print(f"✓ PDF generated successfully: {pdf_path}")

    print("Generating HTML...")
    html_path = generator.generate_html_report()
    print(f"✓ HTML generated successfully: {html_path}")

except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()

