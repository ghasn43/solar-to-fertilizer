"""
Page 9: Strategic Value & Global Impact
Phase 3 policy features: Food security impact, international benchmarking, hydrogen export strategy
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from core.constants import COMPANY_NAME, COMPANY_LOCATION, IP_NOTICE
from core.models import ProcessConfig
from core.process import process_model

st.set_page_config(page_title="9. Strategic Value & Global Impact | S2F-DT", layout="wide")

st.markdown(f"<div style='color:#003366'><h1>🌍 Strategic Value & Global Impact</h1></div>", unsafe_allow_html=True)

st.markdown("""
Advanced strategic analysis: food security impact, international competitive positioning, 
and hydrogen export business case for regional/global markets.
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

def calculate_ammonia_economics(config_dict):
    """Calculate basic ammonia economics."""
    config = ProcessConfig(**config_dict)
    results = process_model(config)
    
    return {
        "cost_usd_per_ton": results.cost_usd_per_ton_nh3,
        "co2_kg_per_ton": results.co2_intensity_kg_per_kg_nh3 * 1000,
    }

# ===== TABS =====

tab_food, tab_bench, tab_export = st.tabs([
    "🌾 Food Security Impact",
    "🌍 International Benchmarking",
    "💰 Hydrogen Export Strategy"
])

# ===== FOOD SECURITY TAB =====
with tab_food:
    st.markdown("## Food Security Impact Analysis")
    st.markdown("""
Calculate how local ammonia production supports UAE's agricultural capacity and food security goals.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        annual_production = st.number_input(
            "Annual Ammonia Production (MT/year)",
            min_value=10000,
            max_value=500000,
            value=50000,
            step=10000,
            help="Target annual ammonia production (local + all plants)"
        )
    
    with col2:
        urea_conversion = st.slider(
            "Conversion to Urea (%)",
            min_value=0,
            max_value=100,
            value=60,
            step=10,
            help="% of ammonia converted to urea (easier to store/transport)"
        )
    
    with col3:
        crop_mix = st.selectbox(
            "Primary Crop Focus",
            ["Mixed Crops", "Wheat & Grain", "Alfalfa (Livestock Feed)", "Dates & Perennials"],
            help="Affects nitrogen uptake efficiency"
        )
    
    st.markdown("---")
    
    # Calculate food security impact
    ammonia_for_fert = annual_production * (1 - urea_conversion/100)  # Direct use
    urea_production = annual_production * (urea_conversion/100) * 0.6  # Urea is ~60% nitrogen as ammonia-equivalent
    total_nitrogen_available = (ammonia_for_fert + urea_production) * 1000  # kg/year
    
    # Nitrogen fertiliser efficiency by crop
    efficiency_map = {
        "Mixed Crops": 0.65,
        "Wheat & Grain": 0.70,
        "Alfalfa (Livestock Feed)": 0.75,
        "Dates & Perennials": 0.50,
    }
    
    efficiency = efficiency_map[crop_mix]
    effective_nitrogen = total_nitrogen_available * efficiency
    
    # Agricultural impact
    # Rule of thumb: 1 kg nitrogen supports ~5–8 kg crop production
    crop_productivity_ratio = 6.5  # kg crop per kg nitrogen available
    crop_production_kg = effective_nitrogen * crop_productivity_ratio
    crop_production_mt = crop_production_kg / 1e9
    
    # Land supported (rough: 200 kg nitrogen/hectare/year typical)
    nitrogen_per_hectare = 200
    hectares_supported = total_nitrogen_available / nitrogen_per_hectare / 1000
    
    # Population fed (rough: 0.5 MT crops per person per year)
    population_fed_years = (crop_production_mt / 1e6) / 0.5
    people_fed_daily = int((crop_production_mt * 1e6) / (365 * 0.5))
    
    # Water savings (ammonia-based fertiliser is more water-efficient than imports + transport)
    water_saved_m3_year = (annual_production / 50) * 30  # Rough estimate
    
    st.markdown("### Agricultural Capacity Impact")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Hectares Supported", f"{int(hectares_supported):,}")
    with col2:
        st.metric("Crop Production", f"{int(crop_production_mt/1000):,}K MT")
    with col3:
        st.metric("People Fed (years)", f"{population_fed_years:.1f}")
    with col4:
        st.metric("Water Managed", f"{int(water_saved_m3_year/1e6):.0f}M m³/year")
    
    st.markdown("---")
    
    st.markdown("### Detailed Food Security Narrative")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Production Split")
        st.markdown(f"""
**Total Ammonia Production:** {annual_production:,} MT/year

- **Direct Use (Ammonia):** {ammonia_for_fert:,.0f} MT/year
  - Cost-effective for large farms
  - Immediate application
  
- **Urea Conversion:** {urea_production:,.0f} MT/year
  - Easier to store & transport
  - Better for smallholder farmers
  - Export potential
        """)
    
    with col2:
        st.markdown("#### Agricultural Support")
        st.markdown(f"""
**Crop Production Capacity:**
- Land supported: {int(hectares_supported):,} hectares
- Annual crop yield: {int(crop_production_mt/1000):,}K MT
- {crop_mix} optimized

**Population Impact:**
- Daily consumption: {people_fed_daily:,} people
- Annual buffer: {population_fed_years:.1f} years of local supply
- Local food security: ✅ Significantly improved

**Regional Benefit:**
- GCC fertiliser availability: +50,000 MT/year
- Reduced import dependency: 100% for ammonia
- Price stability: Local production buffers against spikes
        """)
    
    st.markdown("---")
    
    st.markdown("### Agricultural Value Chain")
    
    fig = go.Figure()
    
    stages = ["Ammonia\nProduction", "Fertiliser\nDistribution", "Farm\nApplication", "Crop\nProduction", "Food\nConsumption"]
    values = [
        annual_production,
        annual_production * 0.95,  # 5% loss in distribution
        annual_production * 0.90 * crop_productivity_ratio,  # Effective nitrogen used
        crop_production_mt / 1e6,  # Crop output
        crop_production_mt / 1e6,  # Food supply
    ]
    units = ["MT", "MT", "kg N", "MT crops", "MT food"]
    
    fig.add_trace(go.Funnel(
        y=stages,
        x=[v for v in values],
        textposition="inside",
        textinfo="value+label",
        marker=dict(color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']),
    ))
    
    fig.update_layout(
        title="Food Production Value Chain",
        height=400,
        showlegend=False,
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### Economic Value to Agriculture Sector")
    
    # Economic calculations
    avg_crop_price = 250  # USD/ton (wheat ~200, alfalfa ~300, dates ~1000)
    crop_economic_value = (crop_production_mt / 1e6) * avg_crop_price * 1e6
    
    farmer_income_increase = crop_economic_value * 0.4  # 40% goes to farmers
    tax_revenue = crop_economic_value * 0.1  # 10% tax equivalent
    
    econ_rows = [
        {
            "Category": "Crop Production Value",
            "Annual (USD)": f"${crop_economic_value/1e9:.1f}B",
            "10-Year (USD)": f"${crop_economic_value * 10 / 1e9:.1f}B"
        },
        {
            "Category": "Farmer Income (40% share)",
            "Annual (USD)": f"${farmer_income_increase/1e9:.2f}B",
            "10-Year (USD)": f"${farmer_income_increase * 10 / 1e9:.1f}B"
        },
        {
            "Category": "Government Tax Revenue",
            "Annual (USD)": f"${tax_revenue/1e6:.0f}M",
            "10-Year (USD)": f"${tax_revenue * 10 / 1e6:.0f}M"
        },
    ]
    
    econ_df = pd.DataFrame(econ_rows)
    st.dataframe(econ_df, use_container_width=True, hide_index=True)

# ===== INTERNATIONAL BENCHMARKING TAB =====
with tab_bench:
    st.markdown("## International Competitive Positioning")
    st.markdown("""
How does UAE's green ammonia strategy compare to other emerging hydrogen economies?
    """)
    
    st.markdown("---")
    
    # International data
    competitors = {
        "UAE (Target 2030)": {
            "capacity_mt": 150000,
            "cost_per_ton": 300,
            "co2_per_ton": 50,
            "deployment_year": 2030,
            "target_market": "Asia-Pacific + Local",
            "competitive_advantage": "Lowest cost, solar leadership",
            "color": "#0066cc"
        },
        "Saudi Arabia (ARAMCO)": {
            "capacity_mt": 200000,
            "cost_per_ton": 320,
            "co2_per_ton": 150,
            "deployment_year": 2028,
            "target_market": "Egypt, Levant",
            "competitive_advantage": "Scale, oil/gas integration",
            "color": "#ff6b6b"
        },
        "Morocco (Green H2)": {
            "capacity_mt": 100000,
            "cost_per_ton": 350,
            "co2_per_ton": 40,
            "deployment_year": 2029,
            "target_market": "North Africa, EU",
            "competitive_advantage": "Solar + wind, EU access",
            "color": "#52c41a"
        },
        "Egypt (Nitrogen Fixation)": {
            "capacity_mt": 80000,
            "cost_per_ton": 380,
            "co2_per_ton": 200,
            "deployment_year": 2031,
            "target_market": "Africa, Middle East",
            "competitive_advantage": "Agricultural focus, scale potential",
            "color": "#ffd93d"
        },
        "Oman (H2 Hub)": {
            "capacity_mt": 120000,
            "cost_per_ton": 310,
            "co2_per_ton": 70,
            "deployment_year": 2029,
            "target_market": "Asia, Europe export",
            "competitive_advantage": "Port access, strategic location",
            "color": "#ff8c42"
        },
    }
    
    st.markdown("### Regional Producer Comparison")
    
    # Create comparison table
    comparison_rows = []
    for producer, data in competitors.items():
        comparison_rows.append({
            "Country/Producer": producer,
            "Capacity (2030)": f"{data['capacity_mt']:,} MT",
            "Cost/Ton": f"${data['cost_per_ton']:.0f}",
            "CO₂/Ton": f"{data['co2_per_ton']:.0f} kg",
            "Launch": data['deployment_year'],
            "Target Market": data['target_market']
        })
    
    comp_df = pd.DataFrame(comparison_rows)
    st.dataframe(comp_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.markdown("### Cost Competitiveness (2030 Projection)")
    
    producers = list(competitors.keys())
    costs = [competitors[p]['cost_per_ton'] for p in producers]
    colors = [competitors[p]['color'] for p in producers]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=producers,
        x=costs,
        orientation='h',
        marker=dict(color=colors),
        text=[f"${c:.0f}/ton" for c in costs],
        textposition='outside',
    ))
    
    fig.add_vline(x=400, line_dash="dash", line_color="orange",
                 annotation_text="Import Baseline")
    fig.add_vline(x=350, line_dash="dash", line_color="green",
                 annotation_text="Competitive Threshold")
    
    fig.update_layout(
        title="Green Ammonia Cost Comparison (2030)",
        xaxis_title="Cost (USD/ton)",
        height=400,
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### Market Share & Competitive Positioning")
    
    # Market calculation
    regional_demand = 800000  # MT/year rough estimate
    total_capacity = sum([competitors[p]['capacity_mt'] for p in competitors])
    uae_share = (competitors["UAE (Target 2030)"]['capacity_mt'] / total_capacity) * 100
    
    market_data = []
    for producer in producers:
        capacity = competitors[producer]['capacity_mt']
        share = (capacity / total_capacity) * 100
        market_data.append({
            "Producer": producer,
            "Capacity (MT)": capacity,
            "Market Share": f"{share:.1f}%"
        })
    
    market_df = pd.DataFrame(market_data)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Regional Production by 2030")
        st.dataframe(market_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### Market Share Pie")
        fig_pie = px.pie(
            values=[competitors[p]['capacity_mt'] for p in producers],
            names=producers,
            color=producers,
            color_discrete_map={p: competitors[p]['color'] for p in producers},
            title="Regional Green Ammonia Production Share (2030)"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### Competitive Advantage Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### UAE Strengths")
        st.markdown("""
✅ **Lowest cost:** $300/ton (best solar + electricity rates)
✅ **Ultra-low carbon:** 50 kg CO₂/ton (aligns with Net Zero 2050)
✅ **Tech leadership:** First-mover in gulf + Asia markets
✅ **Diversified use:** Food security + export + re-export
✅ **Policy support:** Clear government commitment
        """)
    
    with col2:
        st.markdown("#### Competitive Threats")
        st.markdown("""
⚠️ **Saudi scale:** 200K MT (1.3× larger)
⚠️ **Morocco EU access:** Closer to European markets
⚠️ **Oman logistics:** Better port infrastructure
⚠️ **Egypt scale:** Agricultural production advantage
⚠️ **Global oversupply:** Risk if all deploy simultaneously
        """)
    
    with col3:
        st.markdown("#### Strategic Response")
        st.markdown("""
🎯 **First-mover advantage:** Launch 2027–2028 (before competitors)
🎯 **Quality premium:** "Better is green" carbon certification
🎯 **Regional hub:** Abu Dhabi/Masdar as trading center
🎯 **Tech IP:** License catalyst/electrolyser tech to others
🎯 **Partnership:** Joint ventures with Asian off-takers
        """)

# ===== EXPORT STRATEGY TAB =====
with tab_export:
    st.markdown("## Hydrogen Export Business Case")
    st.markdown("""
Evaluate ammonia/hydrogen export strategy: domestic vs export production mix,
market sizing, revenue projections, and strategic positioning.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        annual_capacity = st.number_input(
            "Annual Production Capacity (MT/year)",
            min_value=10000,
            max_value=300000,
            value=150000,
            step=10000
        )
    
    with col2:
        domestic_use_pct = st.slider(
            "Domestic Use (%)",
            min_value=0,
            max_value=100,
            value=40,
            step=10,
            help="% allocated to local food security; rest for export"
        )
    
    with col3:
        export_price_premium = st.slider(
            "Green Ammonia Price Premium (%)",
            min_value=0,
            max_value=50,
            value=15,
            step=5,
            help="Premium for certified green ammonia vs commodity price"
        )
    
    st.markdown("---")
    
    # Calculate export scenarios
    domestic_amount = annual_capacity * (domestic_use_pct / 100)
    export_amount = annual_capacity - domestic_amount
    
    base_ammonia_price = 350  # USD/ton (market price)
    export_price = base_ammonia_price * (1 + export_price_premium / 100)
    
    annual_export_revenue = export_amount * export_price
    
    # Shipping costs
    shipping_cost_per_ton = {
        "Japan": 45,
        "Singapore": 50,
        "Europe": 70,
    }
    
    # Market allocation
    market_allocation = {
        "Japan (40%)": {
            "volume_mt": export_amount * 0.40,
            "shipping_cost": shipping_cost_per_ton["Japan"],
        },
        "Singapore (30%)": {
            "volume_mt": export_amount * 0.30,
            "shipping_cost": shipping_cost_per_ton["Singapore"],
        },
        "Europe (30%)": {
            "volume_mt": export_amount * 0.30,
            "shipping_cost": shipping_cost_per_ton["Europe"],
        },
    }
    
    st.markdown("### Export Business Model")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Capacity", f"{annual_capacity:,} MT/year")
    with col2:
        st.metric("Domestic Use", f"{int(domestic_amount):,} MT")
    with col3:
        st.metric("Export Volume", f"{int(export_amount):,} MT")
    with col4:
        st.metric("Export Price", f"${export_price:.0f}/ton")
    
    st.markdown("---")
    
    st.markdown("### Revenue & Market Analysis")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Revenue Projection")
        revenue_10yr = annual_export_revenue * 10
        revenue_20yr = annual_export_revenue * 20
        
        st.markdown(f"""
**Annual Export Revenue (green premium {export_price_premium}%):**
- **Export volume:** {int(export_amount):,} MT
- **Price/ton:** ${export_price:.0f}
- **Annual revenue:** ${annual_export_revenue/1e9:.2f}B

**Long-term Projections:**
- **10-year revenue:** ${revenue_10yr/1e9:.1f}B
- **20-year revenue:** ${revenue_20yr/1e9:.1f}B

**Foreign Exchange Impact:**
- Annual FX earnings: ${annual_export_revenue*1e6:.0f}
- Currency basket benefit: Strong AED support
        """)
    
    with col2:
        st.markdown("#### Market Breakdown")
        
        market_rows = []
        for market, data in market_allocation.items():
            revenue = data['volume_mt'] * export_price
            net_revenue = revenue - (data['volume_mt'] * data['shipping_cost'])
            margin_pct = (net_revenue / revenue) * 100
            
            market_rows.append({
                "Market": market,
                "Volume (MT)": f"{int(data['volume_mt']):,}",
                "Shipping ($/ton)": data['shipping_cost'],
                "Revenue": f"${revenue/1e9:.2f}B",
                "Net Margin": f"{margin_pct:.0f}%"
            })
        
        market_df = pd.DataFrame(market_rows)
        st.dataframe(market_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.markdown("### Strategic Export Scenarios")
    
    scenarios = {
        "Scenario 1: LOCAL FOCUS (Food Security)": {
            "domestic": 60,
            "description": "Prioritize agricultural & food security (60% domestic, 40% export)",
            "strategic_value": "Maximum food security + stable export revenue",
            "export_vol_pct": 40,
        },
        "Scenario 2: BALANCED (Optimal)": {
            "domestic": 40,
            "description": "Balance local needs with export revenue (40% domestic, 60% export)",
            "strategic_value": "Food security + strong revenue + foreign exchange",
            "export_vol_pct": 60,
        },
        "Scenario 3: REVENUE MAXIMIZATION": {
            "domestic": 20,
            "description": "Maximize export revenue; import food if needed (20% domestic, 80% export)",
            "strategic_value": "Maximum foreign exchange ($300M+/year) + exports leadership",
            "export_vol_pct": 80,
        },
    }
    
    for scenario_name, scenario_data in scenarios.items():
        with st.expander(f"**{scenario_name}**", expanded=False):
            dom_pct = scenario_data['domestic']
            exp_pct = scenario_data['export_vol_pct']
            
            dom_mt = annual_capacity * (dom_pct / 100)
            exp_mt = annual_capacity * (exp_pct / 100)
            exp_rev = exp_mt * export_price
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown(f"**{scenario_data['description']}**")
                st.markdown(f"""
- Domestic allocation: {dom_pct}% ({int(dom_mt):,} MT)
- Export allocation: {exp_pct}% ({int(exp_mt):,} MT)
- Annual export revenue: ${exp_rev/1e9:.2f}B
- 10-year FX earnings: ${exp_rev * 10 / 1e9:.1f}B
                """)
            
            with col2:
                st.markdown(f"**Strategic Value:**")
                st.markdown(scenario_data['strategic_value'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Production pie
                fig = px.pie(
                    values=[dom_mt, exp_mt],
                    names=['Domestic', 'Export'],
                    title=f"Production Allocation",
                    color_discrete_map={'Domestic': '#6bcf7f', 'Export': '#0066cc'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Revenue breakdown by market
                japan_rev = exp_mt * 0.40 * export_price
                sg_rev = exp_mt * 0.30 * export_price
                eu_rev = exp_mt * 0.30 * export_price
                
                fig = px.bar(
                    x=['Japan (40%)', 'Singapore (30%)', 'Europe (30%)'],
                    y=[japan_rev, sg_rev, eu_rev],
                    title="Export Revenue by Market",
                    labels={'y': 'Annual Revenue (USD)', 'x': 'Market'}
                )
                st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### Strategic Positioning: Ammonia as Hydrogen Carrier")
    
    st.markdown("""
**Why export ammonia instead of hydrogen?**

| Factor | Liquid H₂ | Ammonia |
|--------|-----------|---------|
| **Energy density** | 120 MJ/kg | 16 MJ/kg × 17% H₂ = lower direct |
| **Shipping cost** | $200–300/ton | $45–70/ton (3–5× cheaper) |
| **Boiling point** | -253°C (difficult) | -33°C (manageable) |
| **Infrastructure** | New required | Existing ports/carriers |
| **End-use** | Direct fuel cells | Cracking to H₂ or direct power |
| **Market maturity** | Emerging | Established commodity |

**Export value chain:**
```
UAE Production → Ammonia Export → Buyer Country Cracking → Hydrogen/Power
                (low-cost bulk)   (last-mile value-add)   (end-value capture)
```

**Commercial strategy:**
- Export ammonia at bulk commodity rates ($300–350/ton)
- Buyers crack it on-site or use directly
- Japan: Import for H₂ fuel cell vehicles
- Singapore: Hub for SE Asia cracking
- Europe: Green hydrogen for industry
    """)

st.markdown("---")

# Footer
st.markdown(f"""
<div style='text-align: center; font-size: 0.75rem; color: #666; border-top: 1px solid #ddd; padding-top: 1rem; margin-top: 2rem;'>
<p><strong style='color: #003366'>{COMPANY_NAME}</strong> | {COMPANY_LOCATION}</p>
<p>{IP_NOTICE}</p>
<p><em>Phase 3 Strategic Tools: Food security impact, international benchmarking, hydrogen export strategy</em></p>
</div>
""", unsafe_allow_html=True)
