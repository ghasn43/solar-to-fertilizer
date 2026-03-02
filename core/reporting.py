"""
PDF report generation using reportlab.
"""
import json
from datetime import datetime
from io import BytesIO
from typing import Dict, Any, List

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.lib import colors
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

from core.constants import COMPANY_NAME, COMPANY_LOCATION, IP_NOTICE
from core.models import ScenarioComparison


def generate_pdf_report(
    scenario: ScenarioComparison,
    config_dict: Dict[str, Any],
    process_results: Dict[str, Any],
    scenarios_comparison: List[Dict[str, str]],
    output_path: str = None,
) -> BytesIO:
    """
    Generate a 1-page PDF report.
    
    Args:
        scenario: Selected scenario
        config_dict: Configuration parameters
        process_results: Process calculation results
        scenarios_comparison: List of scenario comparison dicts
        output_path: Path to save PDF; if None, return BytesIO buffer
    
    Returns:
        BytesIO buffer with PDF content (or None if file saved)
    """
    if not HAS_REPORTLAB:
        raise ImportError("reportlab is required for PDF generation. Install with: pip install reportlab")
    
    # Create buffer or file
    if output_path:
        buffer = open(output_path, 'wb')
    else:
        buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
    )
    
    # Build story
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#003366'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#003366'),
        spaceAfter=4,
        spaceBefore=4,
        fontName='Helvetica-Bold',
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=4,
    )
    
    small_style = ParagraphStyle(
        'CustomSmall',
        parent=styles['Normal'],
        fontSize=7,
        textColor=colors.grey,
        spaceAfter=2,
    )
    
    # Header
    story.append(Paragraph(f"<b>{COMPANY_NAME}</b>", title_style))
    story.append(Paragraph(COMPANY_LOCATION, normal_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("Solar-to-Fertiliser Digital Twin (S2F-DT)", heading_style))
    story.append(Paragraph(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", small_style))
    story.append(Spacer(1, 0.1 * inch))
    
    # Scenario
    story.append(Paragraph(f"<b>Selected Scenario:</b> {scenario.name}", normal_style))
    story.append(Paragraph(f"<b>Description:</b> {scenario.description}", small_style))
    story.append(Spacer(1, 0.08 * inch))
    
    # Key Inputs
    story.append(Paragraph("<b>Configuration Inputs</b>", heading_style))
    input_table_data = [
        ["Parameter", "Value"],
        ["Target NH3 (tons/day)", f"{config_dict.get('target_nh3_day', 'N/A')}"],
        ["Solar Capacity (MW)", f"{config_dict.get('solar_capacity_mw', 'N/A')}"],
        ["Electrolyser Eff. (kWh/kg H2)", f"{config_dict.get('electrolyser_efficiency', 'N/A')}"],
        ["Catalyst Factor", f"{config_dict.get('catalyst_factor', 'N/A')}"],
        ["Capacity Factor", f"{config_dict.get('capacity_factor', 'N/A')}"],
    ]
    input_table = Table(input_table_data, colWidths=[3.5 * inch, 1.5 * inch])
    input_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E6F0FF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(input_table)
    story.append(Spacer(1, 0.08 * inch))
    
    # KPIs
    story.append(Paragraph("<b>Key Performance Indicators</b>", heading_style))
    kpi_table_data = [
        ["metric", "Value"],
        ["NH3 Production (tons/day)", f"{process_results.get('nh3_tons_day', 'N/A'):.2f}"],
        ["Water Requirement (m³/day)", f"{process_results.get('water_m3_day', 'N/A'):.1f}"],
        ["Electricity (kWh/day)", f"{process_results.get('electricity_kwh_day', 'N/A'):.0f}"],
        ["CO2 Intensity (kg CO2/ton)", f"{scenario.co2_kg_per_ton:.1f}"],
        ["Cost (USD/ton NH3)", f"{scenario.cost_usd_per_ton:.0f}"],
    ]
    kpi_table = Table(kpi_table_data, colWidths=[3.5 * inch, 1.5 * inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFE6E6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 0.08 * inch))
    
    # Scenario Comparison
    if scenarios_comparison:
        story.append(Paragraph("<b>Scenario Comparison</b>", heading_style))
        comparison_data = [["Scenario"] + list(scenarios_comparison[0].keys())[1:]] if scenarios_comparison else []
        for sc in scenarios_comparison:
            comparison_data.append(list(sc.values()))
        
        if len(comparison_data) > 1:
            comparison_table = Table(comparison_data, colWidths=[1.5 * inch, 1 * inch, 1 * inch, 1.5 * inch])
            comparison_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E6FFE6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 7),
                ('FONTSIZE', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            story.append(comparison_table)
            story.append(Spacer(1, 0.08 * inch))
    
    # Footer with IP notice
    story.append(Spacer(1, 0.05 * inch))
    story.append(Paragraph(f"<i>{IP_NOTICE}</i>", small_style))
    
    # Build PDF
    doc.build(story)
    
    if output_path:
        buffer.close()
        return None
    else:
        buffer.seek(0)
        return buffer


def export_config_json(
    config_dict: Dict[str, Any],
    process_results: Dict[str, Any],
    scenario_name: str,
    output_path: str = None,
) -> str:
    """
    Export configuration and results as JSON.
    
    Args:
        config_dict: Configuration parameters
        process_results: Process results
        scenario_name: Selected scenario name
        output_path: Path to save JSON; if None, return JSON string
    
    Returns:
        JSON string (or None if file saved)
    """
    export_data = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "company": COMPANY_NAME,
            "application": "Solar-to-Fertiliser Digital Twin (S2F-DT)",
        },
        "scenario": scenario_name,
        "configuration": config_dict,
        "results": process_results,
    }
    
    json_str = json.dumps(export_data, indent=2, default=str)
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(json_str)
        return None
    else:
        return json_str
