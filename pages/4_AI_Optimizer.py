"""
Page 4: AI Optimizer
"""
import streamlit as st
import pandas as pd
from core.models import ProcessConfig
from core.optimizer import grid_search_optimizer, display_top_solutions
from core.process import process_model
from core.utils import save_defaults
from core.constants import COMPANY_NAME, COMPANY_LOCATION, IP_NOTICE
import json

st.set_page_config(page_title="4. AI Optimizer | S2F-DT", layout="wide")

st.markdown(f"<div style='color:#003366'><h1>🤖 AI Optimizer</h1></div>", unsafe_allow_html=True)

st.markdown("""
Use grid-search optimization to find the best process configuration 
that minimizes cost, CO₂ intensity, or a combination of both.
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

# Optimization Settings
st.sidebar.markdown("### ⚙️ Optimizer Settings")

target_nh3 = st.sidebar.number_input(
    "Target NH₃ (tons/day)",
    min_value=1.0,
    max_value=20.0,
    value=st.session_state.process_config["target_nh3_day"],
    step=0.5
)

objective = st.sidebar.radio(
    "Minimize:",
    options=["cost", "co2", "combined"],
    format_func=lambda x: {
        "cost": "💰 Cost (USD/ton)",
        "co2": "🌍 CO₂ Intensity (kg CO₂/ton)",
        "combined": "⚖️ Combined (Cost + CO₂)",
    }[x],
    help="Choose optimization objective"
)

lambda_weight = 1.0
if objective == "combined":
    lambda_weight = st.sidebar.slider(
        "CO₂ Weight (λ)",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1,
        help="Higher = prioritize CO₂ reduction"
    )

grid_density = st.sidebar.slider(
    "Grid Density (points per dimension)",
    min_value=3,
    max_value=7,
    value=4,
    step=1,
    help="Higher = finer search, slower"
)

st.markdown("---")

# Run optimization
if st.button("▶️ Run Optimization", type="primary", use_container_width=True):
    with st.spinner("Optimizing... this may take a minute..."):
        try:
            solutions, best = grid_search_optimizer(
                target_nh3_tons_day=target_nh3,
                objective=objective,
                lambda_weight=lambda_weight,
                grid_density=grid_density,
            )
            
            st.session_state.solutions = solutions
            st.session_state.best_solution = best
            st.success("✅ Optimization Complete!")
            
        except Exception as e:
            st.error(f"Optimization Error: {str(e)}")

# Display results
if "best_solution" in st.session_state:
    best = st.session_state.best_solution
    
    st.markdown("### 🏆 Best Solution Found")
    
    col_best_a, col_best_b, col_best_c, col_best_d = st.columns(4)
    
    with col_best_a:
        st.metric("Cost (USD/ton)", f"${best['cost_usd_per_ton']:.0f}")
    with col_best_b:
        st.metric("CO₂ (kg CO₂/ton)", f"{best['co2_kg_per_ton']:.1f}")
    with col_best_c:
        st.metric("Catalyst Factor", f"{best['catalyst_factor']:.2f}")
    with col_best_d:
        st.metric("Solar Capacity (MW)", f"{best['solar_capacity_mw']:.0f}")
    
    st.markdown("---")
    
    st.markdown("### 📊 Top 10 Solutions")
    
    solutions = st.session_state.solutions
    top_df = display_top_solutions(solutions, top_n=10)
    st.dataframe(top_df, use_container_width=True)
    
    st.markdown("---")
    
    # Apply best solution to session config
    st.markdown("### 💾 Apply Best Solution")
    
    col_apply_a, col_apply_b = st.columns([2, 1])
    
    with col_apply_a:
        st.info(f"""
**Best Configuration:**
- Electrolyser Efficiency: {best['electrolyser_efficiency']:.1f} kWh/kg H₂
- Catalyst Factor: {best['catalyst_factor']:.2f}
- Solar Capacity: {best['solar_capacity_mw']:.0f} MW
- Capacity Factor: {best['capacity_factor']:.1%}
        """)
    
    with col_apply_b:
        if st.button("✅ Apply to Config", use_container_width=True):
            st.session_state.process_config["electrolyser_efficiency"] = best["electrolyser_efficiency"]
            st.session_state.process_config["catalyst_factor"] = best["catalyst_factor"]
            st.session_state.process_config["solar_capacity_mw"] = best["solar_capacity_mw"]
            st.session_state.process_config["capacity_factor"] = best["capacity_factor"]
            st.session_state.process_config["target_nh3_day"] = target_nh3
            st.success("✅ Applied! Go to Process Model to verify.")
    
    st.markdown("---")
    
    # Export best solution
    st.markdown("### 📥 Export Best Solution")
    
    best_config_dict = {
        "target_nh3_day": target_nh3,
        "solar_capacity_mw": best["solar_capacity_mw"],
        "electrolyser_efficiency": best["electrolyser_efficiency"],
        "n2_separation_energy": 0.5,
        "synthesis_energy": 8.0,
        "catalyst_factor": best["catalyst_factor"],
        "capacity_factor": best["capacity_factor"],
        "water_cost_usd_m3": 1.5,
        "electricity_cost_usd_kwh": 0.04,
        "include_urea": False,
    }
    
    json_str = json.dumps(best_config_dict, indent=2)
    
    st.download_button(
        label="📥 Download Best Config (JSON)",
        data=json_str,
        file_name="s2f_dt_best_config.json",
        mime="application/json",
    )
    
    if st.button("💾 Save as Default", use_container_width=True):
        save_defaults(best_config_dict, filepath="data/defaults.json")
        st.success("✅ Saved as defaults.json")

else:
    st.info("👈 Configure optimizer settings in the sidebar and click **Run Optimization** to get started.")

st.markdown("---")

# Optimization Explanation
with st.expander("📚 How the Optimizer Works"):
    st.markdown("""
### Algorithm Overview

The **Grid Search Optimizer** systematically explores the parameter space to find 
configurations that minimize your chosen objective.

#### Search Space
- **Electrolyser Efficiency**: 35–50 kWh/kg H₂
- **Catalyst Factor**: 0.5–1.2 (multiplier)
- **Solar Capacity**: 10–100 MW
- **Capacity Factor**: 0.15–0.35 (%)

#### Objectives
1. **Minimize Cost**: Find cheapest configuration
2. **Minimize CO₂**: Find lowest carbon footprint
3. **Minimize Combined** (Cost + λ × CO₂): Balance both

#### Complexity
- **Grid Density = 4**: ~256 evaluations (4⁴)
- **Grid Density = 5**: ~625 evaluations (5⁴)
- **Grid Density = 7**: ~2401 evaluations (7⁴)

Higher density = better solution, but slower.

#### Strategy
- Run with **grid_density=4** for quick exploration (~30 sec)
- Run with **grid_density=5–6** for final optimization (~2-5 min)
- Use **λ weight** to shift trade-off between cost and CO₂

#### Disclaimer
This is a **deterministic grid search**, not a stochastic optimizer. 
For more advanced optimization, integrate with SciPy's minimize() or Optuna.
    """)

st.markdown("---")

# Footer
st.markdown(f"""
<div style='text-align: center; font-size: 0.75rem; color: #666; border-top: 1px solid #ddd; padding-top: 1rem; margin-top: 2rem;'>
<p><strong style='color: #003366'>{COMPANY_NAME}</strong> | {COMPANY_LOCATION}</p>
<p>{IP_NOTICE}</p>
</div>
""", unsafe_allow_html=True)
