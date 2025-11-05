#!/usr/bin/env python3
"""Test PDF generation directly"""
import sys
import os

sys.path.insert(0, '/Users/biswajitsahu/Desktop/marketing-campaign-analysis/marketing-campaign-analysis')

print("=" * 60)
print("PDF GENERATION TEST")
print("=" * 60)

# Test 1: Check if reportlab is available
print("\n1. Checking if reportlab is available...")
try:
    import reportlab
    print(f"   ✓ reportlab version: {reportlab.__version__}")
except ImportError as e:
    print(f"   ✗ reportlab not found: {e}")
    sys.exit(1)

# Test 2: Check correct imports
print("\n2. Testing reportlab imports...")
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, white
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    print("   ✓ All imports successful")
except ImportError as e:
    print(f"   ✗ Import failed: {e}")
    sys.exit(1)

# Test 3: Initialize generator
print("\n3. Initializing ExecutiveSummaryGenerator...")
try:
    from src.generate_executive_summary import ExecutiveSummaryGenerator
    gen = ExecutiveSummaryGenerator()
    print("   ✓ Generator initialized")
except Exception as e:
    print(f"   ✗ Failed to initialize: {e}")
    sys.exit(1)

# Test 4: Generate PDF
print("\n4. Generating PDF...")
try:
    pdf_path = gen.generate_pdf()
    if os.path.exists(pdf_path):
        size = os.path.getsize(pdf_path)
        print(f"   ✓ PDF generated successfully")
        print(f"   Location: {pdf_path}")
        print(f"   Size: {size:,} bytes")
    else:
        print(f"   ✗ PDF file not found at: {pdf_path}")
except Exception as e:
    print(f"   ✗ PDF generation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Generate HTML
print("\n5. Generating HTML...")
try:
    html_path = gen.generate_html_report()
    if os.path.exists(html_path):
        size = os.path.getsize(html_path)
        print(f"   ✓ HTML generated successfully")
        print(f"   Location: {html_path}")
        print(f"   Size: {size:,} bytes")
    else:
        print(f"   ✗ HTML file not found at: {html_path}")
except Exception as e:
    print(f"   ✗ HTML generation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED!")
print("=" * 60)

