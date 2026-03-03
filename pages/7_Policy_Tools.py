"""
Page 7: Policy Tools
Sensitivity analysis, break-even calculator, regional scaling, national goals
for policy makers and government stakeholders
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from core.constants import COMPANY_NAME, COMPANY_LOCATION, IP_NOTICE
from core.models import ProcessConfig
from core.process import process_model

st.set_page_config(page_title="7. Policy Tools | S2F-DT", layout="wide")

st.markdown(f"<div style='color:#003366'><h1>🏛️ Policy Tools & Analysis</h1></div>", unsafe_allow_html=True)

st.markdown("""
Strategic analysis tools for government stakeholders, policy makers, and cabinet briefings.
Explore sensitivity, subsidy requirements, regional deployment, and national scaling scenarios.
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

def calculate_ammonia_economics(config_dict, electricity_cost=None, water_cost=None, 
                                carbon_tax=None, subsidy=None):
    """Calculate cost and emissions for given configuration."""
    config = config_dict.copy()
    if electricity_cost is not None:
        config["electricity_cost_usd_kwh"] = electricity_cost
    if water_cost is not None:
        config["water_cost_usd_m3"] = water_cost
    
    # Create ProcessConfig object
    process_config = ProcessConfig(**config)
    results = process_model(process_config)
    
    cost = results.cost_usd_per_ton_nh3
    co2 = results.co2_intensity_kg_per_kg_nh3 * 1000  # Convert kg/kg to kg/ton
    
    # Apply carbon tax if specified (adds cost per ton)
    if carbon_tax is not None:
        cost_from_carbon = co2 * carbon_tax / 1000  # co2 is in kg/ton, convert to cost
        cost += cost_from_carbon
    
    # Apply subsidy if specified (reduces cost)
    if subsidy is not None:
        cost -= subsidy
    
    return {
        "cost_usd_per_ton": cost,
        "co2_kg_per_ton": co2,
        "energy_mwh_day": results.electricity_kwh_day / 1000,
        "water_m3_day": results.water_m3_day,
        "co2_metric_tons_year": (co2 / 1000) * config_dict["target_nh3_day"] * 365,
    }

# Regional data for UAE
EMIRATES_DATA = {
    "Abu Dhabi": {
        "solar_irradiance": 5.8,
        "capacity_factor": 0.26,
        "electricity_cost": 0.035,
        "water_cost": 1.2,
        "water_scarcity": "Medium",
        "land_availability": "High",
        "description": "Best solar resources, excellent infrastructure, growing agriculture demand"
    },
    "Dubai": {
        "solar_irradiance": 5.5,
        "capacity_factor": 0.24,
        "electricity_cost": 0.045,
        "water_cost": 2.0,
        "water_scarcity": "High",
        "land_availability": "Low",
        "description": "Good solar, limited land, high water costs, export-focused"
    },
    "Sharjah": {
        "solar_irradiance": 5.6,
        "capacity_factor": 0.25,
        "electricity_cost": 0.040,
        "water_cost": 1.8,
        "water_scarcity": "High",
        "land_availability": "Low",
        "description": "Moderate resources, growing agriculture sector"
    },
    "Al Ain": {
        "solar_irradiance": 5.7,
        "capacity_factor": 0.25,
        "electricity_cost": 0.042,
        "water_cost": 1.5,
        "water_scarcity": "Medium",
        "land_availability": "High",
        "description": "Strong agriculture, good solar, agricultural focus"
    },
    "Masdar City": {
        "solar_irradiance": 5.9,
        "capacity_factor": 0.27,
        "electricity_cost": 0.030,
        "water_cost": 1.0,
        "water_scarcity": "Low",
        "land_availability": "High",
        "description": "World-class renewable hub, lowest costs, green tech focus"
    },
}

# Main tabs
tab_sensitivity, tab_breakeven, tab_regional, tab_national = st.tabs([
    "📊 Sensitivity Analysis",
    "⚖️ Break-Even Calculator",
    "🗺️ Regional Deployment",
    "📈 National Scaling"
])

# ===== SENSITIVITY ANALYSIS TAB =====
with tab_sensitivity:
    st.markdown("## Sensitivity Analysis: Policy Levers")
    st.markdown("""
How sensitive is ammonia economics to policy variables? Adjust each lever to see impact on cost and emissions.
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Policy Variable Ranges")
        
        # Sliders for sensitivity
        electricity_range = st.slider(
            "Electricity Cost Range (USD/kWh)",
            min_value=0.02,
            max_value=0.10,
            value=(0.03, 0.08),
            step=0.005,
            help="Current UAE rate ~0.04; subsidized ~0.03; market high ~0.08"
        )
        
        water_range = st.slider(
            "Water Cost Range (USD/m³)",
            min_value=0.5,
            max_value=3.0,
            value=(1.0, 2.5),
            step=0.1,
            help="Desalinated water; recycled ~1.0; market ~2.0; scarcity premium ~3.0"
        )
        
        carbon_tax_range = st.slider(
            "Carbon Tax Range (USD/kg CO₂)",
            min_value=0.0,
            max_value=0.50,
            value=(0.0, 0.25),
            step=0.01,
            help="Carbon tax incentive; ranges from $0 (none) to $0.25+ per kg"
        )
        
        tech_improvement = st.slider(
            "Technology Learning Rate (% annual improvement)",
            min_value=0.0,
            max_value=10.0,
            value=5.0,
            step=0.5,
            help="Electrolyser efficiency improvement over time"
        )
        
        # Calculate baseline
        baseline = calculate_ammonia_economics(config_dict)
    
    with col2:
        st.metric("Baseline Cost", f"${baseline['cost_usd_per_ton']:.0f}/ton")
        st.metric("Baseline CO₂", f"{baseline['co2_kg_per_ton']:.0f} kg/ton")
        st.metric("Annual CO₂ Savings", f"{baseline['co2_metric_tons_year']:.0f} MT")
    
    st.markdown("---")
    
    # Tornado chart: Show individual impacts
    st.markdown("### Impact Ranking (Tornado Chart)")
    st.markdown("Each policy variable's impact on cost/ton, holding others constant:")
    
    # Calculate impacts
    impacts = []
    
    # Electricity impact
    config_low_elec = config_dict.copy()
    config_low_elec["electricity_cost_usd_kwh"] = electricity_range[0]
    result_low_elec = calculate_ammonia_economics(config_low_elec)
    elec_impact = baseline["cost_usd_per_ton"] - result_low_elec["cost_usd_per_ton"]
    impacts.append(("Electricity Subsidy", elec_impact))
    
    # Water impact
    config_low_water = config_dict.copy()
    config_low_water["water_cost_usd_m3"] = water_range[0]
    result_low_water = calculate_ammonia_economics(config_low_water)
    water_impact = baseline["cost_usd_per_ton"] - result_low_water["cost_usd_per_ton"]
    impacts.append(("Water Cost Reduction", water_impact))
    
    # Carbon tax impact
    config_carbon = config_dict.copy()
    result_carbon = calculate_ammonia_economics(config_carbon, carbon_tax=carbon_tax_range[1])
    carbon_impact = result_carbon["cost_usd_per_ton"] - baseline["cost_usd_per_ton"]
    impacts.append(("Carbon Tax (incentive)", carbon_impact))
    
    # Technology impact
    config_tech = config_dict.copy()
    # Adjust efficiency based on learning rate (5% improvement = 5% lower kWh needed)
    config_tech["electrolyser_efficiency"] = config_dict["electrolyser_efficiency"] * (1 - tech_improvement/100)
    result_tech = calculate_ammonia_economics(config_tech)
    tech_impact = baseline["cost_usd_per_ton"] - result_tech["cost_usd_per_ton"]
    impacts.append(("Technology Improvement", tech_impact))
    
    # Sort by magnitude
    impacts.sort(key=lambda x: abs(x[1]), reverse=True)
    
    # Create tornado chart
    fig_tornado = go.Figure()
    
    variables = [x[0] for x in impacts]
    values = [x[1] for x in impacts]
    colors = ['green' if v > 0 else 'red' for v in values]
    
    fig_tornado.add_trace(go.Bar(
        y=variables,
        x=values,
        orientation='h',
        marker=dict(color=colors),
        text=[f"${v:+.0f}/ton" for v in values],
        textposition='outside',
    ))
    
    fig_tornado.update_layout(
        title="Impact on Cost/Ton (Relative to Baseline)",
        xaxis_title="Cost Change (USD/ton)",
        yaxis_title="Policy Variable",
        height=400,
        showlegend=False,
    )
    
    st.plotly_chart(fig_tornado, use_container_width=True)
    
    st.markdown("**Key Insight:** Electricity cost is typically 3–5× more impactful than water cost. Prioritize electricity subsidies or long-term PPAs.")
    
    # Sensitivity table
    st.markdown("### Detailed Sensitivity Table")
    
    sensitivity_rows = []
    
    # Electricity scenarios
    for price in np.linspace(electricity_range[0], electricity_range[1], 5):
        result = calculate_ammonia_economics(config_dict, electricity_cost=price)
        sensitivity_rows.append({
            "Policy": "Electricity Price",
            "Parameter": f"${price:.3f}/kWh",
            "Cost/Ton": f"${result['cost_usd_per_ton']:.0f}",
            "vs Import": f"{result['cost_usd_per_ton'] - 400:+.0f}",
            "Viable?": "✅ Yes" if result['cost_usd_per_ton'] <= 400 else "⚠️ Subsidy needed"
        })
    
    # Carbon tax scenarios
    for tax in np.linspace(carbon_tax_range[0], carbon_tax_range[1], 4):
        result = calculate_ammonia_economics(config_dict, carbon_tax=tax)
        sensitivity_rows.append({
            "Policy": "Carbon Tax",
            "Parameter": f"${tax:.2f}/kg CO₂",
            "Cost/Ton": f"${result['cost_usd_per_ton']:.0f}",
            "vs Import": f"{result['cost_usd_per_ton'] - 400:+.0f}",
            "Viable?": "✅ Yes" if result['cost_usd_per_ton'] <= 400 else "⚠️ Subsidy needed"
        })
    
    sensitivity_df = pd.DataFrame(sensitivity_rows)
    st.dataframe(sensitivity_df, use_container_width=True)

# ===== BREAK-EVEN TAB =====
with tab_breakeven:
    st.markdown("## Break-Even Analysis: Policy Requirements")
    st.markdown("""
What policy interventions are needed to achieve cost parity with imports, or a target cost?
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        target_cost = st.number_input(
            "Target Cost (USD/ton)",
            min_value=200.0,
            max_value=500.0,
            value=350.0,
            step=10.0,
            help="Goal: cost-competitive with imports (~$400/ton)"
        )
    
    with col2:
        current_import_price = st.number_input(
            "Current Import Price (USD/ton)",
            min_value=300.0,
            max_value=600.0,
            value=400.0,
            step=10.0,
            help="Typical ammonia import price from Middle East"
        )
    
    with col3:
        time_horizon = st.selectbox(
            "Time Horizon",
            ["Now (2026)", "Near-term (2028)", "Medium-term (2030)", "Long-term (2035)"],
            help="Assume technology improvements with time"
        )
    
    st.markdown("---")
    
    # Calculate baseline
    baseline_result = calculate_ammonia_economics(config_dict)
    baseline_cost = baseline_result["cost_usd_per_ton"]
    gap = baseline_cost - target_cost
    
    st.markdown(f"### Current Status")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Baseline Cost", f"${baseline_cost:.0f}/ton")
    with col2:
        st.metric("Target Cost", f"${target_cost:.0f}/ton")
    with col3:
        st.metric("Gap to Close", f"${gap:+.0f}/ton")
    with col4:
        pct_gap = (gap / baseline_cost) * 100
        st.metric("% of Baseline", f"{pct_gap:+.0f}%")
    
    st.markdown("---")
    
    st.markdown("### Policy Pathways to Achieve Target")
    
    # Option 1: Electricity subsidy alone
    st.markdown("#### Option 1️⃣: Electricity Subsidy")
    current_elec = config_dict["electricity_cost_usd_kwh"]
    results_by_elec = []
    for elec_price in np.linspace(0.02, 0.08, 15):
        result = calculate_ammonia_economics(config_dict, electricity_cost=elec_price)
        if abs(result["cost_usd_per_ton"] - target_cost) < 5:  # Close to target
            required_elec = elec_price
            break
    else:
        required_elec = None
    
    if required_elec and required_elec < current_elec:
        subsidy_amount = (current_elec - required_elec) * 1000  # Convert to $/MWh
        subsidy_per_ton = gap
        st.info(f"""
✅ **Electricity subsidy path:**
- **Required rate:** ${required_elec:.3f}/kWh
- **Subsidy magnitude:** ${subsidy_amount:.0f}/MWh (current: $40/MWh typical)
- **Annual cost (10 plants × 3,650 tons):** ${subsidy_per_ton * 10 * 3650 / 1e9:.2f}B
        """)
        
        # Chart: cost vs electricity price
        elec_prices = np.linspace(0.02, 0.08, 20)
        costs = [calculate_ammonia_economics(config_dict, electricity_cost=p)["cost_usd_per_ton"] 
                 for p in elec_prices]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=elec_prices,
            y=costs,
            mode='lines+markers',
            name='Cost/ton',
            line=dict(color='blue', width=3)
        ))
        fig.add_hline(y=target_cost, line_dash="dash", line_color="green", 
                     annotation_text=f"Target: ${target_cost:.0f}/ton")
        fig.add_hline(y=current_import_price, line_dash="dash", line_color="orange",
                     annotation_text=f"Import: ${current_import_price:.0f}/ton")
        fig.update_layout(
            title="Cost vs. Electricity Price",
            xaxis_title="Electricity Price (USD/kWh)",
            yaxis_title="Cost (USD/ton)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Electricity subsidy alone cannot achieve target cost with current technology.")
    
    st.markdown("---")
    
    # Option 2: Direct subsidy + current prices
    st.markdown("#### Option 2️⃣: Direct Subsidy per Ton")
    direct_subsidy = gap
    if direct_subsidy > 0:
        annual_budget_10plants = direct_subsidy * 10 * 3650 / 1e9
        st.info(f"""
✅ **Direct subsidy path:**
- **Subsidy per ton:** ${direct_subsidy:.0f}/ton
- **Annual cost (10 plants):** ${annual_budget_10plants:.2f}B
- **2030 cumulative (4 plants phased):** ${annual_budget_10plants * 15 * 0.5:.2f}B
        """)
    else:
        st.success(f"✅ Already cost-competitive at ${baseline_cost:.0f}/ton (better than import ${current_import_price:.0f}/ton)")
    
    st.markdown("---")
    
    # Option 3: Carbon tax
    st.markdown("#### Option 3️⃣: Carbon Tax Incentive")
    baseline_co2 = baseline_result["co2_kg_per_ton"]
    co2_advantage = (400 * 1000 - baseline_co2) / 1000  # kg CO₂ saved per ton vs import baseline
    
    required_carbon_tax = abs(gap / (baseline_co2 / 1000)) if gap < 0 else None
    
    if required_carbon_tax and required_carbon_tax > 0:
        st.info(f"""
✅ **Carbon tax incentive path:**
- **Required carbon tax:** ${required_carbon_tax:.2f}/kg CO₂
- **Rationale:** Solar ammonia saves {baseline_co2:.0f} kg CO₂/ton vs. ~2000 kg import baseline
- **Fair value:** 95% reduction × $X/ton CO₂ offset credit
        """)
    else:
        st.info(f"""
✅ **Carbon advantage:**
- **CO₂ savings:** {2000 - baseline_co2:.0f} kg CO₂/ton vs. imports
- **Carbon credit value:** {2000 - baseline_co2:.0f} kg × $0.15/kg = ${(2000 - baseline_co2) * 0.15:.0f}/ton (offset)
        """)
    
    st.markdown("---")
    
    st.markdown("### Summary Table: Policy Scenarios")
    
    policy_scenarios = []
    
    # Scenario 1: Current
    policy_scenarios.append({
        "Scenario": "Current (no support)",
        "Electricity ($/kWh)": f"{config_dict['electricity_cost_usd_kwh']:.3f}",
        "Subsidy ($/ton)": "$0",
        "Cost/Ton": f"${baseline_cost:.0f}",
        "vs Import": f"{baseline_cost - current_import_price:+.0f}",
        "Viability": "⚠️ Marginal" if baseline_cost > current_import_price else "✅ Good"
    })
    
    # Scenario 2: Moderate support
    if required_elec and required_elec < current_elec:
        mod_result = calculate_ammonia_economics(config_dict, electricity_cost=required_elec)
        policy_scenarios.append({
            "Scenario": "Moderate support",
            "Electricity ($/kWh)": f"${required_elec:.3f}",
            "Subsidy ($/ton)": f"${gap/2:.0f}",
            "Cost/Ton": f"${mod_result['cost_usd_per_ton']:.0f}",
            "vs Import": f"{mod_result['cost_usd_per_ton'] - current_import_price:+.0f}",
            "Viability": "✅ Excellent"
        })
    
    # Scenario 3: Full support
    policy_scenarios.append({
        "Scenario": "Full support (target achieved)",
        "Electricity ($/kWh)": "$0.035",
        "Subsidy ($/ton)": f"${gap:.0f}",
        "Cost/Ton": f"${target_cost:.0f}",
        "vs Import": f"{target_cost - current_import_price:+.0f}",
        "Viability": "✅ Excellent"
    })
    
    scenario_df = pd.DataFrame(policy_scenarios)
    st.dataframe(scenario_df, use_container_width=True)

# ===== REGIONAL SCALING TAB =====
with tab_regional:
    st.markdown("## Regional Deployment Analysis")
    st.markdown("Compare economics and impact across UAE emirates.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_emirate = st.selectbox(
            "Select Emirate to Detail",
            list(EMIRATES_DATA.keys()),
            index=0
        )
    
    with col2:
        plants_size = st.number_input(
            "Plant Size (tons/day)",
            min_value=1.0,
            max_value=50.0,
            value=10.0,
            step=1.0
        )
    
    st.markdown("---")
    
    # Show selected emirate details
    emirate_data = EMIRATES_DATA[selected_emirate]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Solar Irradiance", f"{emirate_data['solar_irradiance']} kWh/m²/day")
    with col2:
        st.metric("Capacity Factor", f"{emirate_data['capacity_factor']:.1%}")
    with col3:
        st.metric("Electricity Cost", f"${emirate_data['electricity_cost']:.3f}/kWh")
    with col4:
        st.metric("Water Cost", f"${emirate_data['water_cost']:.2f}/m³")
    
    st.markdown(f"**{selected_emirate}:** {emirate_data['description']}")
    
    st.markdown("---")
    
    # Calculate for selected emirate
    regional_config = config_dict.copy()
    regional_config["electricity_cost_usd_kwh"] = emirate_data["electricity_cost"]
    regional_config["water_cost_usd_m3"] = emirate_data["water_cost"]
    regional_config["capacity_factor"] = emirate_data["capacity_factor"]
    regional_config["target_nh3_day"] = plants_size
    
    regional_result = calculate_ammonia_economics(regional_config)
    
    st.markdown(f"### Economics for {plants_size}-ton/day Plant in {selected_emirate}")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Cost/Ton", f"${regional_result['cost_usd_per_ton']:.0f}")
    with col2:
        cost_gap = 400 - regional_result['cost_usd_per_ton']
        st.metric("vs Import ($400)", f"{cost_gap:+.0f}")
    with col3:
        st.metric("CO₂/Ton", f"{regional_result['co2_kg_per_ton']:.0f} kg")
    with col4:
        st.metric("Daily Energy", f"{regional_result['energy_mwh_day']:.0f} MWh")
    with col5:
        st.metric("Annual CO₂ Saved", f"{regional_result['co2_metric_tons_year']:.0f} MT")
    
    st.markdown("---")
    
    # Comparison across all emirates
    st.markdown("### Regional Comparison Table")
    
    regional_comparison = []
    
    for emirate_name, edata in EMIRATES_DATA.items():
        ec = config_dict.copy()
        ec["electricity_cost_usd_kwh"] = edata["electricity_cost"]
        ec["water_cost_usd_m3"] = edata["water_cost"]
        ec["capacity_factor"] = edata["capacity_factor"]
        ec["target_nh3_day"] = plants_size
        
        eres = calculate_ammonia_economics(ec)
        
        regional_comparison.append({
            "Emirate": emirate_name,
            "Cost/Ton": f"${eres['cost_usd_per_ton']:.0f}",
            "vs Import": f"{eres['cost_usd_per_ton'] - 400:+.0f}",
            "CO₂/Ton": f"{eres['co2_kg_per_ton']:.0f} kg",
            "Ranking": "🥇 Best" if emirate_name == selected_emirate else "🥈" if emirate_name == "Masdar City" else "🥉"
        })
    
    regional_df = pd.DataFrame(regional_comparison)
    st.dataframe(regional_df, use_container_width=True)
    
    st.markdown("---")
    
    # Regional heatmap
    st.markdown("### Regional Economics Heatmap")
    
    heatmap_data = []
    emirates_list = list(EMIRATES_DATA.keys())
    
    for emirate_name in emirates_list:
        edata = EMIRATES_DATA[emirate_name]
        ec = config_dict.copy()
        ec["electricity_cost_usd_kwh"] = edata["electricity_cost"]
        ec["water_cost_usd_m3"] = edata["water_cost"]
        ec["capacity_factor"] = edata["capacity_factor"]
        ec["target_nh3_day"] = plants_size
        
        eres = calculate_ammonia_economics(ec)
        heatmap_data.append([emirate_name, "Cost/Ton", eres['cost_usd_per_ton']])
        heatmap_data.append([emirate_name, "CO₂/Ton", eres['co2_kg_per_ton']])
    
    heatmap_df = pd.DataFrame(heatmap_data, columns=["Emirate", "Metric", "Value"])
    
    fig_cost = px.bar(
        heatmap_df[heatmap_df["Metric"] == "Cost/Ton"],
        x="Emirate",
        y="Value",
        color="Value",
        color_continuous_scale="RdYlGn_r",
        title=f"Cost/Ton by Emirate ({plants_size}-ton/day plant)"
    )
    fig_cost.add_hline(y=400, line_dash="dash", line_color="orange", annotation_text="Import Baseline")
    
    st.plotly_chart(fig_cost, use_container_width=True)

# ===== NATIONAL SCALING TAB =====
with tab_national:
    st.markdown("## National Scaling to Strategic Goals")
    st.markdown("""
Calculate the investment, resources, and impact needed to achieve UAE's ammonia self-sufficiency targets.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        self_sufficiency_target = st.slider(
            "Self-Sufficiency Target (%)",
            min_value=10,
            max_value=100,
            value=50,
            step=10,
            help="% of current ammonia imports to replace with local production"
        )
    
    with col2:
        target_year = st.selectbox(
            "Target Year",
            [2028, 2030, 2033, 2035],
            index=1,
            help="Timeline for deployment"
        )
    
    with col3:
        plant_size = st.number_input(
            "Standard Plant Size (tons/day)",
            min_value=5.0,
            max_value=50.0,
            value=10.0,
            step=5.0
        )
    
    st.markdown("---")
    
    # UAE ammonia consumption estimates
    uae_ammonia_imports_annual = 550000  # metric tons/year (rough estimate)
    
    target_production_annual = uae_ammonia_imports_annual * (self_sufficiency_target / 100)
    target_production_daily = target_production_annual / 365
    plants_needed = int(np.ceil(target_production_daily / plant_size))
    
    st.markdown(f"### Deployment Requirements")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Current Imports", f"{uae_ammonia_imports_annual/1000:.0f}K MT/year")
    with col2:
        st.metric("Target (Local)", f"{target_production_annual/1000:.0f}K MT/year")
    with col3:
        st.metric("Plants Needed", f"{plants_needed} units")
    with col4:
        st.metric("Deployment Timeline", f"{target_year - 2026} years")
    
    st.markdown("---")
    
    # Calculate resource requirements
    config_national = config_dict.copy()
    config_national["target_nh3_day"] = plant_size
    result_national = calculate_ammonia_economics(config_national)
    
    # Solar capacity (rough: 10 MW per 10 ton/day)
    solar_mw_per_plant = (plant_size / 10) * 50  # scales from 50 MW baseline for 5 tons/day
    total_solar_mw = plants_needed * solar_mw_per_plant
    
    # CapEx estimate (rough: $100-150M per plant with balance of system)
    capex_per_plant_millions = plant_size * 15  # $15M per ton/day capacity
    total_capex_billions = (plants_needed * capex_per_plant_millions) / 1000
    
    # Annual energy consumption
    daily_energy_per_plant = result_national["energy_mwh_day"]
    annual_energy_gwh = (plants_needed * daily_energy_per_plant * 365) / 1000
    
    # Water consumption
    daily_water_per_plant = result_national["water_m3_day"]
    annual_water_km3 = (plants_needed * daily_water_per_plant * 365) / 1e9
    
    # CO₂ avoided
    annual_co2_avoided = plants_needed * result_national["co2_metric_tons_year"]
    
    # Jobs (rough estimate: 100 jobs per plant during construction, 20 during operations)
    construction_jobs = plants_needed * 100
    operations_jobs = plants_needed * 20
    
    st.markdown("### Infrastructure Requirements")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Solar Capacity", f"{total_solar_mw:,.0f} MW")
    with col2:
        st.metric("Annual Energy", f"{annual_energy_gwh:,.0f} GWh")
    with col3:
        st.metric("Annual Water", f"{annual_water_km3:.2f} km³")
    with col4:
        st.metric("Annual CO₂ Avoided", f"{annual_co2_avoided:,.0f} MT")
    
    st.markdown("### Financial & Economic Impact")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total CapEx", f"${total_capex_billions:.1f}B")
    with col2:
        annual_opex = plants_needed * plant_size * 365 * (result_national["cost_usd_per_ton"] * 0.2)  # Rough OpEx
        st.metric("Annual OpEx (est.)", f"${annual_opex/1e9:.2f}B")
    with col3:
        st.metric("Construction Jobs", f"{construction_jobs:,}")
    with col4:
        st.metric("Operations Jobs", f"{operations_jobs:,}")
    
    st.markdown("---")
    
    # Comparison: Local vs Import
    st.markdown("### Local vs. Imported Ammonia: Strategic Comparison")
    
    comparison_data = {
        "Metric": [
            "Annual Cost",
            "Annual CO₂ Emissions",
            "Water Consumption",
            "Energy Source",
            "Supply Security",
            "Technology Control",
            "Skills Development"
        ],
        "Imported Baseline": [
            f"${target_production_annual * 400 / 1e9:.1f}B",
            f"{target_production_annual * 2000 / 1e9:.1f}M MT CO₂",
            "Embedded in imports",
            "Fossil fuels (foreign)",
            "❌ Dependent on suppliers",
            "❌ Foreign ownership",
            "❌ Limited"
        ],
        "Local (Solar-Powered)": [
            f"${target_production_annual * result_national['cost_usd_per_ton'] / 1e9:.1f}B",
            f"{annual_co2_avoided/1e9:.1f}M MT CO₂ (avoided)",
            f"{annual_water_km3:.2f} km³ (managed)",
            "Solar (renewable, local)",
            "✅ Controlled locally",
            "✅ UAE tech leadership",
            "✅ Thousands of jobs"
        ]
    }
    
    comparison_table = pd.DataFrame(comparison_data)
    st.dataframe(comparison_table, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Phased deployment schedule
    st.markdown("### Suggested Phased Deployment Schedule")
    
    years_available = target_year - 2026
    plants_per_phase = int(np.ceil(plants_needed / 3))  # 3 phases
    
    phase_data = []
    for phase in range(1, 4):
        year = 2026 + (years_available // 3) * phase
        cumulative_plants = min(plants_per_phase * phase, plants_needed)
        phase_annual_prod = cumulative_plants * plant_size * 365 / 1000
        
        phase_data.append({
            "Phase": f"Phase {phase}",
            "Target Year": year,
            "Plants Built": cumulative_plants,
            "Annual Production": f"{phase_annual_prod:.0f}K MT",
            "Cumulative CapEx": f"${cumulative_plants * capex_per_plant_millions / 1000:.1f}B",
            "Status": "Already underway" if phase == 1 else "Planned" if phase == 2 else "Future"
        })
    
    phase_df = pd.DataFrame(phase_data)
    st.dataframe(phase_df, use_container_width=True)
    
    st.markdown("---")
    
    # Policy recommendations
    st.markdown("### Policy Recommendations for Success")
    
    recommendations = [
        ("🔌 **Energy Policy**", "Lock in long-term renewable electricity at < $0.035/kWh via PPAs"),
        ("💦 **Water Strategy**", "Allocate treated/recycled water (not freshwater) for desalination"),
        ("📊 **Incentive Program**", "Time-limited subsidy or tax credit to bridge cost gap (5–10 years)"),
        ("🏢 **Industrial Zone**", "Designate special economic zone for ammonia cluster (Al Ain or Masdar)"),
        ("👥 **Workforce Development**", "Partner with universities for electrolyser & catalyst R&D"),
        ("📈 **Phased Rollout**", f"Start with 1–2 plants (2027–2028), scale to {plants_needed} by {target_year}"),
    ]
    
    for title, detail in recommendations:
        st.markdown(f"**{title}**  \n{detail}")

st.markdown("---")

# Footer
st.markdown(f"""
<div style='text-align: center; font-size: 0.75rem; color: #666; border-top: 1px solid #ddd; padding-top: 1rem; margin-top: 2rem;'>
<p><strong style='color: #003366'>{COMPANY_NAME}</strong> | {COMPANY_LOCATION}</p>
<p>{IP_NOTICE}</p>
<p><em>Policy tools for government stakeholders. All calculations based on simplified models; use for strategic planning only.</em></p>
</div>
""", unsafe_allow_html=True)
