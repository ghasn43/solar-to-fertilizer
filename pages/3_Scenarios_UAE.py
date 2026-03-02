"""
Page 3: Scenarios UAE
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from core.models import ProcessConfig
from core.scenarios import (
    create_scenario_1_baseline,
    create_scenario_2_uae_green,
    create_scenario_3_future_catalyst,
    compare_scenarios,
    uae_greening_text,
)
from core.constants import COMPANY_NAME, COMPANY_LOCATION, IP_NOTICE

st.set_page_config(page_title="3. Scenarios UAE | S2F-DT", layout="wide")

st.markdown(f"<div style='color:#003366'><h1>🌍 Scenarios: UAE Greening</h1></div>", unsafe_allow_html=True)

st.markdown("""
Compare three contrasting scenarios to understand the value of solar-powered green ammonia 
for UAE's greening agenda and agricultural fertiliser needs.
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

# Create three scenarios
st.sidebar.markdown("### 📊 Scenario Configuration")

target_nh3 = st.sidebar.slider(
    "Target NH₃ (tons/day)",
    min_value=1.0,
    max_value=20.0,
    value=config_dict["target_nh3_day"],
    step=0.5
)
st.session_state.process_config["target_nh3_day"] = target_nh3

# Scenario 1: Baseline (user can modify)
st.sidebar.markdown("#### S1: Imported Baseline")
baseline_cost = st.sidebar.number_input(
    "Cost (USD/ton)",
    min_value=200.0,
    max_value=600.0,
    value=400.0,
    step=10.0
)
baseline_co2 = st.sidebar.number_input(
    "CO₂ (kg/ton)",
    min_value=1.0,
    max_value=5.0,
    value=2.0,
    step=0.1
)

# Scenario 2: UAE Green (from current config)
config = ProcessConfig(**config_dict)
scenario_2 = create_scenario_2_uae_green(config)

# Scenario 3: Future Catalyst (improved)
st.sidebar.markdown("#### S3: Future Catalyst")
catalyst_improvement = st.sidebar.slider(
    "Catalyst Factor (0.5=best, 1.0=baseline)",
    min_value=0.5,
    max_value=1.2,
    value=0.8,
    step=0.05
)

scenario_1 = create_scenario_1_baseline(target_nh3)
scenario_1.cost_usd_per_ton = baseline_cost
scenario_1.co2_kg_per_ton = baseline_co2 * 1000

scenario_3 = create_scenario_3_future_catalyst(config, catalyst_factor_improvement=catalyst_improvement)

# Store scenarios in session
st.session_state.scenarios = [scenario_1, scenario_2, scenario_3]

st.markdown("---")

# Scenario Comparison Table
st.markdown("### 📋 Scenario Comparison Table")

comparison_df = pd.DataFrame({
    "Scenario": [scenario_1.name, scenario_2.name, scenario_3.name],
    "Description": [scenario_1.description, scenario_2.description, scenario_3.description],
    "NH₃ (tons/day)": [
        f"{scenario_1.nh3_tons_day:.2f}",
        f"{scenario_2.nh3_tons_day:.2f}",
        f"{scenario_3.nh3_tons_day:.2f}",
    ],
    "Cost (USD/ton)": [
        f"${scenario_1.cost_usd_per_ton:.0f}",
        f"${scenario_2.cost_usd_per_ton:.0f}",
        f"${scenario_3.cost_usd_per_ton:.0f}",
    ],
    "CO₂ Intensity (kg CO₂/ton)": [
        f"{scenario_1.co2_kg_per_ton:.0f}",
        f"{scenario_2.co2_kg_per_ton:.0f}",
        f"{scenario_3.co2_kg_per_ton:.0f}",
    ],
})

st.dataframe(comparison_df, use_container_width=True)

# Charts
col_chart_a, col_chart_b = st.columns([1, 1], gap="large")

with col_chart_a:
    st.markdown("#### Cost Comparison")
    cost_data = {
        "S1\nImported": scenario_1.cost_usd_per_ton,
        "S2\nGreen UAE": scenario_2.cost_usd_per_ton,
        "S3\nFuture": scenario_3.cost_usd_per_ton,
    }
    fig, ax = plt.subplots(figsize=(5, 4))
    colors = ['#ff6b6b', '#52c41a', '#1890ff']
    bars = ax.bar(cost_data.keys(), cost_data.values(), color=colors)
    ax.set_ylabel("Cost (USD/ton NH₃)", fontweight='bold')
    ax.set_title("Production Cost Comparison", fontweight='bold')
    ax.set_ylim(0, max(cost_data.values()) * 1.2)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:.0f}', ha='center', va='bottom', fontweight='bold')
    st.pyplot(fig)

with col_chart_b:
    st.markdown("#### CO₂ Intensity Comparison")
    co2_data = {
        "S1\nImported": scenario_1.co2_kg_per_ton,
        "S2\nGreen UAE": scenario_2.co2_kg_per_ton,
        "S3\nFuture": scenario_3.co2_kg_per_ton,
    }
    fig, ax = plt.subplots(figsize=(5, 4))
    colors = ['#ff6b6b', '#52c41a', '#1890ff']
    bars = ax.bar(co2_data.keys(), co2_data.values(), color=colors)
    ax.set_ylabel("CO₂ Intensity (kg CO₂/ton NH₃)", fontweight='bold')
    ax.set_title("Carbon Footprint Comparison", fontweight='bold')
    ax.set_ylim(0, max(co2_data.values()) * 1.2)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}', ha='center', va='bottom', fontweight='bold')
    st.pyplot(fig)

st.markdown("---")

# Strategic Analysis
st.markdown("### 🎯 Strategic Analysis")

col_text_a, col_text_b = st.columns([1, 1], gap="large")

with col_text_a:
    cost_saving_s2 = ((scenario_1.cost_usd_per_ton - scenario_2.cost_usd_per_ton) 
                       / scenario_1.cost_usd_per_ton * 100)
    cost_saving_s3 = ((scenario_1.cost_usd_per_ton - scenario_3.cost_usd_per_ton) 
                       / scenario_1.cost_usd_per_ton * 100)
    
    st.markdown(f"""
#### Cost-Competitiveness
- **Baseline Import**: ${scenario_1.cost_usd_per_ton:.0f}/ton
- **S2 (Green UAE)**: ${scenario_2.cost_usd_per_ton:.0f}/ton → **{cost_saving_s2:+.0f}%**
- **S3 (Future)**: ${scenario_3.cost_usd_per_ton:.0f}/ton → **{cost_saving_s3:+.0f}%**

**Analysis:**
- Green ammonia is cost-competitive when electricity cost < $0.04/kWh
- UAE solar + low energy costs create native advantage
- Future catalyst (S3) can improve margin further
    """)

with col_text_b:
    co2_reduction_s2 = ((scenario_1.co2_kg_per_ton - scenario_2.co2_kg_per_ton) 
                         / scenario_1.co2_kg_per_ton * 100)
    co2_reduction_s3 = ((scenario_1.co2_kg_per_ton - scenario_3.co2_kg_per_ton) 
                         / scenario_1.co2_kg_per_ton * 100)
    
    st.markdown(f"""
#### Carbon Reduction
- **Baseline Import**: {scenario_1.co2_kg_per_ton:.0f} kg CO₂/ton
- **S2 (Green UAE)**: {scenario_2.co2_kg_per_ton:.0f} kg CO₂/ton → **{co2_reduction_s2:+.0f}%**
- **S3 (Future)**: {scenario_3.co2_kg_per_ton:.0f} kg CO₂/ton → **{co2_reduction_s3:+.0f}%**

**Analysis:**
- Solar-powered production eliminates ~95% of transport + direct emissions
- Aligns with UAE Net Zero 2050 mandate
- Future catalysts further reduce energy footprint
    """)

st.markdown("---")

# UAE Greening/Sustainability
st.markdown("### 🌱 How This Supports UAE Greening & Food Security")

st.markdown(uae_greening_text())

st.markdown("---")

# Key Takeaways
st.markdown("### 💡 Key Takeaways")

col_t1, col_t2, col_t3 = st.columns(3)

with col_t1:
    st.markdown("""
**Environmental**
- ☀️ Solar-powered production
- 🌍 ~95% CO₂ reduction vs. imports
- 💧 Circular water use (desalination)
    """)

with col_t2:
    st.markdown("""
**Economic**
- 💰 Cost parity or better vs. imports
- 🏭 Local production = lower transport cost
- 📈 Scalable with solar expansion
    """)

with col_t3:
    st.markdown("""
**Strategic**
- 🇦🇪 Food security via local fertiliser
- 🏆 UAE tech leadership
- ⚡ Synergy with green hydrogen initiative
    """)

st.markdown("---")

# Footer
st.markdown(f"""
<div style='text-align: center; font-size: 0.75rem; color: #666; border-top: 1px solid #ddd; padding-top: 1rem; margin-top: 2rem;'>
<p><strong style='color: #003366'>{COMPANY_NAME}</strong> | {COMPANY_LOCATION}</p>
<p>{IP_NOTICE}</p>
</div>
""", unsafe_allow_html=True)
