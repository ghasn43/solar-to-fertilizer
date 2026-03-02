"""
Page 1: Overview
"""
import streamlit as st
from core.models import ProcessConfig
from core.process import process_model
from core.constants import (
    COMPANY_NAME,
    COMPANY_LOCATION,
    IP_NOTICE,
    STOICH_H2_TO_NH3,
    STOICH_N2_TO_NH3,
    WATER_USAGE_PER_KG_H2,
)

st.set_page_config(page_title="1. Overview | S2F-DT", layout="wide")

st.markdown(f"<div style='color:#003366'><h1>📊 Project Overview</h1></div>", unsafe_allow_html=True)

st.markdown("""
### Solar-to-Fertiliser Digital Twin (S2F-DT) — Executive Summary

This virtual project simulates the production of **ammonia (NH₃)** and optionally **urea** from:
- **Solar electricity** (UAE capacity)
- **Ambient air** (N₂ extraction)
- **Water** (electrolysis for H₂)

#### Mission
Support **UAE's green agenda** by producing clean fertiliser locally, reducing import dependency, 
lowering carbon footprint, and creating opportunities for agricultural and green-tech innovation.

#### Process Reaction
**N₂ + 3H₂ → 2NH₃** (Haber-Bosch, 100+ year old synthesis, still industry standard)

---
""")

# Key Performance Indicators (KPIs)
st.markdown("### 📈 Key Performance Indicators (KPIs)")

# Get default config and calculate results
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
config = ProcessConfig(**config_dict)
results = process_model(config)

# Display KPI cards in columns
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(
        "NH₃ Production",
        f"{results.nh3_tons_day:.2f} tons/day",
        delta="Target output",
        delta_color="off"
    )

with col2:
    if results.urea_tons_day:
        st.metric(
            "Urea Production",
            f"{results.urea_tons_day:.2f} tons/day",
            delta="(if enabled)",
            delta_color="off"
        )
    else:
        st.metric(
            "Urea Production",
            "Disabled",
            delta="(optional)",
            delta_color="off"
        )

with col3:
    st.metric(
        "Daily Electricity",
        f"{results.electricity_kwh_day:,.0f} kWh",
        delta=f"~{results.electricity_kwh_day/1000:.1f} MWh",
        delta_color="off"
    )

with col4:
    st.metric(
        "Daily Water Usage",
        f"{results.water_m3_day:.1f} m³",
        delta=f"~{results.water_m3_day*1000:.0f} kg",
        delta_color="off"
    )

with col5:
    st.metric(
        "CO₂ Intensity (Solar)",
        f"{results.co2_intensity_kg_per_kg_nh3 * 1000:.1f} kg CO₂/ton",
        delta="Per ton NH₃",
        delta_color="off"
    )

with col6:
    st.metric(
        "Cost Per Ton",
        f"${results.cost_usd_per_ton_nh3:.0f}",
        delta="USD/ton NH₃",
        delta_color="off"
    )

st.markdown("---")

# Assumptions accordion
st.markdown("### 📋 Stoichiometric & Process Assumptions")

with st.expander("🔬 Show All Assumptions", expanded=False):
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("""
#### Mass Balance (Stoichiometry)
**Reaction**: N₂ + 3H₂ → 2NH₃

For **1 ton of NH₃ produced**:
- **N₂ Required**: ~{:.3f} tons (28 kg out of 34 kg total)
- **H₂ Required**: ~{:.3f} tons (6 kg out of 34 kg total)

**Water for Electrolysis**:
- 2H₂O → 2H₂ + O₂
- Assumed: **{:.1f} kg water per kg H₂** (includes efficiency loss)

#### Energy Blocks (Default)
- **Electrolysis**: {} kWh/kg H₂ (PEM alkaline baseline)
- **N₂ Separation**: 0.5 kWh/kg N₂ (cryogenic or PSA)
- **Synthesis**: 8.0 kWh/kg NH₃ (Haber-Bosch reactor)
- **Catalyst Improvement**: 1.0× (multiplier; 0.5-1.2 range)
        """.format(
            STOICH_N2_TO_NH3,
            STOICH_H2_TO_NH3,
            WATER_USAGE_PER_KG_H2,
            config_dict["electrolyser_efficiency"]
        ))
    
    with col_b:
        st.markdown(f"""
#### Costs (Default)
- **Electricity Cost**: ${config_dict['electricity_cost_usd_kwh']}/kWh (~0.15 AED/kWh UAE rate)
- **Water Cost**: ${config_dict['water_cost_usd_m3']}/m³ (desalination 1.5 AED/m³)
- **CapEx Amortization**: $50/ton NH₃ (embedded in OpEx)

#### Emissions Factors
- **Solar**: 0.01 kg CO₂/kWh (lifecycle only)
- **Grid (UAE)**: 0.48 kg CO₂/kWh (gas + solar mix)

#### Capacity & Availability
- **Solar Capacity Factor**: {} (25% annual average for UAE)
- **Daily Effective Output**: Solar MW × 24h × Capacity Factor

#### Assumptions & Caveats
- ✓ No CO₂ capture cost (for urea feedstock)
- ✓ Pressure & temperature optimized for Haber-Bosch
- ✓ Catalyst efficiency modeled as multiplier
- ✓ Linear cost model (reality: economy of scale)
        """.format(
            f"{config_dict['capacity_factor']:.2%}"
        ))

st.markdown("---")

# Process Description
st.markdown("### 🔄 Process Flow")

st.markdown("""
```
┌─────────────────┐
│  SOLAR (UAE)    │ ⚡ MW input
│  50-100 MW PV   │
└────────┬────────┘
         │ (24h × capacity factor → kWh/day)
         │
    ┌────▼─────────────────┐
    │  ELECTROLYSIS        │
    │  2H₂O → 2H₂ + O₂      │
    │  (45 kWh/kg H₂)       │
    │  Output: H₂           │
    └────┬─────────────────┘
         │
    ┌────┴──────┬──────────────┐
    │            │              │
┌───▼──┐   ┌────▼─────┐   ┌───▼─────┐
│  H₂  │   │  N₂ SEP  │   │ Haber-  │
│      │   │  (0.5)   │   │ Bosch   │
└───┬──┘   └────┬─────┘   │ Reactor │
    │           │          │ (8 kWh) │
    │      ┌────▼──┐      └───┬─────┘
    │      │ N₂    │          │
    │      └───────┤          │
    └──────────────┤          │
                 ┌─▼──┐       │
                 │ HB │◄──────┘
                 │    │
                 └─┬──┘
                   │
              ┌────▼────┐
              │ NH₃      │ ← Main Product
              │ 2-10 t/d │
              └────┬─────┘
                   │
              ┌────▼──────────────┐
              │ Optional: Urea    │
              │ 2NH₃ + CO₂ → Urea │
              │ (if enabled)      │
              └───────────────────┘
```
""")

st.markdown("---")

# Navigation hint
st.info("""
**Next Steps:**
1. Go to **Process Model** to adjust parameters and see detailed energy / cost breakdown
2. Review **Scenarios UAE** to compare baseline vs. green ammonia strategies
3. Use **AI Optimizer** to find best cost/CO₂ trade-off
""")

st.markdown("---")

# Footer
st.markdown(f"""
<div style='text-align: center; font-size: 0.75rem; color: #666; border-top: 1px solid #ddd; padding-top: 1rem; margin-top: 2rem;'>
<p><strong style='color: #003366'>{COMPANY_NAME}</strong> | {COMPANY_LOCATION}</p>
<p>{IP_NOTICE}</p>
</div>
""", unsafe_allow_html=True)
