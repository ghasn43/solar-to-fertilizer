"""
Page 0: Help & Tutorial
Interactive guide to the S2F-DT application
"""
import streamlit as st
from core.constants import COMPANY_NAME, COMPANY_LOCATION, IP_NOTICE

st.set_page_config(page_title="0. Help & Tutorial | S2F-DT", layout="wide")

st.markdown(f"<div style='color:#003366'><h1>📚 Help & Tutorial</h1></div>", unsafe_allow_html=True)

st.markdown("""
Welcome to the **Solar-to-Fertiliser Digital Twin (S2F-DT)** interactive tutorial.  
Learn how to use the app, understand each page, and explore real-world scenarios.
""")

# Tabs for organization
tab_quickstart, tab_welcome, tab_tour, tab_usecases, tab_glossary, tab_tech = st.tabs([
    "⚡ Quick Start",
    "🎯 Welcome",
    "📖 Page Tour",
    "💼 Use Cases",
    "📚 Glossary",
    "🔬 Technical"
])

# ===== QUICK START TAB =====
with tab_quickstart:
    st.markdown("## Quick Start Guide")
    
    st.markdown("### 1️⃣ Install")
    with st.expander("Option A: Automated (Windows)", expanded=False):
        st.code("""cd Solar-to-Fertiliser\\s2f_dt
.\\setup.bat""", language="bash")
    
    with st.expander("Option B: Automated (Mac/Linux)", expanded=False):
        st.code("""cd Solar-to-Fertiliser/s2f_dt
bash setup.sh""", language="bash")
    
    with st.expander("Option C: Manual", expanded=False):
        st.code("""python -m venv venv
# Windows: venv\\Scripts\\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt""", language="bash")
    
    st.markdown("### 2️⃣ Run")
    st.code("streamlit run app.py", language="bash")
    st.info("App opens at `http://localhost:8501`")
    
    st.markdown("### 3️⃣ First 5 Steps")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
1. **Overview**
2. **Process Model**
3. **Scenarios UAE**
4. **AI Optimizer**
5. **Report Export**
        """)
    
    with col2:
        st.markdown("""
See executive KPIs
Adjust all parameters
Compare 3 scenarios
Search for best config
Download PDF & JSON
        """)
    
    st.markdown("### 📊 Key Sliders at a Glance")
    slider_data = {
        "NH₃ Production": "1–20 tons/day",
        "Solar Capacity": "10–100 MW",
        "Electrolyser Eff.": "35–50 kWh/kg (↓ = better)",
        "Catalyst Factor": "0.5–1.2 (↓ = breakthrough)",
        "Capacity Factor": "15–35% (UAE typical: 25%)",
        "Electricity Cost": "0.03–0.08 $/kWh (UAE: 0.04)",
    }
    st.table(slider_data)

# ===== WELCOME TAB =====
with tab_welcome:
    st.markdown("## Welcome & Purpose")
    
    st.markdown("### The Problem")
    st.markdown("""
- **Ammonia** is essential for fertiliser, but traditional production uses fossil fuels
- ~2% of global CO₂ emissions come from ammonia synthesis
- **UAE challenge:** 100% of ammonia is imported; no local production
    """)
    
    st.markdown("### Why UAE Context Matters")
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
✅ **Opportunities**
- Abundant solar energy (5–6 kWh/m²/day)
- Net Zero 2050 commitment
- Growing food security needs
        """)
    
    with col2:
        st.warning("""
⚠️ **Challenges**
- All ammonia imported
- Limited freshwater
- Reliance on distant producers
        """)
    
    st.markdown("### What S2F-DT Does")
    st.info("""
**S2F-DT is a digital twin simulation** that models ammonia production powered by solar:

**Process Flow:**
```
Air (N₂) + Water (H₂O) + Solar Power
         ↓ Electrolysis ↓
         Hydrogen (H₂)
         ↓ N₂ Separation & Synthesis ↓
         Ammonia (NH₃)
         ↓ Optional: Urea Conversion ↓
         Fertiliser (NH₃ or Urea)
```

**Outputs:** Cost, Energy, Water, CO₂ intensity, PDF reports, JSON configs
    """)
    
    st.markdown("### What S2F-DT Is **NOT**")
    st.error("""
❌ Not a design blueprint or engineering specification  
❌ Not a site-specific environmental assessment  
❌ Not a financial model with capital expenditure details  
❌ Not a quantum chemistry simulator  
✓ **Educational and exploration tool for stakeholders**
    """)
    
    st.markdown("### Disclaimer")
    st.warning("""
**This is a simulation and educational prototype.**
All outputs are estimates based on simplified models. Actual plant performance will vary based on site conditions, 
technology selection, operational practices, and market conditions. Use for scenario planning and learning only.
    """)

# ===== PAGE TOUR TAB =====
with tab_tour:
    st.markdown("## App Tour: Page by Page")
    
    pages_tour = {
        "🏠 Overview": {
            "Purpose": "Get the big picture and understand what inputs matter",
            "Key Metrics": [
                "NH₃ Production (tons/day) — Daily output",
                "Total Energy (MWh/day) — Solar power needed",
                "Cost (USD/ton) — Production cost per ton",
                "CO₂ Intensity (kg CO₂/ton) — Carbon footprint",
                "Water Usage (m³/day) — Daily water consumption",
            ],
            "What to Do": "Read KPIs, explore Process Assumptions accordion"
        },
        "⚙️ Process Model": {
            "Purpose": "Deep dive into every input and see how each affects outputs",
            "Key Controls": [
                "Target NH₃ (tons/day) — Daily production goal",
                "Solar Capacity (MW) — Farm size",
                "Electrolyser Efficiency — Technology maturity (lower = better)",
                "Catalyst Factor — Efficiency multiplier (0.5 = breakthrough)",
                "Capacity Factor — % time solar runs at full power",
            ],
            "What to Do": "Adjust sliders, watch outputs update, read Energy Breakdown chart"
        },
        "🌍 Scenarios UAE": {
            "Purpose": "Compare 3 realistic pathways for UAE ammonia production",
            "Scenarios": {
                "S1 (Import Baseline)": "Status quo: ~$400/ton, ~2000 kg CO₂/ton",
                "S2 (Green Today)": "Solar-powered with current tech: ~$350/ton, ~50 kg CO₂/ton",
                "S3 (Future Catalyst)": "Breakthrough technology: ~$300/ton, ~20 kg CO₂/ton",
            },
            "What to Do": "Adjust S3 catalyst factor, read Strategic Analysis, compare cost/CO₂ charts"
        },
        "🤖 AI Optimizer": {
            "Purpose": "Automatically find the cheapest/cleanest configuration",
            "Options": [
                "Choose objective: Minimize Cost / CO₂ / Combined",
                "Set grid density: 3–7 (higher = finer search, slower)",
                "Run optimization (1–10 minutes)",
            ],
            "What to Do": "Configure optimizer, run search, view Top 10 solutions, apply best to config"
        },
        "⚛️ Quantum-Ready": {
            "Purpose": "Explore emerging catalyst technologies (forward-looking)",
            "Important": "This is a PLACEHOLDER, not real quantum chemistry",
            "What to Do": "Explore candidate catalysts, use for scenario planning narratives"
        },
        "📊 Report Export": {
            "Purpose": "Generate professional outputs for presentations and records",
            "Outputs": [
                "PDF Report — 1-page professional summary with charts",
                "JSON Configuration — Machine-readable config for archiving",
            ],
            "What to Do": "Generate PDF, download JSON, share with colleagues"
        },
    }
    
    for page_name, details in pages_tour.items():
        with st.expander(f"**{page_name}**", expanded=False):
            st.markdown(f"**Purpose:** {details['Purpose']}")
            
            if "Key Metrics" in details:
                st.markdown("**Key Metrics:**")
                for metric in details["Key Metrics"]:
                    st.markdown(f"- {metric}")
            
            if "Key Controls" in details:
                st.markdown("**Key Controls:**")
                for control in details["Key Controls"]:
                    st.markdown(f"- {control}")
            
            if "Scenarios" in details:
                st.markdown("**The Scenarios:**")
                for scenario, desc in details["Scenarios"].items():
                    st.markdown(f"- **{scenario}:** {desc}")
            
            if "Options" in details:
                st.markdown("**Options:**")
                for option in details["Options"]:
                    st.markdown(f"- {option}")
            
            if "Outputs" in details:
                st.markdown("**Outputs:**")
                for output in details["Outputs"]:
                    st.markdown(f"- {output}")
            
            if "Important" in details:
                st.warning(f"⚠️ **{details['Important']}**")
            
            st.markdown(f"**What to Do:** {details['What to Do']}")

# ===== USE CASES TAB =====
with tab_usecases:
    st.markdown("## Real-World Use Cases")
    
    usecase_a, usecase_b, usecase_c, usecase_d = st.tabs([
        "A: Executive Demo",
        "B: Farm Planning",
        "C: CO₂ Story",
        "D: Catalyst Future"
    ])
    
    with usecase_a:
        st.markdown("### A. Executive Demo (3 Minutes)")
        st.markdown("**Goal:** Show why local ammonia is viable")
        st.markdown("""
**Path:**
1. **Overview page** → Point out KPIs
   - "Cost is $X/ton (beating imports at ~$400)"
   - "CO₂ is Y kg/ton (95% cleaner than shipped)"
   
2. **Scenarios UAE** → Show cost & CO₂ charts
   - "S2 undercuts imports"
   - "S3 is ultra-low-carbon"
   
3. **Report Export** → Generate PDF
   - Email to board with executive summary

**Talking Points:**
- ✅ Cost-competitive with current imports
- ✅ Major CO₂ reduction (climate story)
- ✅ Supports UAE food security and greening mandate
        """)
    
    with usecase_b:
        st.markdown("### B. Farm / Greenhouse Planning")
        st.markdown("**Goal:** Estimate energy, water, and cost for your farm")
        st.markdown("**Scenario:** 1000-hectare farm needs 10 tons/day ammonia")
        st.markdown("""
**Steps:**
1. **Process Model** page
2. Adjust **Target NH₃** → 10 tons/day
3. Check **Electricity Cost** → $0.04/kWh (UAE standard)
4. Check **Water Cost** → $1.5/m³ (desalination)
5. Adjust **Capacity Factor** → 0.24 (your region)
6. **Read outputs:**
   - Solar capacity required (MW)
   - Daily energy (MWh)
   - Cost per ton
   - Water per day (m³)
7. **Share with your solar developer** the config JSON

**Key Actions:**
| Output | Share With |
|--------|-----------|
| Solar capacity (MW) | Solar EPC contractor |
| Daily energy (MWh) | Feasibility team |
| Cost per ton | Budget proposal |
| Water m³/day | Water authority |
        """)
    
    with usecase_c:
        st.markdown("### C. CO₂ Reduction Story (Climate Impact)")
        st.markdown("**Goal:** Show ESG/climate impact for investors or regulators")
        st.markdown("""
**Steps:**
1. **Overview** page → Write down CO₂ value (~50 kg/ton)
2. **Scenarios UAE** → Note baseline (~2000 kg/ton)
3. **Calculate impact:**
   - If 10 tons/day: Annual = 3,650 tons
   - Solar: 3,650 × 50 = 182,500 kg CO₂ = 182.5 metric tons
   - Import: 3,650 × 2000 = 7,300 metric tons CO₂
   - **Savings: 7,120 metric tons CO₂/year** (like removing 1,500 cars)

4. **Report Export** → Use PDF in ESG report, investor deck

**Talking Points:**
- Aligns with UAE's Net Zero 2050 commitment
- Each ton removes ~2,000 kg CO₂ vs. imports
- Scalable to replace all imported ammonia over time
- Green agriculture story
        """)
    
    with usecase_d:
        st.markdown("### D. Future Catalyst Breakthrough")
        st.markdown("**Goal:** Show impact of next-generation catalyst (5-year horizon)")
        st.markdown("""
**Steps:**
1. **Process Model** page → Note **Catalyst Factor = 1.0** (baseline)
   - Observe Cost/ton and CO₂/ton
   
2. **Adjust Catalyst Factor** → 0.7 (30% better)
   - **Watch cost and energy drop!**
   
3. **Scenarios UAE** → Update S3 catalyst factor to 0.7
   - Compare S2 (today) vs S3 (future)
   
4. **Calculate benefit:**
   - Cost savings: $X per ton
   - CO₂ reduction: Y kg per ton
   
5. **AI Optimizer** → Run for "Combined" objective
   - See how optimization allocates resources
   
6. **Export PDF** as "Future Scenario 2027–2030"

**Talking Points:**
- Quantum chemistry could unlock 20–30% gains
- Small efficiency jumps → large cost/carbon savings
- R&D investment in catalysts has high ROI
- UAE research institutions could lead breakthrough
        """)

# ===== GLOSSARY TAB =====
with tab_glossary:
    st.markdown("## Glossary of Terms")
    
    glossary = {
        "Ammonia (NH₃)": "Colorless gas, essential for nitrate fertilisers. Made from nitrogen (air) + hydrogen (water).",
        "Nitrogen Fixation": "Process of converting N₂ (inert) → reactive compounds. Natural & industrial processes.",
        "Urea": "Stable, solid fertiliser made from ammonia. Easier to transport and store than ammonia gas.",
        "Stoichiometry": "Science of chemical ratios. Our model: N₂ + 3H₂ → 2NH₃",
        "Electrolysis": "Electric current splits water (H₂O) → hydrogen (H₂) + oxygen (O₂). Current tech: ~45 kWh/kg H₂.",
        "Haber-Bosch": "Industrial ammonia synthesis: N₂ + 3H₂ → 2NH₃ at high T & P. Standard since 1909.",
        "Capacity Factor": "Fraction of time a plant runs at full power. Solar: 20–30%. Our model: 0.15–0.35.",
        "kWh": "Kilowatt-hour. Unit of electrical energy. 1 kWh = power of 1 kW for 1 hour.",
        "MW": "Megawatt. Unit of power. 1 MW = 1000 kW. Solar farm sizes in MW.",
        "Cost per Ton": "Total production cost ÷ output. Includes: electricity, water, capital, labor, margin.",
        "CO₂ Intensity": "Carbon footprint per unit product. Includes: embedded emissions in electricity, transport, operations.",
        "Emissions Factor": "kg CO₂ per kWh. Solar: ~0.01. UAE grid: ~0.48. Import baseline: ~1.0.",
        "Catalyst": "Substance speeding up reactions without being consumed. In ammonia: metals (Fe, Ru) on supports.",
        "Digital Twin": "Virtual simulation of a real system. Allows: what-if scenarios without building real plant.",
        "Quantum Chemistry": "Computational chemistry using quantum mechanics. Can predict new catalyst structures (research phase).",
    }
    
    for term, definition in glossary.items():
        st.markdown(f"**{term}**  \n{definition}")

# ===== TECHNICAL TAB =====
with tab_tech:
    st.markdown("## Technical Details for Reviewers")
    
    st.markdown("### Stoichiometry & Ratios")
    st.markdown("""
**Chemical Equation:**
```
N₂ + 3H₂ → 2NH₃
```

**Stoichiometric Ratios:**
- 1 kg N₂ + 3 kg H₂ → 4 kg NH₃
- H₂ per NH₃: 0.75 kg
- N₂ per NH₃: 0.25 kg
    """)
    
    st.markdown("### Energy Balance")
    st.markdown("""
**Total Energy = Electrolysis + N₂ Separation + Synthesis**

| Component | Formula | Typical Value |
|-----------|---------|---|
| **Electrolysis** | mass_H₂ × efficiency | 35–50 kWh/kg H₂ |
| **N₂ Separation** | mass_N₂ × separation_energy | 0.5–2.0 kWh/kg |
| **Synthesis** | mass_NH₃ × synthesis_energy × catalyst_factor | 0.5–15 kWh/kg |

**Daily Energy (MWh)** = Sum of above / 1000
    """)
    
    st.markdown("### CO₂ Intensity")
    st.markdown("""
**Formula:**
```
CO₂ intensity = (Daily Energy × Emissions Factor) / Production
```

**Emissions Factors:**
| Source | kg CO₂/kWh | Notes |
|--------|---|---|
| Solar | 0.01 | Lifecycle (manufacturing, installation) |
| UAE Grid | 0.48 | Gas + solar mix (time-dependent) |
| Imported Ammonia | ~1.0 | Fossil fuel production + transport |
    """)
    
    st.markdown("### Model Assumptions")
    st.markdown("""
All parameters are defined in `core/constants.py`:
- Stoichiometry ratios
- Energy factors (kWh)
- Cost factors (USD)
- Emissions factors (kg CO₂)
- Default capacity factor
- Default catalyst factor

All values are **configurable** via `data/defaults.json` and UI sliders.
    """)
    
    st.markdown("### Testing & Validation")
    st.markdown("""
Run tests locally:
```bash
cd Solar-to-Fertiliser/s2f_dt
pip install pytest
pytest tests/ -v
```

**Test coverage:**
- Stoichiometry & mass balance
- Energy calculations vs. efficiency
- Water requirements
- Cost calculations
- CO₂ intensity
    """)
    
    st.markdown("### Model Limitations")
    st.markdown("""
- **Linear cost model** — Real plants have economies of scale
- **Simplified water balance** — No condensation recovery
- **No grid integration** — Single-site assumption
- **Placeholder quantum scorer** — Not physics-based
- **Single pathway** — Only Haber-Bosch; no other syntheses
- **Uniform capacity factor** — Same everywhere; actually site-dependent
    """)

st.markdown("---")

# Footer
st.markdown(f"""
<div style='text-align: center; font-size: 0.75rem; color: #666; border-top: 1px solid #ddd; padding-top: 1rem; margin-top: 2rem;'>
<p><strong style='color: #003366'>{COMPANY_NAME}</strong> | {COMPANY_LOCATION}</p>
<p>{IP_NOTICE}</p>
<p><em>For detailed tutorial, see: docs/TUTORIAL.md on GitHub</em></p>
</div>
""", unsafe_allow_html=True)
