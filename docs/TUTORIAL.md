# Solar-to-Fertiliser Digital Twin (S2F-DT)
## Complete User Tutorial

**Experts Group FZE** — Abu Dhabi, UAE  
*All Rights Reserved. Confidential. © Experts Group FZE*

---

## 📚 Table of Contents
1. [Welcome & Purpose](#welcome--purpose)
2. [What You Need (Prerequisites)](#what-you-need-prerequisites)
3. [Getting Started](#getting-started)
4. [App Tour: Page by Page](#app-tour-page-by-page)
5. [Step-by-Step Use Cases](#step-by-step-use-cases)
6. [Common Mistakes & Troubleshooting](#common-mistakes--troubleshooting)
7. [Glossary](#glossary)
8. [For Technical Reviewers](#for-technical-reviewers)

---

## Welcome & Purpose

### The Problem We're Solving

Ammonia (NH₃) is essential for fertiliser, but traditional production is energy-intensive and carbon-heavy:
- **Haber-Bosch process** requires temperatures >400°C and fossil fuels
- ~2% of global CO₂ emissions come from ammonia synthesis
- Middle East regions import 100% of their ammonia fertiliser

### Why UAE Context Matters

The UAE faces unique opportunities and challenges:
- ✅ **Abundant solar energy** (5–6 kWh/m²/day, world-class resources)
- ✅ **Greening mandate**: UAE Net Zero 2050 commitment
- ✅ **Food security**: Growing agricultural demand, limited water
- ⚠️ **Current gap**: All ammonia imported, relying on distant producers

### What S2F-DT Does

S2F-DT is a **simulation tool** — a "digital twin" — that models ammonia production powered by solar electricity:

**Process Flow:**
```
Air (N₂) + Water (H₂O) + Solar Power (kWh)
         ↓
   Electrolysis (H₂ generation)
         ↓
   N₂ Separation & Synthesis
         ↓
   Ammonia (NH₃) → Urea (optional)
         ↓
   Cost, Energy, Water, and CO₂ metrics
```

### What S2F-DT Is **NOT**

- ❌ Not a design blueprint or engineering specification
- ❌ Not a site-specific environmental assessment
- ❌ Not a financial model with capital expenditure details
- ❌ Not a quantum chemistry simulator (placeholder only)
- ✓ Educational and exploration tool for stakeholders

> **Disclaimer:** This is a **simulation and educational prototype**. All outputs are estimates based on simplified models. Actual plant performance will vary based on site conditions, technology selection, operational practices, and market conditions. Use for scenario planning and learning only.

---

## What You Need (Prerequisites)

### System Requirements
- **Python 3.11+** (or 3.10 minimum)
- **Windows, Mac, or Linux** (any OS that runs Python)
- **Internet connection** (optional — app runs offline, but Streamlit Cloud requires it)
- **~500 MB disk space** for dependencies

### Installation Steps

#### Option 1: Automated (Recommended)

**On Windows:**
```bash
# Download the repo, then:
cd Solar-to-Fertiliser\s2f_dt
.\setup.bat
```

**On Mac/Linux:**
```bash
# Download the repo, then:
cd Solar-to-Fertiliser/s2f_dt
bash setup.sh
```

#### Option 2: Manual Installation

```bash
# 1. Install Python 3.11 or newer
python --version

# 2. Clone or download the repository
cd Solar-to-Fertiliser/s2f_dt

# 3. Create a virtual environment (optional but recommended)
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

### Optional: Customize Defaults

Edit `data/defaults.json` to change starting values:
```json
{
  "target_nh3_day": 5.0,
  "solar_capacity_mw": 50.0,
  "electrolyser_efficiency": 45.0,
  "electricity_cost_usd_kwh": 0.04,
  "capacity_factor": 0.25,
  ...
}
```

Changes take effect the next time you run the app.

---

## Getting Started

### First Launch
When you open the app, you'll see a **sidebar on the left** and the **main content area** in the center.

**Sidebar** contains:
- 📊 Page selector (6 pages to explore)
- ⚙️ Input controls (sliders, numbers, dropdown menus)
- 📥 Configuration buttons

**Main area** displays:
- 📈 Charts and tables
- 📝 Explanations and KPIs
- 💾 Export buttons (PDF, JSON)

### Navigation

Click any page name in the sidebar to jump to it:
1. **🏠 Overview** — Executive summary & key assumptions
2. **⚙️ Process Model** — Detailed parameter inputs
3. **🌍 Scenarios UAE** — Compare 3 contrasting scenarios
4. **🤖 AI Optimizer** — Search for best configurations
5. **⚛️ Quantum-Ready** — Catalyst scoring (emerging tech)
6. **📊 Report Export** — Generate PDF & JSON outputs

---

## App Tour: Page by Page

### Page 1: Overview

**Purpose:** Get the big picture and understand what inputs matter.

#### Key Metrics at the Top
- **NH₃ Production (tons/day)** — How much ammonia you're making daily
- **Total Energy (MWh/day)** — Solar power needed to feed the system
- **Cost (USD/ton)** — What each ton costs to produce
- **CO₂ Intensity (kg CO₂/ton)** — Carbon footprint per ton
- **Water Usage (m³/day)** — Fresh/desalinated water consumption

#### What These Mean

| Metric | Why It Matters | Good Range |
|--------|------------------|------------|
| **NH₃ tons/day** | Fertiliser production capacity | 1–20 tons (site-dependent) |
| **Energy (MWh)** | Required solar panel size | Lower = smaller solar farm |
| **Cost (USD/ton)** | Competitive vs. imports (~$350–450) | <$400 = cost-competitive |
| **CO₂ (kg/ton)** | Climate impact (import ~2000 kg/ton) | <100 = low-carbon |
| **Water (m³/day)** | Desalination load (UAE concern) | Minimize where possible |

#### Process Assumptions Section
Click **"📋 Process Assumptions Open to explore:"
- **Stoichiometry** — Chemical ratios (N₂ + 3H₂ → 2NH₃)
- **Energy requirements** — Electrolysis, synthesis, separation
- **Cost factors** — Electricity, water, amortized capital
- **Emissions** — Solar vs grid electricity CO₂ intensity
- **Caveats** — Linear cost model, no economies of scale yet

---

### Page 2: Process Model

**Purpose:** Deep dive into every input and see how each one affects outputs.

#### Input Controls (Left Sidebar)

1. **Target NH₃ Production (tons/day)**
   - **Range:** 1–20 tons/day
   - **What it does:** Sets the goal daily output
   - **Try it:** Increase it → watch Energy, Cost, Water rise

2. **Solar Capacity (MW)**
   - **Range:** 10–100 MW
   - **What it does:** Size of solar farm (determines available kWh)
   - **Try it:** Decrease it → watch Cost go up (less efficient at small scale)

3. **Electrolyser Efficiency (kWh/kg H₂)**
   - **Range:** 35–50 kWh/kg
   - **What it does:** Technology maturity (lower = better)
   - **Try it:** Lower it to 38 → Cost drops, Energy drops

4. **N₂ Separation Energy (kWh/kg N₂)**
   - **Range:** 0.5–2.0 kWh/kg
   - **What it does:** How hard it is to capture nitrogen from air
   - **Try it:** Increase it → Cost and Energy rise

5. **Synthesis Energy (kWh/kg NH₃)**
   - **Range:** 0.5–15 kWh/kg
   - **What it does:** Energy for Haber-Bosch reactor (N₂ + H₂ → NH₃)
   - **Try it:** Typical value is ~8; very sensitive to process conditions

6. **Catalyst Factor (multiplier)**
   - **Range:** 0.5–1.2
   - **What it does:** Efficiency multiplier (0.5 = best breakthrough tech, 1.0 = baseline)
   - **Try it:** Lower it → Energy and Cost drop significantly

7. **Capacity Factor (%)**
   - **Range:** 15–35%
   - **What it does:** Fraction of time solar farm runs at full power (weather, dust)
   - **Why:** UAE typical = 25%; desert = lower; monitored sites = higher

8. **Electricity Cost (USD/kWh)**
   - **Range:** 0.03–0.08 USD/kWh
   - **Why it matters:** Major cost driver; UAE has advantage (~0.04)
   - **Try it:** Increase to 0.08 → Cost per ton jumps ~50%

9. **Water Cost (USD/m³)**
   - **Range:** 1–3 USD/m³
   - **Why it matters:**Esisal water (reverse osmosis) adds cost
   - **Try it:** Increase to 2.5 → impacts cost but not major

10. **Include Urea (Checkbox)**
    - **What it does:** Convert ammonia to urea (optional product)
    - **Effect:** Increases cost slightly, extends shelf life

#### Energy Breakdown Chart
Shows where your power goes:
- **Electrolysis** — Usually 70–80%
- **N₂ Separation** — ~5–10%
- **Synthesis** — ~10–15%

**Insight:** Electrolyser efficiency is your biggest lever.

#### Output Table
Shows calculated results:
- Daily energy (MWh)
- Required solar MW (calculated)
- Cost per ton
- Water per day
- CO₂ intensity

---

### Page 3: Scenarios UAE

**Purpose:** Compare 3 realistic pathways for UAE ammonia production.

#### The Three Scenarios

**Scenario 1: Imported Baseline**
- Status quo: UAE buys ammonia from Middle East producers
- **Cost:** ~$400/ton (historical)
- **CO₂:** ~2000 kg/ton (ship transport + fossil fuel production)
- **Why included:** Benchmark to beat

**Scenario 2: UAE Green (Today)**
- Local solar-powered ammonia with current technology
- Assumes current electrolyser efficiency (~45 kWh/kg H₂)
- Solar capacity factor typical for UAE (25%)
- **Expected Cost:** $350–380/ton (competitive!)
- **Expected CO₂:** ~50 kg/ton (95% reduction)
- **Why:** Solar + grid mix = low emissions, but not zero

**Scenario 3: Future Catalyst (2027–2030)**
- Breakthrough in catalyst efficiency (next 5 years)
- Catalyst factor = 0.7–0.8 (vs. 1.0 baseline)
- Same solar capacity, better yield
- **Expected Cost:** $300–340/ton (significant savings)
- **Expected CO₂:** ~20 kg/ton (ultra-low carbon)
- **Why it matters:** Small efficiency gains → large cost/carbon savings

#### How to Use This Page

1. **Read the comparison table** across S1, S2, S3
2. **Adjust S3 catalyst factor** in the sidebar to see impact
   - Adjust to 0.5 → "what if we get a breakthrough?"
   - Adjust to 1.0 → "what if we don't innovate?"
3. **Compare the two charts**
   - Left: Cost comparison → S2 beats imports
   - Right: CO₂ comparison → S3 is ultra-clean
4. **Read Strategic Analysis**
   - Cost-competitiveness section explains market viability
   - Carbon reduction section explains climate impact

#### Supporting UAE Greening
At the bottom, you'll find a **narrative** explaining:
- How local ammonia supports food security
- Alignment with UAE Net Zero 2050
- Synergy with hydrogen exports

---

### Page 4: AI Optimizer

**Purpose:** Automatically find the fastest/cheapest/cleanest configuration.

#### What Is Optimization?

Instead of manually adjusting sliders, the optimizer searches thousands of configurations to find the best one.

**It explores:**
- Electrolyser efficiency (35–50 kWh/kg)
- Catalyst factor (0.5–1.2)
- Solar capacity (10–100 MW)
- Capacity factor (15–35%)

#### Input Controls

1. **Target NH₃ (tons/day)**
   - The amount you want to produce; optimizer finds best way to make it

2. **Minimize: (choose objective)**
   - **💰 Cost** — Find the cheapest configuration
   - **🌍 CO₂** — Find the cleanest configuration
   - **⚖️ Combined** — Balance cost + CO₂

3. **CO₂ Weight (λ, if Combined)**
   - **Low (0.1):** Strongly favor cost
   - **Medium (1.0):** Equal weight to cost and CO₂
   - **High (5.0):** Strongly favor CO₂ reduction

4. **Grid Density (points per dimension)**
   - **3 or 4:** Quick search (~1 minute)
   - **5 or 6:** Thorough search (~3–5 minutes)
   - **7:** Exhaustive (~10+ minutes)

#### How to Run It

1. Adjust settings in the sidebar
2. Click **"▶️ Run Optimization"**
3. Wait for the search (indicator shows progress)
4. View results:
   - **Best Solution Found** — Top KPIs
   - **Top 10 Solutions** — Ranked alternatives
   - **Apply to Config** button → Use the best result

#### Interpreting Results

The **top 10 table** shows:
- **Rank** — 1st is best for your objective
- **Cost (USD/ton)** — Production cost
- **CO₂ (kg/ton)** — Carbon intensity
- **Catalyst Factor** — Efficiency multiplier
- **Solar (MW)** — Required capacity
- **Electrolysis (kWh/kg)** — Technology maturity

**Key insight:** Optimizer usually finds that **lower electricity cost + high capacity** beats high efficiency.

#### Export & Apply

- **Apply to Config** — Use best result in other pages
- **Download JSON** — Save the configuration for records
- **Save as Default** — Make this your starting point next time

---

### Page 5: Quantum-Ready

**Purpose:** Explore emerging catalyst technologies (forward-looking, not yet deployed).

#### What Is the "Quantum Score"?

This page uses a **surrogate model** — a stand-in placeholder — that mimics how quantum chemistry might discover better catalysts.

**Important:** This is **NOT real quantum chemistry**. It's a:
- ✓ Placeholder for future integration
- ✓ Educational demonstration
- ✓ Way to show how quantum hits could help
- ❌ NOT scientifically validated yet

#### How It Works

1. Shows 10 candidate catalysts ranked by a simulated "quantum score"
2. Each candidate has:
   - **Catalyst ID** — Identifier
   - **Quantum Score** — Simulated effectiveness (higher = better)
   - **Potential Energy Reduction** — Hypothetical savings if deployed
3. The top-ranked candidate shows impact in:
   - Cost/ton (if this catalyst were real)
   - CO₂/ton (if this catalyst were real)

#### How to Use It

- **Explore the candidate list** → See what "could be" with future breakthroughs
- **Click on a candidate** → See its projected impact
- **Use in narratives** → "If quantum discovers a 30% catalyst, savings could be $X/ton"

#### Honest Disclaimers

- 🔬 Rankings are seeded randomly (reproducible but not physics-based)
- 🎲 Actual quantum discovery is unpredictable
- 📊 Use for scenario planning only, not predictions

---

### Page 6: Report Export

**Purpose:** Generate professional outputs for presentations and records.

#### PDF Report

Generates a **1-page professional summary** that includes:
- Your chosen configuration (NH₃ tons/day, solar MW, etc.)
- Key metrics (Cost, CO₂, Energy, Water)
- Energy breakdown chart
- Cost vs. Import baseline
- Emissions reduction story
- Footer with company branding

**To generate PDF:**
1. Adjust your configuration (any page)
2. Go to **Report Export**
3. Click **"📄 Generate PDF Report"**
4. Click **"📥 Download Report.pdf"**
5. Use in presentations, emails, stakeholder briefings

**File format:** A4 landscape, clean design, professional appearance.

#### JSON Configuration

Exports your exact configuration as a machine-readable file:
```json
{
  "target_nh3_day": 5.0,
  "solar_capacity_mw": 50.0,
  "electrolyser_efficiency": 45.0,
  "capacity_factor": 0.25,
  "electricity_cost_usd_kwh": 0.04,
  ...
}
```

**Use JSON for:**
- Archiving your analysis
- Sharing exact parameters with colleagues
- Importing into other tools
- Version control (store in Git/SharePoint)

**To export JSON:**
1. Go to **Report Export**
2. Click **"📥 Download Configuration.json"**
3. Store with your notes/email thread

---

## Step-by-Step Use Cases

### Use Case A: Executive Demo (3-Minute Version)

**Goal:** Quickly show leadership why local ammonia is viable.

**Path:**
1. Open app → **Overview page** ✓
2. Point out the KPIs:
   - "Cost is $X/ton (beating import baseline of ~$400)"
   - "CO₂ is $Y kg/ton (95% cleaner than shipped ammonia)"
   - "Water use is Z m³/day (managed via desalination)"
3. Navigate to **Scenarios UAE** ✓
4. Show the **cost comparison chart** (S2 undercuts imports)
5. Show the **CO₂ comparison chart** (S2 + S3 are dramatically lower)
6. Read aloud the **Strategic Analysis** boxes (30 seconds each)
7. Go to **Report Export** ✓
8. Generate + download PDF
9. Close: "...and this PDF summarizes everything for your board deck."

**Talking points:**
- ✅ Cost-competitive with current imports
- ✅ Major CO₂ reduction (climate story)
- ✅ Supports UAE food security and greening mandate
- ✅ Scalable with UAE's growing solar capacity

---

### Use Case B: UAE Farm / Greenhouse Planning

**Goal:** Estimate energy, water, and cost for a specific farm size.

**Scenario:** You manage a 1000-hectare farm in Al Ain and need 10 tons/day ammonia (ammonium nitrate fertiliser).

**Steps:**

1. **Open app** → **Process Model** page ✓

2. **Set Target NH₃:**
   - Adjust slider to **10 tons/day** ✓
   - *Note: right sidebar updates in real time*

3. **Adjust Electricity Cost:**
   - UAE typical: **$0.04/kWh** ✓
   - *Leave at default if you're getting wholesale solar power*

4. **Adjust Water Cost:**
   - Local desalination: **$1.5/m³** ✓
   - *Confirm with your water supplier*

5. **Check Capacity Factor:**
   - Al Ain region: typical **0.23–0.26** (slightly higher than Abu Dhabi)
   - Adjust to **0.24** ✓

6. **Read the output table:**
   - Daily energy needed: **[see calculated value]** MWh
   - Solar capacity required: **[see calculated value]** MW
   - Cost per ton: **[see calculated value]** USD
   - Water per day: **[see calculated value]** m³

7. **Talk to your solar developer:**
   - "I need X MW of solar capacity on [site]"
   - "Annual output will be ~Y MWh"
   - Cost envelope: $[cost/ton] per ton ammonia

8. **Go to Report Export** ✓
   - Generate PDF
   - Email to your engineering team with the config JSON

**Key outputs to act on:**
| Output | Use |
|--------|-----|
| Solar capacity (MW) | Bid to solar EPC contractor |
| Daily energy (MWh) | Feasibility study for your site |
| Cost per ton | Budget proposal |
| Water m³/day | Water authority planning |

---

### Use Case C: CO₂ Reduction Story (Climate Impact)

**Goal:** Show how solar-powered ammonia supports UAE's Net Zero 2050 commitment.

**Scenario:** You're presenting to an ESG committee or investor relations team.

**Steps:**

1. **Open app** → **Overview** page ✓
   - Write down the **CO₂ Intensity** value shown
   - *(default: ~50 kg CO₂/ton)*

2. **Go to Scenarios UAE** page ✓

3. **Read the comparison:**
   - Baseline (imported): **~2000 kg CO₂/ton**
   - S2 (solar green): **~50 kg CO₂/ton**
   - **Reduction: 97.5% less carbon** ✓

4. **Calculate impact (for your narrative):**
   - If you make 10 tons/day:
     - **Annual production:** 3,650 tons
     - **Annual CO₂ equivalent:** 3,650 × 50 = 182,500 kg = **182.5 metric tons CO₂** (solar)
     - **vs Imported:** 3,650 × 2000 = 7,300,000 kg = **7,300 metric tons CO₂**
     - **Annual savings: ~7,120 metric tons CO₂** (equivalent to ~1,500 cars off the road for a year)

5. **Go to Report Export** ✓
   - Generate PDF
   - Use in ESG report, investor presentation, regulatory filing

**Talking points:**
- "This aligns with UAE's Net Zero 2050 commitment"
- "Each ton of solar ammonia removes ~2,000 kg CO₂ vs. imports"
- "Scalable to replace all imported ammonia over time"
- "Green agriculture story: fertiliser and emissions reduction"

---

### Use Case D: Future Catalyst Breakthrough Story

**Goal:** Show impact of next-generation catalyst technology.

**Scenario:** You want to explore "what if we discover a 30% better catalyst in the next 5 years?"

**Steps:**

1. **Open app** → **Process Model** page ✓

2. **Note the baseline:**
   - **Catalyst Factor is currently 1.0** (baseline = 100%)
   - Cost per ton: **[observe value]**
   - CO₂ per ton: **[observe value]**

3. **"Breakthrough scenario":** Adjust **Catalyst Factor** slider down to **0.7** ✓
   - *(0.7 means 30% less energy required)*

4. **Observe the impact:**
   - Cost per ton: **[drops by ~X%]**
   - CO₂ per ton: **[drops by ~Y%]**
   - Total daily energy: **[drops]**

5. **Go to Scenarios UAE** ✓
   - Change S3 **Catalyst Factor** to 0.7
   - See updated Scenario 3 metrics
   - Read the cost savings & CO₂ reduction

6. **Create a comparison:**
   - **Today (S2, catalyst 1.0):** Cost $X, CO₂ Y kg/ton
   - **Future (S3, catalyst 0.7):** Cost $X', CO₂ Y' kg/ton
   - **Savings: $[diff] per ton, [diff] kg CO₂ per ton**

7. **Export & present:**
   - Go to **AI Optimizer** ✓
   - Set "Minimize: Combined" (cost + CO₂)
   - Run optimization
   - Download best config as JSON
   - View PDF report showing future scenario

**Talking points:**
- "Quantum chemistry could unlock 20–30% energy improvements"
- "Small jumps in catalyst efficiency → large cost and emission gains"
- "R&D investment in catalysts has high ROI"
- "UAE research institutions could lead this breakthrough"

---

## Common Mistakes & Troubleshooting

### Mistake 1: Setting Unrealistic Parameter Combinations

**What happens:**
- You set **Target NH₃ = 20 tons/day** and **Solar Capacity = 10 MW**
- App shows energy shortage warnings or very high costs

**Why it happens:**
- Small solar farm can't power large production
- Leads to poor capacity utilization

**Fix:**
1. Adjust **Target NH₃** down (5–10 tons/day) OR
2. Increase **Solar Capacity** (50–100 MW) to match

**Rule of thumb:**
- 5 tons/day NH₃ needs ~50 MW solar (at 25% capacity factor)
- 10 tons/day needs ~100 MW
- Scale roughly linearly

---

### Mistake 2: Confusing Tons/Day vs. kg/Day

**What happens:**
- Someone reads "5 tons/day" as "5 kg/day"
- Leads to oversizing / undersizing the plant by 1000×

**Fix:**
- **1 ton = 1000 kg**
- "5 tons/day" = "5000 kg/day"
- App always uses **tons** as the unit

---

### Mistake 3: Misunderstanding Emissions Factor

**What happens:**
- User sees "50 kg CO₂/ton" and wonders "is that good?"
- Without context, unclear if it's reference point

**Context:**
- **Imported ammonia:** ~2000 kg CO₂/ton (fossil fuel + transport)
- **Solar-powered (grid mix):** ~50–100 kg CO₂/ton
- **Solar-powered (pure solar):** ~5–10 kg CO₂/ton (lifecycle only)

**Fix:**
- Always compare to import baseline
- Use the **Scenarios UAE** page to see side-by-side comparison

---

### Mistake 4: Expecting Real Quantum Scores

**What happens:**
- User assumes the **Quantum-Ready** page shows real chemistry
- Tries to patent the "discovery"

**Fix:**
- Quantum-Ready is a **placeholder** for future integration
- Rankings are seeded randomly, not physics-based
- Use for storytelling: "If quantum discovers X, then Y..."
- Do not cite as scientific result

---

### Mistake 5: PDF Won't Download

**What happens:**
- Click "Download Report.pdf" but nothing appears
- Browser doesn't trigger download

**Possible causes:**
- Browser pop-up blocker is active
- Network issue

**Fixes:**
1. Allow pop-ups for `localhost:8501` or your Streamlit Cloud domain
2. Try a different browser (Chrome, Firefox, Safari)
3. If running locally, ensure no antivirus is blocking writes to Downloads folder
4. Refresh the page and try again

---

### Mistake 6: Slider Changes Don't Update Chart / PDF

**What happens:**
- You adjust a parameter.
- Chart doesn't change immediately.

**Why:**
- Streamlit caches heavy calculations; sometimes needs refresh

**Fix:**
1. Click **F5** or **Ctrl+Shift+R** to reload the page
2. Or close and reopen the browser tab
3. Local app: Streamlit auto-rerunning, but may lag

---

### Mistake 7: Confusing "Capacity Factor" with "Efficiency"

**What happens:**
- User thinks capacity factor is electrolyser efficiency
- Sets it to 0.9 (90%) thinking that's realistic

**Fix:**
- **Capacity Factor** = fraction of time solar farm runs at full power
  - Depends on: cloud cover, dust, maintenance
  - UAE typical: 0.22–0.26 (22–26%)
  - NOT a control variable; it's site-dependent

- **Electrolyser Efficiency** = kWh/kg (separate slider)
  - Depends on technology
  - Current tech: 40–50 kWh/kg
  - Future tech: 35–40 kWh/kg

---

### Mistake 8: Variable Exports (JSON) Get Lost

**What happens:**
- Export JSON config but forget where it went
- Can't recreate the scenario later

**Fix:**
1. Always save JSON with a **descriptive name:**
   - ✓ `s2f_dt_uae_green_2026_10t_day.json`
   - ❌ `config.json` (too generic)

2. Store in a **project folder:**
   - Put all exports in: `projects/[farm_name]/configs/`

3. Use **version control (Git):**
   - Commit JSON files to Git with commit message explaining scenario

---

## Glossary

### Core Concepts

**Ammonia (NH₃)**
- Colorless gas, pungent smell
- Essential precursor for nitrate fertilisers
- Made from nitrogen (air) + hydrogen (water)

**Nitrogen Fixation**
- Process of converting N₂ (inert gas) → reactive nitrogen compounds
- Natural process: bacteria in soil
- Industrial process: Haber-Bosch (high temperature + pressure)
- Our model: Electrochemical fixation + Haber-Bosch

**Urea (NH₂)₂CO**
- Stable, solid fertiliser made from ammonia
- Easier to transport and store than ammonia gas
- Our model: Optional conversion from ammonia

**Stoichiometry**
- Science of chemical ratios
- Our model: N₂ + 3H₂ → 2NH₃ (nitrogen + hydrogen → ammonia)
- This tells us: 1 kg N₂ needs 3 kg H₂ to make 4 kg NH₃

### Energy & Power

**Electrolysis**
- Process: Electric current splits water (H₂O) → hydrogen (H₂) + oxygen (O₂)
- Energy required: ~45 kWh per kg of H₂ (current tech)
- Our model: Configurable efficiency (35–50 kWh/kg)

**Haber-Bosch Synthesis**
- Process: High temperature + high pressure + catalyst → N₂ + 3H₂ → 2NH₃
- Industrial standard since 1909
- Energy cost: ~5–15 kWh per kg of NH₃
- Our model: 0.5–15 kWh/kg (configurable)

**Capacity Factor**
- Fraction of time a plant runs at full power
- Formula: (Actual Output)/(Max Possible Output)
- Solar farm typical: 20–30% (weather, dust, maintenance)
- Our model: 0.15–0.35 (15–35%)

**kWh (Kilowatt-hour)**
- Unit of electrical energy
- 1 kWh = power of 1 kW running for 1 hour
- Roughly: electricity to run a microwave for 10 minutes

**MW (Megawatt)**
- Unit of power (rate of energy flow)
- 1 MW = capacity to generate 1000 kW
- Solar farm size typically measured in MW

### Cost & Carbon

**Cost per Ton (USD/ton)**
- Total production cost divided by output
- Includes: electricity, water, amortized capital, labor, margin
- Our model: Simplified linear cost (reality has economies of scale)

**CO₂ Intensity (kg CO₂/ton)**
- Carbon footprint per unit of product
- Includes: embedded emissions in electricity, transport, operations
- Lower = better

**Emissions Factor (kg CO₂/kWh)**
- Carbon emitted per kilowatt-hour of electricity
- **Solar:** ~0.01 kg CO₂/kWh (lifecycle only: manufacturing, installation)
- **Grid (UAE mix):** ~0.48 kg CO₂/kWh (gas turbines + solar mix)
- **Grid (global avg):** ~0.40 kg CO₂/kWh

### Technology & Innovation

**Catalyst**
- Substance that speeds up reactions without being consumed
- In ammonia synthesis: metals (Fe, Ru) deposited on supports
- Efficiency improvement: Catalyst Factor < 1.0 means less energy needed

**Digital Twin**
- Virtual simulation of a real system
- Allows: "what-if" scenarios without building real plant
- Our model: Simplified twin of a future ammonia plant

**Quantum Chemistry (Placeholder)**
- Branch of computational chemistry using quantum mechanics
- Can predict new catalyst structures
- Current status: Research phase, expensive, not yet deployed
- Our model: "Quantum-Ready" page mocks what **could** be discovered

---

## For Technical Reviewers

### Stoichiometry & Derived Ratios

**Chemical Equation:**
```
N₂ + 3H₂ → 2NH₃
```

**Molecular Weights:**
- N (Nitrogen): 14 g/mol → N₂ = 28 g/mol
- H (Hydrogen): 1 g/mol → H₂ = 2 g/mol
- NH₃ (Ammonia): 17 g/mol

**Stoichiometric Ratios:**
- 1 kg N₂ requires 3 kg H₂ → produces 4 kg NH₃
- Equivalently:
  - **H₂ per NH₃:** 3/4 = 0.75 kg H₂ per kg NH₃
  - **N₂ per NH₃:** 1/4 = 0.25 kg N₂ per kg NH₃

**In our model:** `constants.py` defines:
```python
STOICH_H2_TO_NH3 = 0.17857  # kg H2 per kg NH3 (accounts for 3H2 + N2 → 2NH3)
STOICH_N2_TO_NH3 = 0.25  # kg N2 per kg NH3
```

### Energy Block Formulas

The total energy required is:

```
E_total = E_electrolysis + E_n2_sep + E_synthesis + E_other
```

#### 1. Electrolysis (Dominant)
```
E_electrolysis [kWh] = mass_h2 [kg] × electrolyser_efficiency [kWh/kg]
where:
  mass_h2 = target_nh3 × STOICH_H2_TO_NH3
  electrolyser_efficiency = user slider (35–50 kWh/kg)
```

#### 2. N₂ Separation from Air
```
E_n2_sep [kWh] = mass_n2 [kg] × n2_separation_energy [kWh/kg]
where:
  mass_n2 = target_nh3 × STOICH_N2_TO_NH3
  n2_separation_energy = user slider (0.5–2.0 kWh/kg)
```

#### 3. Haber-Bosch Synthesis
```
E_synthesis [kWh] = target_nh3 [kg] × synthesis_energy [kWh/kg] × catalyst_factor
where:
  synthesis_energy = user slider (0.5–15 kWh/kg)
  catalyst_factor = user slider (0.5–1.2, multiplier)
  Lower catalyst_factor → lower energy (better catalyst)
```

#### 4. Total Daily Energy
```
E_daily [MWh/day] = (E_electrolysis + E_n2_sep + E_synthesis) / 1000
```

#### 5. Required Solar Capacity
```
solar_capacity_required [MW] = E_daily × 1000 / (24 × capacity_factor)
Example:
  E_daily = 100 MWh
  capacity_factor = 0.25 (25%)
  solar_capacity = 100 × 1000 / (24 × 0.25) = 16.67 MW
```

### Cost Formulas

```
Cost_per_ton_nh3 [USD/ton] = (cost_electricity + cost_water) / target_nh3
```

#### Electricity Cost
```
cost_electricity [USD] = E_daily [MWh] × 1000 × electricity_cost_usd_kwh
Example:
  100 MWh × 1000 kWh/MWh × 0.04 USD/kWh = $4000/day
  For 5 tons/day: $4000 / 5 = $800/ton (attributed to E)
```

#### Water Cost
```
mass_water_required [m³/day] = (mass_h2 + losses) / density
cost_water [USD] = mass_water [m³] × water_cost_usd_m3
```

### CO₂ Intensity Formulas

```
CO2_intensity [kg CO2/ton] = (E_daily × emissions_factor) / target_nh3
where:
  emissions_factor [kg CO2/kWh] = {
    0.01 if using pure solar (lifecycle)
    0.48 if using UAE grid mix (gas turbines + solar)
  }
```

**Interpretation:**
- Solar-powered (grid mix): ~50 kg CO₂/ton
- Imported (fossil fuel): ~2000 kg CO₂/ton
- **97.5% reduction** via solar

### Climate Data Assumptions

**UAE Solar Irradiation:**
- Direct Normal Irradiance (DNI): 5–6 kWh/m²/day
- Capacity Factor: 0.22–0.26 (typical)
- Source: NASA/NREL Solar Atlas

**UAE Electricity Emissions Factor:**
- Grid mix: ~48% gas + solar + other renewables
- Emissions: ~0.48 kg CO₂/kWh
- Expected to improve as solar penetration increases

**Solar Equipment Lifecycle Co2:**
- PV panels: ~0.01 kg CO₂/kWh (manufacturing + installation + decommission)
- Inverters: ~0.002 kg CO₂/kWh
- **Total solar lifecycle:** ~0.012 kg CO₂/kWh

### Assumptions Source

All configurable parameters and defaults are defined in:
```
core/constants.py
```

Key sections:
```python
# Stoichiometry
STOICH_N2_TO_NH3 = 0.25
STOICH_H2_TO_NH3 = 0.17857

# Energy factors (kWh)
ELECTROLYSER_EFFICIENCY_KWH_PER_KG_H2 = 45.0
N2_SEPARATION_ENERGY_KWH_PER_KG_N2 = 0.5
SYNTHESIS_ENERGY_KWH_PER_KG_NH3 = 8.0

# Cost factors (USD)
ELECTRICITY_COST_USD_PER_KWH = 0.04
WATER_COST_USD_PER_M3 = 1.5
CAPEX_AMORTIZED_USD_PER_TON_NH3 = 50.0

# Emissions factors (kg CO2)
SOLAR_EMISSIONS_FACTOR_KG_CO2_PER_KWH = 0.01
GRID_EMISSIONS_FACTOR_KG_CO2_PER_KWH = 0.48

# Defaults
DEFAULT_CAPACITY_FACTOR = 0.25
DEFAULT_CATALYST_FACTOR = 1.0
```

All values are **configurable** via `data/defaults.json` and UI sliders.

### Testing Coverage

The repository includes automated tests in `tests/test_process.py`.

**Test categories:**

1. **Stoichiometry Tests**
   - Verify N₂, H₂ → NH₃ ratios
   - Test mass balance conservation

2. **Energy Calculation Tests**
   - Electrolysis energy vs. efficiency
   - Synthesis energy vs. catalyst factor
   - Total daily energy aggregation

3. **Water Requirement Tests**
   - H₂O per kg H₂ (electrolysis)
   - Daily water demand

4. **Cost Calculation Tests**
   - Electricity cost component
   - Water cost component
   - Total cost per ton

5. **CO₂ Intensity Tests**
   - Solar-powered (low- emission)
   - Grid-powered (high-emission)
   - Comparison to import baseline

**To run tests locally:**
```bash
cd Solar-to-Fertiliser/s2f_dt
pip install pytest
pytest tests/ -v
```

**Expected output:** All tests pass (green ✓).

### Model Limitations & Future Improvements

**Current Limitations:**
1. **Linear cost model** — Real plants have economies of scale (non-linear)
2. **Simplified water balance** — Doesn't account for condensation recovery
3. **No grid integration** — Assumes single-site, no electricity trading
4. **No transport** — Assumes fertiliser used locally (no shipping)
5. **Placeholder quantum scorer** — Not based on real quantum chemistry
6. **Single technology pathway** — Assumes Haber-Bosch; other syntheses not explored
7. **No site-specific geology** — Capacity factor same everywhere (actually varies)

**Path to Production Readiness:**
- [ ] Integrate real CapEx data (engineering quotes)
- [ ] Add Monte Carlo uncertainty analysis
- [ ] Couple to grid forecasting (wind + solar)
- [ ] Include supply chain & logistics costs
- [ ] Validate catalyst evolution curves against literature
- [ ] Link to real quantum chemistry frameworks (TensorFlow, JAX)
- [ ] Add environmental impact categories (water stress, land use, biodiversity)

---

## Final Notes

### Support & Documentation

For questions:
- **App Issues:** Check the Troubleshooting section above
- **Technical Deep Dive:** Review the "For Technical Reviewers" section
- **Source Code:** Available on GitHub (contact Experts Group FZE for access)

### Citation

If you use S2F-DT in research, reports, or presentations, please cite as:

> Experts Group FZE (2026). Solar-to-Fertiliser Digital Twin (S2F-DT), version 1.0. Abu Dhabi, UAE. Educational and research use. Disclaimer: simplified model; not for final engineering design.

### Feedback

We welcome feedback to improve S2F-DT:
- Usability issues
- Parameter suggestions
- New use cases
- Scientific accuracy concerns

Contact: Experts Group FZE, Abu Dhabi, UAE

---

**Document Version:** 1.0  
**Last Updated:** March 2026  
**Status:** Approved for Distribution

*Experts Group FZE — Abu Dhabi, UAE — All Rights Reserved*
