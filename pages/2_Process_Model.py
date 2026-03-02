"""
Page 2: Process Model
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from core.models import ProcessConfig
from core.process import process_model
from core.constants import COMPANY_NAME, COMPANY_LOCATION, IP_NOTICE

st.set_page_config(page_title="2. Process Model | S2F-DT", layout="wide")

st.markdown(f"<div style='color:#003366'><h1>🔧 Process Model & Simulation</h1></div>", unsafe_allow_html=True)

st.markdown("""
Configure process parameters and simulate mass balance, energy requirements, and economics.
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

st.sidebar.markdown("### 🎛️ Configuration Inputs")

# Inputs Section
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("#### Production Target")
    target_nh3 = st.slider(
        "Target NH₃ Output (tons/day)",
        min_value=0.5,
        max_value=50.0,
        value=st.session_state.process_config["target_nh3_day"],
        step=0.5,
        help="Daily ammonia production target"
    )
    st.session_state.process_config["target_nh3_day"] = target_nh3
    
    st.markdown("#### Solar & Capacity")
    solar_mw = st.slider(
        "Solar Capacity (MW)",
        min_value=10.0,
        max_value=200.0,
        value=st.session_state.process_config["solar_capacity_mw"],
        step=5.0,
        help="Total solar PV capacity installed"
    )
    st.session_state.process_config["solar_capacity_mw"] = solar_mw
    
    cap_factor = st.slider(
        "Capacity Factor (%)",
        min_value=5,
        max_value=40,
        value=int(st.session_state.process_config["capacity_factor"] * 100),
        step=1,
        help="Solar availability: UAE ~25% annual average"
    )
    st.session_state.process_config["capacity_factor"] = cap_factor / 100

with col_right:
    st.markdown("#### Electrolyser & Synthesis")
    electrolyser_eff = st.slider(
        "Electrolyser Efficiency (kWh/kg H₂)",
        min_value=35.0,
        max_value=55.0,
        value=st.session_state.process_config["electrolyser_efficiency"],
        step=1.0,
        help="PEM/Alkaline: 40-50 typical; 35-55 range"
    )
    st.session_state.process_config["electrolyser_efficiency"] = electrolyser_eff
    
    catalyst_factor = st.slider(
        "Catalyst Improvement Factor",
        min_value=0.5,
        max_value=1.5,
        value=st.session_state.process_config["catalyst_factor"],
        step=0.05,
        help="0.5 = breakthrough (50% energy reduction), 1.0 = baseline, 1.2 = worse"
    )
    st.session_state.process_config["catalyst_factor"] = catalyst_factor
    
    synthesis_energy = st.slider(
        "Synthesis Energy (kWh/kg NH₃)",
        min_value=5.0,
        max_value=12.0,
        value=st.session_state.process_config["synthesis_energy"],
        step=0.5,
        help="Haber-Bosch: 8-10 typical (affected by catalyst factor)"
    )
    st.session_state.process_config["synthesis_energy"] = synthesis_energy

st.markdown("---")

col_cost_a, col_cost_b = st.columns([1, 1])

with col_cost_a:
    st.markdown("#### Energy & Water Costs")
    elec_cost = st.number_input(
        "Electricity Cost (USD/kWh)",
        min_value=0.01,
        max_value=0.20,
        value=st.session_state.process_config["electricity_cost_usd_kwh"],
        step=0.005,
        format="%.4f",
        help="UAE rate ~0.04 USD/kWh (~0.15 AED/kWh)"
    )
    st.session_state.process_config["electricity_cost_usd_kwh"] = elec_cost
    
    water_cost = st.number_input(
        "Water Cost (USD/m³)",
        min_value=0.5,
        max_value=5.0,
        value=st.session_state.process_config["water_cost_usd_m3"],
        step=0.1,
        format="%.2f",
        help="UAE desalination ~1.5 AED/m³ (~0.41 USD/m³)"
    )
    st.session_state.process_config["water_cost_usd_m3"] = water_cost

with col_cost_b:
    st.markdown("#### Options")
    include_urea = st.checkbox(
        "Include Urea Production",
        value=st.session_state.process_config["include_urea"],
        help="Add urea synthesis stage (2NH₃ + CO₂ → Urea)"
    )
    st.session_state.process_config["include_urea"] = include_urea

st.markdown("---")

# Run simulation
st.markdown("### 📊 Simulation Results")

config_dict = st.session_state.process_config
config = ProcessConfig(**config_dict)

try:
    results = process_model(config)
    
    # KPI Summary
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        st.metric("NH₃ Daily Output", f"{results.nh3_tons_day:.2f} tons", "tons/day")
    with kpi_col2:
        st.metric("Daily Electricity", f"{results.electricity_kwh_day:,.0f} kWh", "kWh/day")
    with kpi_col3:
        st.metric("Daily Water Usage", f"{results.water_m3_day:.1f} m³", "m³/day")
    with kpi_col4:
        st.metric("Cost Per Ton", f"${results.cost_usd_per_ton_nh3:.0f}", "USD/ton NH₃")
    
    st.markdown("---")
    
    # Energy Breakdown Chart
    col_chart_a, col_chart_b = st.columns([1, 1])
    
    with col_chart_a:
        st.markdown("#### Energy Breakdown (Daily)")
        energy_data = results.energy_breakdown
        
        fig, ax = plt.subplots(figsize=(6, 4))
        colors = ['#667eea', '#764ba2', '#f093fb']
        ax.pie(
            energy_data.values(),
            labels=energy_data.keys(),
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        ax.set_title(f"Total: {sum(energy_data.values()):,.0f} kWh/day", fontweight='bold')
        st.pyplot(fig)
    
    with col_chart_b:
        st.markdown("#### Energy by Block (kWh/day)")
        energy_df = pd.DataFrame(
            list(energy_data.items()),
            columns=["Block", "kWh/day"]
        )
        st.bar_chart(energy_df.set_index("Block"))
    
    st.markdown("---")
    
    # Detailed Results Table
    st.markdown("#### 📈 Detailed Calculation Table")
    
    nh3_kg_day = results.nh3_tons_day * 1000
    h2_required_kg = nh3_kg_day * (6 / 34)  # STOICH_H2_TO_NH3
    n2_required_kg = nh3_kg_day * (28 / 34)  # STOICH_N2_TO_NH3
    
    results_table = pd.DataFrame({
        "Parameter": [
            "NH₃ Production",
            "H₂ Requirement",
            "N₂ Requirement",
            "Water for Electrolysis",
            "Total Daily Electricity",
            "Cost per Ton NH₃",
            "CO₂ Intensity (Solar)",
            "Capacity Factor",
            "Annual NH₃ Output",
        ],
        "Value": [
            f"{results.nh3_tons_day:.2f}",
            f"{h2_required_kg:.0f}",
            f"{n2_required_kg:.0f}",
            f"{results.water_m3_day:.1f}",
            f"{results.electricity_kwh_day:,.0f}",
            f"${results.cost_usd_per_ton_nh3:.0f}",
            f"{results.co2_intensity_kg_per_kg_nh3 * 1000:.1f} kg CO₂/ton",
            f"{cap_factor:.0%}",
            f"{results.nh3_tons_day * 365:.0f}",
        ],
        "Unit": [
            "tons/day",
            "kg/day",
            "kg/day",
            "m³/day",
            "kWh/day",
            "USD/ton",
            "kg CO₂/ton",
            "%",
            "tons/year",
        ]
    })
    
    st.table(results_table)
    
    # Energy balance detail
    st.markdown("#### ⚡ Energy Balance (Stoichiometry)")
    with st.expander("Show Detailed Energy Calculations"):
        st.markdown(f"""
**H₂ Production via Electrolysis:**
- H₂ Required: {h2_required_kg:,.0f} kg/day
- Electrolyser Efficiency: {electrolyser_eff:.1f} kWh/kg H₂
- Energy: {energy_data.get('Electrolysis', 0):,.0f} kWh/day

**N₂ Separation (Air):**
- N₂ Required: {n2_required_kg:,.0f} kg/day
- Separation Energy: 0.5 kWh/kg N₂
- Energy: {energy_data.get('N2 Separation', 0):,.0f} kWh/day

**Haber-Bosch Synthesis (N₂ + 3H₂ → 2NH₃):**
- Synthesis Energy: {synthesis_energy:.1f} kWh/kg NH₃
- Catalyst Factor: {catalyst_factor:.2f}×
- Effective Energy: {synthesis_energy * catalyst_factor:.2f} kWh/kg NH₃
- Energy: {energy_data.get('Synthesis (Haber-Bosch)', 0):,.0f} kWh/day

**Total Daily Energy: {results.electricity_kwh_day:,.0f} kWh**
- Annual: {results.electricity_kwh_day * 365:,.0f} kWh/year
- Solar Capacity Required: {solar_mw:.0f} MW @ {cap_factor:.0%} capacity factor
        """)

except Exception as e:
    st.error(f"Simulation Error: {str(e)}")

st.markdown("---")

# Footer
st.markdown(f"""
<div style='text-align: center; font-size: 0.75rem; color: #666; border-top: 1px solid #ddd; padding-top: 1rem; margin-top: 2rem;'>
<p><strong style='color: #003366'>{COMPANY_NAME}</strong> | {COMPANY_LOCATION}</p>
<p>{IP_NOTICE}</p>
</div>
""", unsafe_allow_html=True)
