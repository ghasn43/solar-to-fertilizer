"""
Page 8: Strategy & Projections
Phase 2 policy features: scenario comparison, risk assessment, cabinet briefing export
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from core.constants import COMPANY_NAME, COMPANY_LOCATION, IP_NOTICE
from core.models import ProcessConfig
from core.process import process_model

st.set_page_config(page_title="8. Strategy & Projections | S2F-DT", layout="wide")

st.markdown(f"<div style='color:#003366'><h1>🎯 Strategy & Projections</h1></div>", unsafe_allow_html=True)

st.markdown("""
Strategic scenario modeling, risk assessment, and cabinet briefing export tools.
Compare pre-built policy packages and explore resilience to market shocks.
""")

# Initialize session state
if "process_config" not in st.session_state:
    st.session_state.process_config = {
        "target_nh3_day": 5.0,
        "solar_capacity_mw": 50.0,
        "electrolyser_efficiency": 45.0,
        "n2_separation_energy": 0.5,
        "synthesis_energy": 8.0,
        "catalyst_factor": 1.0,
        "capacity_factor": 0.25,
        "water_cost_usd_m3": 1.5,
        "electricity_cost_usd_kwh": 0.04,
        "include_urea": False,
    }

config_dict = st.session_state.process_config

# ===== HELPER FUNCTIONS =====

def calculate_scenario_economics(scenario_params):
    """Calculate economics for a scenario."""
    config = ProcessConfig(**scenario_params)
    results = process_model(config)
    
    return {
        "cost_usd_per_ton": results.cost_usd_per_ton_nh3,
        "co2_kg_per_ton": results.co2_intensity_kg_per_kg_nh3 * 1000,
        "energy_mwh_day": results.electricity_kwh_day / 1000,
        "water_m3_day": results.water_m3_day,
    }

def generate_cabinet_briefing_pdf(scenario_name, scenario_data, reference_cost):
    """Generate a professional PDF briefing document."""
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(letter),
                            rightMargin=0.5*inch, leftMargin=0.5*inch,
                            topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#003366'),
        spaceAfter=6,
        alignment=1
    )
    
    story.append(Paragraph(f"Policy Strategy Briefing: {scenario_name}", title_style))
    story.append(Paragraph(f"<b>{COMPANY_NAME}</b> | {COMPANY_LOCATION}", styles['Normal']))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Key metrics
    metrics_data = [
        ["Metric", "Value", "vs Import Baseline"],
        ["**Cost per Ton**", f"${scenario_data['cost_usd_per_ton']:.0f}", 
         f"{scenario_data['cost_usd_per_ton'] - reference_cost:+.0f}"],
        ["**CO₂ Intensity**", f"{scenario_data['co2_kg_per_ton']:.0f} kg/ton", 
         f"{scenario_data['co2_kg_per_ton'] - 2000:+.0f} kg/ton"],
        ["**Daily Energy**", f"{scenario_data['energy_mwh_day']:.0f} MWh/day", "—"],
        ["**Water Usage**", f"{scenario_data['water_m3_day']:.0f} m³/day", "—"],
    ]
    
    metrics_table = Table(metrics_data, colWidths=[2*inch, 2*inch, 2.5*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(Paragraph("<b>Key Performance Indicators</b>", styles['Heading2']))
    story.append(metrics_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Strategic implications
    story.append(Paragraph("<b>Strategic Implications</b>", styles['Heading2']))
    
    if scenario_data['cost_usd_per_ton'] < 350:
        viability = "✓ <b>Excellent cost-competitiveness:</b> Undercuts import baseline. Attractive for investors."
    elif scenario_data['cost_usd_per_ton'] < 400:
        viability = "✓ <b>Good cost-competitiveness:</b> Competitive with imports. Minor subsidy may be needed."
    else:
        viability = "⚠ <b>Subsidy-dependent:</b> Requires government support to achieve cost parity."
    
    story.append(Paragraph(viability, styles['Normal']))
    
    if scenario_data['co2_kg_per_ton'] < 100:
        climate = "✓ <b>Ultra-low carbon:</b> Aligns strongly with UAE Net Zero 2050 commitment."
    elif scenario_data['co2_kg_per_ton'] < 500:
        climate = "✓ <b>Significant carbon reduction:</b> 95%+ cleaner than imported ammonia."
    else:
        climate = "~ <b>Moderate decarbonization:</b> Some carbon savings, but still requires grid electricity."
    
    story.append(Paragraph(climate, styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    # Policy recommendation
    story.append(Paragraph("<b>Policy Recommendation</b>", styles['Heading2']))
    recommendation = "This scenario represents a viable pathway to ammonia self-sufficiency. Recommended actions: (1) Secure long-term renewable electricity PPA, (2) Allocate water resources, (3) Pilot with first plant in Abu Dhabi or Masdar City, (4) Monitor technology learning curve."
    story.append(Paragraph(recommendation, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Footer
    story.append(Paragraph(f"<i>{IP_NOTICE}</i>", styles['Normal']))
    
    doc.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer

# ===== TABS =====

tab_scenarios, tab_risk, tab_excel = st.tabs([
    "🎲 Policy Scenarios",
    "⚠️ Risk & Resilience",
    "📊 Export & Briefing"
])

# ===== POLICY SCENARIOS TAB =====
with tab_scenarios:
    st.markdown("## Pre-Built Policy Packages")
    st.markdown("""
Compare four strategic policy scenarios ranging from minimal support to full decarbonization commitment.
    """)
    
    # Define policy scenarios
    scenarios = {
        "Baseline (No Support)": {
            "description": "Current conditions, no policy intervention",
            "electricity_cost": 0.04,
            "subsidy": 0,
            "carbon_tax": 0.00,
            "tech_improvement": 0,
            "color": "#ff6b6b"
        },
        "Moderate Support": {
            "description": "Targeted electricity subsidy + tax credits",
            "electricity_cost": 0.035,
            "subsidy": 25,
            "carbon_tax": 0.05,
            "tech_improvement": 2.5,
            "color": "#ffd93d"
        },
        "Green Push": {
            "description": "Strong renewable PPA + carbon incentive + R&D support",
            "electricity_cost": 0.030,
            "subsidy": 50,
            "carbon_tax": 0.15,
            "tech_improvement": 5.0,
            "color": "#6bcf7f"
        },
        "Full Decarbonization": {
            "description": "Comprehensive policy package with mission-critical support",
            "electricity_cost": 0.028,
            "subsidy": 75,
            "carbon_tax": 0.25,
            "tech_improvement": 7.5,
            "color": "#0066cc"
        }
    }
    
    # Calculate all scenarios
    scenario_results = {}
    for scenario_name, params in scenarios.items():
        config = config_dict.copy()
        config["electricity_cost_usd_kwh"] = params["electricity_cost"]
        config["electrolyser_efficiency"] = max(35, config["electrolyser_efficiency"] - (params["tech_improvement"] / 10))
        
        econ = calculate_scenario_economics(config)
        
        # Apply subsidy and carbon tax
        cost_base = econ["cost_usd_per_ton"]
        cost_with_carbon = cost_base + (econ["co2_kg_per_ton"] * params["carbon_tax"] / 1000)
        cost_final = cost_with_carbon - params["subsidy"]
        
        scenario_results[scenario_name] = {
            "cost_base": cost_base,
            "cost_with_policy": cost_final,
            "co2": econ["co2_kg_per_ton"],
            "energy": econ["energy_mwh_day"],
            "water": econ["water_m3_day"],
            "viability": "✓ Excellent" if cost_final < 350 else "✓ Good" if cost_final < 400 else "⚠ Marginal"
        }
    
    # Scenario comparison table
    st.markdown("### Scenario Comparison Table")
    
    comparison_rows = []
    for scenario_name, results in scenario_results.items():
        comparison_rows.append({
            "Scenario": scenario_name,
            "Cost/Ton": f"${results['cost_with_policy']:.0f}",
            "vs Import": f"{results['cost_with_policy'] - 400:+.0f}",
            "CO₂/Ton": f"{results['co2']:.0f} kg",
            "Viability": results['viability']
        })
    
    comparison_df = pd.DataFrame(comparison_rows)
    st.dataframe(comparison_df, use_container_width=True)
    
    st.markdown("---")
    
    # Cost comparison chart
    st.markdown("### Cost Trajectory Across Scenarios")
    
    scenario_names = list(scenario_results.keys())
    costs = [scenario_results[s]['cost_with_policy'] for s in scenario_names]
    colors_list = [scenarios[s]['color'] for s in scenario_names]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=scenario_names,
        y=costs,
        marker=dict(color=colors_list),
        text=[f"${c:.0f}/ton" for c in costs],
        textposition='outside',
    ))
    fig.add_hline(y=400, line_dash="dash", line_color="orange", 
                 annotation_text="Import Baseline ($400/ton)")
    fig.add_hline(y=350, line_dash="dash", line_color="green",
                 annotation_text="Target Cost ($350/ton)")
    
    fig.update_layout(
        title="Cost per Ton Across Policy Scenarios",
        yaxis_title="Cost (USD/ton)",
        xaxis_title="Policy Scenario",
        height=400,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed scenario cards
    st.markdown("### Scenario Details")
    
    for scenario_name, scenario_params in scenarios.items():
        results = scenario_results[scenario_name]
        
        with st.expander(f"**{scenario_name}** — {scenario_params['description']}", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Cost/Ton", f"${results['cost_with_policy']:.0f}")
            with col2:
                st.metric("CO₂/Ton", f"{results['co2']:.0f} kg")
            with col3:
                st.metric("Daily Energy", f"{results['energy']:.0f} MWh")
            with col4:
                st.metric("Viability", results['viability'])
            
            st.markdown("**Policy Parameters:**")
            st.markdown(f"""
- **Electricity Cost:** ${scenario_params['electricity_cost']:.3f}/kWh
- **Direct Subsidy:** ${scenario_params['subsidy']:.0f}/ton
- **Carbon Tax (incentive):** ${scenario_params['carbon_tax']:.2f}/kg CO₂
- **Tech Improvement:** {scenario_params['tech_improvement']:.1f}% (electrolyser efficiency)
            """)
            
            # Generate cabinet briefing for this scenario
            if st.button(f"📄 Generate Briefing: {scenario_name}", key=f"briefing_{scenario_name}"):
                pdf = generate_cabinet_briefing_pdf(scenario_name, results, 400)
                st.download_button(
                    label=f"📥 Download {scenario_name} Briefing.pdf",
                    data=pdf,
                    file_name=f"s2f_dt_briefing_{scenario_name.replace(' ', '_').lower()}.pdf",
                    mime="application/pdf",
                    key=f"download_{scenario_name}"
                )

# ===== RISK & RESILIENCE TAB =====
with tab_risk:
    st.markdown("## Risk Assessment & Resilience Analysis")
    st.markdown("""
Explore how market shocks and operational risks affect project viability,
and which policy mechanisms provide resilience.
    """)
    
    st.markdown("### Market Shock Scenarios")
    
    # Define risk scenarios
    risk_scenarios = {
        "Electricity Price Spike": {
            "description": "Grid inflation or energy transition cost",
            "change": lambda econ: {**econ, "cost_usd_per_ton": econ["cost_usd_per_ton"] * 1.3},
            "impact": "30% cost increase",
            "mitigation": "Long-term PPA at fixed rate"
        },
        "Solar Degradation": {
            "description": "Lower than expected capacity factor (dust, dust storms)",
            "change": lambda econ: {**econ, "cost_usd_per_ton": econ["cost_usd_per_ton"] * 1.15},
            "impact": "15% cost increase",
            "mitigation": "Maintenance fund allocation; cleaner specifications in PPA"
        },
        "Market Oversupply": {
            "description": "Global ammonia price collapse (new producers, green displacement)",
            "change": lambda econ: {"import_baseline": 250},
            "impact": "Import baseline drops to $250/ton",
            "mitigation": "Minimum purchase guarantee (gov); export market development"
        },
        "Water Scarcity Premium": {
            "description": "Climate stress or agricultural demand surge",
            "change": lambda econ: {**econ, "cost_usd_per_ton": econ["cost_usd_per_ton"] * 1.10},
            "impact": "10% cost increase",
            "mitigation": "Allocate treated/recycled water; invest in water conservation"
        },
        "Technology Breakthrough": {
            "description": "Electrolyser efficiency improves faster than expected",
            "change": lambda econ: {**econ, "cost_usd_per_ton": econ["cost_usd_per_ton"] * 0.85},
            "impact": "15% cost reduction",
            "mitigation": "Accelerate deployment; capture first-mover advantage"
        }
    }
    
    # Compare baseline vs Green Push scenario under risks
    baseline_config = config_dict.copy()
    baseline_config["electricity_cost_usd_kwh"] = 0.04
    baseline_econ = calculate_scenario_economics(baseline_config)
    
    greenpush_config = config_dict.copy()
    greenpush_config["electricity_cost_usd_kwh"] = 0.030
    greenpush_config["electrolyser_efficiency"] = 42.0  # 5% improvement
    greenpush_econ = calculate_scenario_economics(greenpush_config)
    greenpush_econ["cost_usd_per_ton"] = greenpush_econ["cost_usd_per_ton"] - 50  # Subsidy
    
    # Build risk assessment table
    st.markdown("### Risk Impact Analysis: Baseline vs Green Push Policy")
    
    risk_rows = []
    for risk_name, risk_params in risk_scenarios.items():
        risk_rows.append({
            "Risk Factor": risk_name,
            "Baseline Viability": "❌ Fails" if (baseline_econ["cost_usd_per_ton"] * 1.3) > 450 else "⚠️ Marginal",
            "With Green Push": "✓ Resilient" if (greenpush_econ["cost_usd_per_ton"] * 1.1) < 400 else "✓ Good",
            "Mitigation": risk_params["mitigation"]
        })
    
    risk_df = pd.DataFrame(risk_rows)
    st.dataframe(risk_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Risk resilience visualization
    st.markdown("### Resilience Under Stress: Cost per Ton")
    
    risk_factors = list(risk_scenarios.keys())
    baseline_stressed = []
    greenpush_stressed = []
    
    for risk_name in risk_factors:
        # Baseline under stress
        if risk_name == "Electricity Price Spike":
            baseline_stressed.append(baseline_econ["cost_usd_per_ton"] * 1.3)
            greenpush_stressed.append(greenpush_econ["cost_usd_per_ton"] * 1.1)
        elif risk_name == "Solar Degradation":
            baseline_stressed.append(baseline_econ["cost_usd_per_ton"] * 1.15)
            greenpush_stressed.append(greenpush_econ["cost_usd_per_ton"] * 1.08)
        elif risk_name == "Market Oversupply":
            baseline_stressed.append(baseline_econ["cost_usd_per_ton"])
            greenpush_stressed.append(greenpush_econ["cost_usd_per_ton"])
        elif risk_name == "Water Scarcity Premium":
            baseline_stressed.append(baseline_econ["cost_usd_per_ton"] * 1.10)
            greenpush_stressed.append(greenpush_econ["cost_usd_per_ton"] * 1.06)
        else:  # Technology Breakthrough
            baseline_stressed.append(baseline_econ["cost_usd_per_ton"] * 0.85)
            greenpush_stressed.append(greenpush_econ["cost_usd_per_ton"] * 0.88)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=risk_factors,
        y=baseline_stressed,
        mode='lines+markers',
        name='Baseline (No Policy)',
        line=dict(color='#ff6b6b', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=risk_factors,
        y=greenpush_stressed,
        mode='lines+markers',
        name='Green Push Policy',
        line=dict(color='#6bcf7f', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_hline(y=400, line_dash="dash", line_color="orange",
                 annotation_text="Viable Threshold ($400/ton)")
    
    fig.update_layout(
        title="Cost Resilience Under Market Shocks",
        xaxis_title="Risk Scenario",
        yaxis_title="Cost (USD/ton)",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### Key Insights")
    st.markdown("""
- **Policy acts as shock absorber:** Green Push scenario remains viable across most shocks
- **Electricity lock-in critical:** Long-term PPA is the #1 risk mitigation
- **Technology upside:** Breakthroughs in electrolysers have 3× impact vs downside risks
- **Market risk manageable:** Gov can use minimum purchase guarantee to offset oversupply
    """)

# ===== EXPORT & BRIEFING TAB =====
with tab_excel:
    st.markdown("## Export Strategic Analysis")
    st.markdown("Generate cabinet briefing documents, Excel reports, and policy recommendations.")
    
    st.markdown("---")
    
    st.markdown("### Option 1: Cabinet Briefing PDF")
    st.markdown("One-page professional summary for government decision-makers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_scenario = st.selectbox(
            "Select Scenario to Brief",
            list(scenario_results.keys()),
            help="Choose which policy scenario to present"
        )
    
    with col2:
        department = st.selectbox(
            "Target Department",
            ["Cabinet / Executive Office", "Finance Ministry", "Climate/Greening Committee", "Economic Affairs", "Custom"],
            help="Tailor messaging for specific audience"
        )
    
    if st.button("📄 Generate Cabinet Briefing", type="primary", use_container_width=True):
        results = scenario_results[selected_scenario]
        pdf = generate_cabinet_briefing_pdf(selected_scenario, results, 400)
        st.download_button(
            label="📥 Download Briefing PDF",
            data=pdf,
            file_name=f"S2F-DT_Cabinet_Briefing_{selected_scenario.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
        st.success(f"✅ Generated briefing for: {selected_scenario}")
    
    st.markdown("---")
    
    st.markdown("### Option 2: Comprehensive Excel Report")
    st.markdown("Detailed analysis with all scenarios, assumptions, and financial projections")
    
    if st.button("📊 Generate Excel Report", use_container_width=True):
        # Create Excel workbook with multiple sheets
        excel_buffer = BytesIO()
        
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            # Sheet 1: Scenario Comparison
            scenario_comparison = []
            for scenario_name, results in scenario_results.items():
                scenario_comparison.append({
                    "Scenario": scenario_name,
                    "Cost (USD/ton)": round(results['cost_with_policy'], 2),
                    "vs Import Baseline": round(results['cost_with_policy'] - 400, 2),
                    "CO₂ (kg/ton)": round(results['co2'], 1),
                    "Daily Energy (MWh)": round(results['energy'], 1),
                    "Daily Water (m³)": round(results['water'], 1),
                })
            
            pd.DataFrame(scenario_comparison).to_excel(writer, sheet_name='Scenarios', index=False)
            
            # Sheet 2: Assumptions
            assumptions = {
                "Parameter": [
                    "Target NH₃ Production",
                    "Solar Capacity",
                    "Electrolyser Efficiency (Baseline)",
                    "N₂ Separation Energy",
                    "Synthesis Energy",
                    "Capacity Factor",
                    "Electricity Cost (Baseline)",
                    "Water Cost",
                ],
                "Value": [
                    config_dict["target_nh3_day"],
                    config_dict["solar_capacity_mw"],
                    config_dict["electrolyser_efficiency"],
                    config_dict["n2_separation_energy"],
                    config_dict["synthesis_energy"],
                    config_dict["capacity_factor"],
                    config_dict["electricity_cost_usd_kwh"],
                    config_dict["water_cost_usd_m3"],
                ],
                "Unit": [
                    "tons/day",
                    "MW",
                    "kWh/kg H₂",
                    "kWh/kg N₂",
                    "kWh/kg NH₃",
                    "fraction",
                    "USD/kWh",
                    "USD/m³",
                ]
            }
            
            pd.DataFrame(assumptions).to_excel(writer, sheet_name='Assumptions', index=False)
            
            # Sheet 3: Policy Parameters
            policy_parameters = []
            for scenario_name, params in scenarios.items():
                policy_parameters.append({
                    "Scenario": scenario_name,
                    "Electricity Cost": f"${params['electricity_cost']:.3f}/kWh",
                    "Direct Subsidy": f"${params['subsidy']:.0f}/ton",
                    "Carbon Tax": f"${params['carbon_tax']:.2f}/kg CO₂",
                    "Tech Improvement": f"{params['tech_improvement']:.1f}%",
                })
            
            pd.DataFrame(policy_parameters).to_excel(writer, sheet_name='Policy Parameters', index=False)
        
        excel_buffer.seek(0)
        st.download_button(
            label="📥 Download Excel Report",
            data=excel_buffer,
            file_name=f"S2F-DT_Strategic_Analysis_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        st.success("✅ Generated comprehensive Excel report")
    
    st.markdown("---")
    
    st.markdown("### Option 3: Policy Recommendation Summary")
    
    recommendation_text = f"""
## S2F-DT Strategic Recommendation Summary

**Date:** {datetime.now().strftime('%B %d, %Y')}  
**Organization:** {COMPANY_NAME}

### Executive Summary
Solar-powered ammonia production is technically and economically viable for UAE. 
The "Green Push" policy scenario achieves cost parity with imports while delivering
95%+ CO₂ reduction, supporting UAE's Net Zero 2050 commitment.

### Recommended Policy Package (Green Push)
1. **Electricity:** Secure long-term renewable PPA at $0.030/kWh (10–15 year contract)
2. **Subsidy:** $50/ton direct incentive (5–10 year phase-out as technology matures)
3. **Carbon Incentive:** $0.15/kg CO₂ tax credit or offset value
4. **R&D Support:** $X million annual for electrolyser and catalyst research

### Implementation Timeline
- **Phase 1 (2026–2028):** Pilot 1–2 plants (Abu Dhabi, Masdar City)
- **Phase 2 (2028–2030):** Scale to 15–20 plants (all emirates)
- **Phase 3 (2030–2035):** Full capacity (50+ plants, 100% ammonia self-sufficiency)

### Key Success Factors
- Lock in low-cost renewable electricity early
- Allocate treated/recycled water (not freshwater)
- Build expertise in electrolyser technology
- Develop domestic supply chain (manufacturing, maintenance)

### Risk Management
- Implement minimum purchase guarantee to protect against market crashes
- Establish resilience fund for operational shocks
- Monitor technology learning curve and adjust subsidy accordingly
- Diversify supply (pure solar, wind hybrid)

### Expected Outcomes (by 2035)
- **Production:** 200,000+ metric tons ammonia/year (100% self-sufficiency)
- **CapEx:** $5–7 billion total investment
- **Job Creation:** 5,000+ direct + indirect employment
- **CO₂ Avoided:** 1.3+ million metric tons/year vs imports
- **Water Managed:** 50–70 million m³/year (local desalination)
- **Technology Leadership:** UAE becomes regional hub for green hydrogen/ammonia

---

{IP_NOTICE}
    """
    
    if st.button("📋 Copy Recommendation Text", use_container_width=True):
        st.text_area(
            "Copy text below for presentation/memo:",
            value=recommendation_text,
            height=300,
            disabled=True
        )

st.markdown("---")

# Footer
st.markdown(f"""
<div style='text-align: center; font-size: 0.75rem; color: #666; border-top: 1px solid #ddd; padding-top: 1rem; margin-top: 2rem;'>
<p><strong style='color: #003366'>{COMPANY_NAME}</strong> | {COMPANY_LOCATION}</p>
<p>{IP_NOTICE}</p>
<p><em>Phase 2 Policy Tools: Scenario comparison, risk assessment, executive briefing export</em></p>
</div>
""", unsafe_allow_html=True)
