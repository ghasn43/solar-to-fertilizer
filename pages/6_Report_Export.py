"""
Page 6: Report Export
"""
import streamlit as st
from datetime import datetime
import json
from core.models import ProcessConfig
from core.process import process_model
from core.reporting import generate_pdf_report, export_config_json
from core.constants import COMPANY_NAME, COMPANY_LOCATION, IP_NOTICE

st.set_page_config(page_title="6. Report Export | S2F-DT", layout="wide")

st.markdown(f"<div style='color:#003366'><h1>📄 Report Export</h1></div>", unsafe_allow_html=True)

st.markdown("""
Generate and export a 1-page PDF report and JSON configuration file 
for archival, presentations, or integration with other tools.
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

if "scenarios" not in st.session_state:
    st.session_state.scenarios = []

st.markdown("---")

# Select Scenario
st.markdown("### 📊 Select Scenario for Report")

if st.session_state.scenarios:
    scenario_names = [s.name for s in st.session_state.scenarios]
    selected_scenario_idx = st.selectbox(
        "Choose scenario to include in report",
        options=range(len(scenario_names)),
        format_func=lambda x: scenario_names[x],
        help="Select which scenario to highlight in the PDF report"
    )
    selected_scenario = st.session_state.scenarios[selected_scenario_idx]
else:
    st.warning("No scenarios found. Go to **Scenarios UAE** page to create scenarios.")
    selected_scenario = None

st.markdown("---")

# Calculate current results
config_dict = st.session_state.process_config
config = ProcessConfig(**config_dict)
results = process_model(config)

st.markdown("### 📋 Report Preview")

col_preview_a, col_preview_b = st.columns([1, 1])

with col_preview_a:
    st.markdown(f"""
#### Configuration
- **Target NH₃**: {config_dict['target_nh3_day']:.2f} tons/day
- **Solar Capacity**: {config_dict['solar_capacity_mw']:.0f} MW
- **Capacity Factor**: {config_dict['capacity_factor']:.1%}
- **Electrolyser Efficiency**: {config_dict['electrolyser_efficiency']:.1f} kWh/kg H₂
- **Catalyst Factor**: {config_dict['catalyst_factor']:.2f}
    """)

with col_preview_b:
    st.markdown(f"""
#### Key Results
- **Daily Output**: {results.nh3_tons_day:.2f} tons NH₃
- **Daily Water**: {results.water_m3_day:.1f} m³
- **Daily Electricity**: {results.electricity_kwh_day:,.0f} kWh
- **CO₂ Intensity**: {results.co2_intensity_kg_per_kg_nh3 * 1000:.1f} kg CO₂/ton
- **Cost**: ${results.cost_usd_per_ton_nh3:.0f}/ton NH₃
    """)

st.markdown("---")

# Export Controls
st.markdown("### 💾 Export & Download")

col_export_a, col_export_b = st.columns(2, gap="large")

with col_export_a:
    st.markdown("#### PDF Report")
    st.markdown("""
One-page summary including:
- Company branding & IP notice
- Selected scenario details
- Key inputs & KPIs
- Scenario comparison table
    """)
    
    if st.button("📄 Generate PDF Report", use_container_width=True, type="primary"):
        try:
            # Prepare data for PDF
            scenarios_comparison = [
                {
                    "Scenario": s.name,
                    "NH₃ (t/d)": f"{s.nh3_tons_day:.2f}",
                    "Cost ($/t)": f"{s.cost_usd_per_ton:.0f}",
                    "CO₂ (kg/t)": f"{s.co2_kg_per_ton:.0f}",
                }
                for s in st.session_state.scenarios
            ]
            
            process_results = {
                "nh3_tons_day": results.nh3_tons_day,
                "water_m3_day": results.water_m3_day,
                "electricity_kwh_day": results.electricity_kwh_day,
                "co2_intensity_kg_per_kg_nh3": results.co2_intensity_kg_per_kg_nh3,
            }
            
            selected_scenario = st.session_state.scenarios[selected_scenario_idx] if st.session_state.scenarios else None
            
            if selected_scenario:
                pdf_buffer = generate_pdf_report(
                    scenario=selected_scenario,
                    config_dict=config_dict,
                    process_results=process_results,
                    scenarios_comparison=scenarios_comparison,
                )
                
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_buffer,
                    file_name=f"S2F-DT_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                )
                st.success("✅ PDF generated! Click above to download.")
            else:
                st.warning("Please select a scenario first.")
        
        except ImportError:
            st.error("""
⚠️ **reportlab** is required for PDF generation.  
Run: `pip install reportlab`
            """)
        except Exception as e:
            st.error(f"❌ PDF Generation Error: {str(e)}")

with col_export_b:
    st.markdown("#### JSON Configuration")
    st.markdown("""
Portable config file including:
- All input parameters
- Calculation results
- Metadata (timestamp, etc.)
    """)
    
    if st.button("📋 Generate JSON Config", use_container_width=True):
        try:
            json_str = export_config_json(
                config_dict=config_dict,
                process_results={
                    "nh3_tons_day": results.nh3_tons_day,
                    "water_m3_day": results.water_m3_day,
                    "electricity_kwh_day": results.electricity_kwh_day,
                    "co2_intensity_kg_per_kg_nh3": results.co2_intensity_kg_per_kg_nh3,
                    "cost_usd_per_ton_nh3": results.cost_usd_per_ton_nh3,
                },
                scenario_name=selected_scenario.name if selected_scenario else "Custom",
            )
            
            st.download_button(
                label="📥 Download JSON",
                data=json_str,
                file_name=f"S2F-DT_Config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
            )
            st.success("✅ JSON generated! Click above to download.")
        
        except Exception as e:
            st.error(f"❌ JSON Generation Error: {str(e)}")

st.markdown("---")

# Display JSON Preview
with st.expander("👁️ JSON Preview"):
    json_preview = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "company": COMPANY_NAME,
            "application": "Solar-to-Fertiliser Digital Twin (S2F-DT)",
        },
        "scenario": selected_scenario.name if selected_scenario else "Custom",
        "configuration": config_dict,
        "results": {
            "nh3_tons_day": float(results.nh3_tons_day),
            "water_m3_day": float(results.water_m3_day),
            "electricity_kwh_day": float(results.electricity_kwh_day),
            "co2_intensity_kg_per_kg_nh3": float(results.co2_intensity_kg_per_kg_nh3),
            "cost_usd_per_ton_nh3": float(results.cost_usd_per_ton_nh3),
        },
    }
    st.json(json_preview)

st.markdown("---")

# Usage Guide
st.markdown("### 📖 How to Use Exports")

col_usage_a, col_usage_b = st.columns(2)

with col_usage_a:
    st.markdown("""
#### PDF Report
- **Presentations**: Insert into slide decks
- **Meetings**: Print for stakeholder discussions
- **Archives**: Record project state at specific date
- **Proposals**: Include in feasibility studies

**Recipients**: Non-technical stakeholders, management, clients
    """)

with col_usage_b:
    st.markdown("""
#### JSON Configuration
- **Version Control**: Git-track all configurations
- **Reproducibility**: Load exact config later
- **Integration**: Consume in other Python/JS tools
- **Batch Processing**: Run multiple configs in script

**Recipients**: Technical teams, data pipelines, analysis tools
    """)

st.markdown("---")

# Footer
st.markdown(f"""
<div style='text-align: center; font-size: 0.75rem; color: #666; border-top: 1px solid #ddd; padding-top: 1rem; margin-top: 2rem;'>
<p><strong style='color: #003366'>{COMPANY_NAME}</strong> | {COMPANY_LOCATION}</p>
<p>{IP_NOTICE}</p>
</div>
""", unsafe_allow_html=True)
