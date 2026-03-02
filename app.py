"""
Main Streamlit application: Solar-to-Fertiliser Digital Twin (S2F-DT)
"""
import streamlit as st
from core.constants import COMPANY_NAME, COMPANY_LOCATION, IP_NOTICE

# Page configuration
st.set_page_config(
    page_title="S2F-DT | Experts Group FZE",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    [data-testid="stViewerBadgeContainer"] {display: none;}
    .header-footer {
        font-size: 0.75rem;
        color: #666;
        text-align: center;
        padding: 0.5rem 0;
        border-top: 1px solid #ddd;
        margin-top: 2rem;
    }
    .company-branding {
        color: #003366;
        font-weight: bold;
    }
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .scenario-highlight {
        background-color: #e6f2ff;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #003366;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown(f"""
<div class='company-branding'>
⚡ {COMPANY_NAME}
</div>
{COMPANY_LOCATION}
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### Navigation
Use the pages menu to navigate between:
- **Overview**: Projects overview & KPI summary
- **Process Model**: Detailed process simulation
- **Scenarios UAE**: Compare production scenarios
- **AI Optimizer**: Find optimal configurations
- **Quantum-Ready**: Catalysts scoring
- **Report Export**: PDF & JSON export
""")

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
### IP & Confidentiality
{IP_NOTICE}
""")

# Main content
st.title("☀️🧪 Solar-to-Fertiliser Digital Twin (S2F-DT)")
st.markdown("**Virtual Project Simulator for UAE Green Ammonia Production**")

st.markdown("""
---
## Welcome to S2F-DT

This digital twin simulates the production of fertiliser (ammonia, urea) from:
- **Solar electricity** ⚡
- **Ambient air** (N₂ extraction)
- **Water** (electrolysis for H₂)

### Process Overview
**Air → N₂** | **Water → H₂** (electrolysis) | **N₂ + 3H₂ → 2NH₃** (Haber-Bosch) | **Optional: 2NH₃ + CO₂ → Urea**

### Key Features
✅ **Stoichiometric Mass Balance**: Track N₂, H₂, NH₃, and water flows  
✅ **Energy Balance**: Electrolysis, N₂ separation, and synthesis energy blocks  
✅ **CO₂ Intensity**: Compare solar vs. grid electricity emissions  
✅ **Cost Analysis**: OpEx (electricity, water) + CapEx amortization  
✅ **Scenario Comparison**: Baseline vs. Green Ammonia vs. Future Catalyst  
✅ **AI Optimizer**: Grid-search for cost/CO₂ minimization  
✅ **Quantum-Ready**: Mock catalyst scoring (extensible to IBM Quantum)  
✅ **PDF Export**: 1-page report with branding & IP notice  
✅ **JSON Config**: Export/import configurations  

### How to Use
1. Go to **Process Model** to configure parameters
2. Review **Scenarios UAE** for strategic comparisons
3. Use **AI Optimizer** to explore design space
4. Check **Quantum-Ready** for catalyst insights
5. Export results via **Report Export**

---

### Technology Stack
- **Backend**: Python 3.11+, Streamlit, Pandas, NumPy
- **Visualization**: Plotly, Matplotlib
- **Reporting**: ReportLab (PDF), JSON
- **Extensible**: Quantum chemistry ready (mock → IBM Quantum)

---
""")

# Initialize session state for shared config
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

st.markdown("---")
st.markdown(f"""
<div class='header-footer'>
<p><strong>Experts Group FZE</strong> | {COMPANY_LOCATION}</p>
<p>All Rights Reserved. Confidential. © Experts Group FZE</p>
</div>
""", unsafe_allow_html=True)
