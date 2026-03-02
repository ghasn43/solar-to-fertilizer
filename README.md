# Solar-to-Fertiliser Digital Twin (S2F-DT)

## Overview

**S2F-DT** is a comprehensive Streamlit application that simulates the production of **ammonia (NH₃)** and optionally **urea** from solar electricity, ambient air, and water. It's designed for **Experts Group FZE** to support UAE's green agenda and fertiliser industry innovation.

### Process Flow
```
☀️ Solar (MW) → Electrolysis (H₂) + N₂ Separation (Air) 
    → Haber-Bosch Synthesis (N₂ + 3H₂ → 2NH₃) 
    → Optional Urea (2NH₃ + CO₂ → CO(NH₂)₂)
```

### Key Features
✅ **Process Simulation**: Stoichiometric mass balance, energy balance, cost/CO₂ analysis  
✅ **Multi-Scenario Comparison**: Baseline import vs. green ammonia vs. future catalyst  
✅ **AI Optimizer**: Grid-search to minimize cost or CO₂  
✅ **Quantum-Ready**: Mock catalyst scoring (extensible to IBM Quantum)  
✅ **PDF Export**: 1-page branded report  
✅ **JSON Config**: Version-controllable configurations  
✅ **Clean UI**: Multi-page Streamlit app with company branding  

---

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Project Structure](#project-structure)
4. [Page Descriptions](#page-descriptions)
5. [Technical Details](#technical-details)
6. [Testing](#testing)
7. [Configuration](#configuration)
8. [Troubleshooting](#troubleshooting)

---

## Installation

### Prerequisites
- **Python 3.11+** (Windows, macOS, Linux)
- **pip** (Python package manager)
- **Git** (optional, for version control)

### Windows Setup

#### Quick Setup (Automated)
1. **Double-click `setup.bat`** in the project root
2. Wait for installation to complete
3. Run: `streamlit run app.py`

#### Manual Setup
1. **Clone or download the repository:**
   ```powershell
   cd d:\Solar-to-Fertiliser\s2f_dt
   ```

2. **Create a virtual environment:**
   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```

3. **Upgrade pip:**
   ```powershell
   python -m pip install --upgrade pip
   ```

4. **Install dependencies:**
   ```powershell
   pip install --no-cache-dir -r requirements.txt
   ```

5. **Run the application:**
   ```powershell
   streamlit run app.py
   ```

   Your default browser will open to `http://localhost:8501`

**Having issues?** See [SETUP.md](SETUP.md) for troubleshooting.

### macOS Setup

#### Quick Setup (Automated)
1. **Run the setup script** in Terminal:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
2. Wait for installation to complete
3. Run: `streamlit run app.py`

#### Manual Setup
1. **Clone or download the repository:**
   ```bash
   cd ~/Solar-to-Fertiliser/s2f_dt
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Upgrade pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

4. **Install dependencies:**
   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

**Having issues?** See [SETUP.md](SETUP.md) for troubleshooting.

### Linux Setup (Ubuntu/Debian)

1. **Install Python 3.11:**
   ```bash
   sudo apt-get update
   sudo apt-get install python3.11 python3.11-venv python3-pip
   ```

2. **Create a virtual environment:**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run:**
   ```bash
   streamlit run app.py
   ```

---

## Quick Start

### 1. Start the Application
```bash
streamlit run app.py
```

### 2. Navigate Pages (Left Sidebar)
The app includes 6 pages:
1. **📊 Overview** — Project intro & KPI summary
2. **🔧 Process Model** — Configure parameters, see detailed results
3. **🌍 Scenarios UAE** — Compare 3 strategic scenarios
4. **🤖 AI Optimizer** — Find optimal configuration
5. **⚛️ Quantum-Ready** — Mock catalyst scoring (future: IBM Quantum)
6. **📄 Report Export** — Generate PDF & JSON exports

### 3. Configure & Simulate
- Adjust sliders (solar MW, electrolyser efficiency, etc.)
- Click "Run" to see instant results
- Review energy breakdown, costs, CO₂ intensity

### 4. Export Results
- Generate **PDF report** (1-page, branded, IP-protected)
- Export **JSON config** (reproducible, portable)

---

## Project Structure

```
s2f_dt/
├── app.py                          # Main Streamlit app
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── pages/
│   ├── 1_Overview.py              # Overview & KPIs
│   ├── 2_Process_Model.py         # Detailed process simulation
│   ├── 3_Scenarios_UAE.py         # Strategic scenarios
│   ├── 4_AI_Optimizer.py          # Grid-search optimizer
│   ├── 5_Quantum_Ready.py         # Mock quantum catalyst scoring
│   └── 6_Report_Export.py         # PDF & JSON export
│
├── core/
│   ├── __init__.py                # Package exports
│   ├── constants.py               # All assumptions (units, values, etc.)
│   ├── models.py                  # Pydantic models (config, results)
│   ├── process.py                 # Core stoichiometry & energy calculations
│   ├── scenarios.py               # Scenario definitions & comparisons
│   ├── optimizer.py               # Grid-search optimizer
│   ├── quantum_stub.py            # Mock quantum catalyst scorer
│   ├── reporting.py               # PDF & JSON generation
│   └── utils.py                   # Helper functions
│
├── data/
│   └── defaults.json              # Default configuration
│
├── tests/
│   └── test_process.py            # Unit tests for process model
│
└── assets/
    └── logo_placeholder.txt       # Branding placeholder
```

## Troubleshooting

### Installation Issues

If you encounter `pip install` errors, try these solutions in order:

1. **Upgrade pip first:**
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Use `--no-cache-dir` flag:**
   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```

3. **Install minimal version** (core features only):
   ```bash
   pip install -r requirements_minimal.txt
   ```

4. **Install packages individually** (if bulk fails):
   ```bash
   pip install streamlit pandas numpy matplotlib
   ```

5. **Check for virtual environment:**
   - Windows: `where python` should show `venv\Scripts\python.exe`
   - macOS/Linux: `which python` should show path containing `venv`

### Common Errors

| Error | Solution |
|-------|----------|
| `No module named 'venv'` | Use `python3 -m venv venv` with explicit python3 |
| `pip is not recognized` | Use `python -m pip install ...` instead |
| `reportlab build error` | `pip install --only-binary :all: reportlab` |
| `Microsoft C++ required` | Install Visual C++ Build Tools or relax version pins |
| `SSL certificate error` | Update cert: `pip install --upgrade certifi` |

### Getting Help

1. **See [SETUP.md](SETUP.md)** for detailed installation guide
2. **Check Python version:** `python --version` (should be 3.11+)
3. **Verify pip:** `pip --version`
4. **List installed packages:** `pip list`

### 1️⃣ Overview (`1_Overview.py`)
**Purpose**: Executive summary and assumptions.

**Contents**:
- Short narrative on solar-to-fertiliser production
- KPI cards: NH₃/day, Urea/day, kWh/day, water/day, CO₂ intensity, cost/ton
- Expandable "Assumptions" section with stoichiometry, energy, costs
- Process diagram

### 2️⃣ Process Model (`2_Process_Model.py`)
**Purpose**: Detailed process simulation and energy balance.

**Inputs** (Sliders):
- Target NH₃ (tons/day)
- Solar capacity (MW)
- Electrolyser efficiency (kWh/kg H₂)
- Catalyst factor (multiplier)
- Capacity factor (%)
- Water cost (USD/m³)
- Electricity cost (USD/kWh)
- Include Urea? (toggle)

**Outputs**:
- Daily NH₃, water, electricity, cost, CO₂
- Energy breakdown pie chart
- Detailed calculation table
- Stoichiometric mass balance

### 3️⃣ Scenarios UAE (`3_Scenarios_UAE.py`)
**Purpose**: Compare 3 strategic scenarios for UAE greening.

**Scenarios**:
1. **S1**: Imported fertiliser baseline
2. **S2**: UAE green ammonia (current config)
3. **S3**: Future breakthrough catalyst (improved efficiency)

**Analysis**:
- Comparison table & charts (cost, CO₂)
- Strategic analysis (cost-competitiveness, carbon reduction)
- "How this supports UAE greening" bullet points
- Takeaways (environmental, economic, strategic)

### 4️⃣ AI Optimizer (`4_AI_Optimizer.py`)
**Purpose**: Find optimal configuration minimizing cost or CO₂.

**Algorithm**: Grid search over:
- Electrolyser efficiency (35–50 kWh/kg H₂)
- Catalyst factor (0.5–1.2)
- Solar capacity (10–100 MW)
- Capacity factor (0.15–0.35)

**Objectives**:
- Minimize cost
- Minimize CO₂
- Minimize combined (Cost + λ × CO₂)

**Outputs**:
- Best solution (KPIs)
- Top 10 solutions (table)
- Option to apply best to config
- JSON download

### 5️⃣ Quantum-Ready (`5_Quantum_Ready.py`)
**Purpose**: Demonstrate quantum-ready architecture for catalyst optimization.

**Features**:
- **Surrogate Model**: Mock quantum scorer (seeded RNG, fast)
- **Catalyst Ranking**: Score 5 candidates
- **Top 3 Analysis**: Detailed comparison
- **Integration Path**: Phase 1→4 roadmap (to IBM Quantum)
- **Custom Catalyst**: Score your own candidate

### 6️⃣ Report Export (`6_Report_Export.py`)
**Purpose**: Generate exportable PDF and JSON files.

**PDF Report** (1-page):
- Title, date, company branding
- Selected scenario details
- Key inputs & KPIs
- Scenario comparison table
- IP notice (confidential footer)

**JSON Config**:
- Metadata (timestamp, company, app version)
- All input parameters
- Calculation results
- Importable for batch processing

---

## Technical Details

### Stoichiometry
**Reaction**: N₂ + 3H₂ → 2NH₃

For **1 ton NH₃**:
- N₂ required: 0.824 tons (28 kg of 34 kg total)
- H₂ required: 0.176 tons (6 kg of 34 kg total)

### Energy Blocks
1. **Electrolysis**: 2H₂O → 2H₂ + O₂ @ 45 kWh/kg H₂ (PEM/alkaline baseline)
2. **N₂ Separation**: Cryogenic or PSA @ 0.5 kWh/kg N₂
3. **Haber-Bosch**: N₂ + 3H₂ → 2NH₃ @ 8 kWh/kg NH₃ (catalyst-dependent)

**Catalyst Factor**: Multiplier on synthesis energy (0.5–1.2):
- 0.5 = breakthrough (50% energy reduction)
- 1.0 = baseline
- 1.2 = pessimistic scenario

### Cost Model
**OpEx** (operational):
- Electricity cost: electricity_kwh_day × electricity_cost_usd_kwh
- Water cost: water_m3_day × water_cost_usd_m3

**CapEx** (amortized):
- Hardcoded: $50/ton NH₃ (depreciation over system lifetime)

**Formula**: Cost/ton = (OpEx + CapEx) / daily_nh3_tons

### CO₂ Intensity
**Solar scenario** (default):
- 0.01 kg CO₂/kWh (lifecycle only; manufacturing, logistics)

**Grid scenario** (alternative):
- 0.48 kg CO₂/kWh (UAE mix: natural gas + solar)

### Capacity Factor
**UAE Solar**: ~25% annual average
- Accounts for seasonal variation, day/night cycles, weather
- Example: 100 MW @ 25% capacity = 600 MWh/day (on average)

### Water Usage
**Electrolysis**: 2H₂O → 2H₂ + O₂
- Baseline assumption: **9 kg water per kg H₂** (includes efficiency loss)
- Source: Alkaline electrolyser manufacturers' specs

---

## Testing

### Run Unit Tests
```bash
# Windows
python -m pytest tests/test_process.py -v

# macOS / Linux
python3 -m pytest tests/test_process.py -v
```

### Test Coverage
- **test_process.py**:
  - `TestMassBalance`: Stoichiometric calculations
  - `TestEnergyBalance`: Energy blocks & catalyst factor
  - `TestWaterRequirement`: Water usage
  - `TestCO2Intensity`: Solar vs. grid emissions
  - `TestCost`: Cost per ton
  - `TestProcessModel`: Full integration test

### Example Test Output
```
tests/test_process.py::TestMassBalance::test_mass_balance_1_ton_nh3 PASSED      [ 10%]
tests/test_process.py::TestMassBalance::test_mass_balance_5_tons_nh3 PASSED      [ 20%]
tests/test_process.py::TestEnergyBalance::test_energy_balance_baseline PASSED    [ 30%]
...
============================== 6 passed in 0.23s ==============================
```

---

## Configuration

### Default Values (`data/defaults.json`)
```json
{
  "target_nh3_day": 5.0,
  "solar_capacity_mw": 50.0,
  "electrolyser_efficiency": 45.0,
  "n2_separation_energy": 0.5,
  "synthesis_energy": 8.0,
  "catalyst_factor": 1.0,
  "capacity_factor": 0.25,
  "water_cost_usd_m3": 1.5,
  "electricity_cost_usd_kwh": 0.04,
  "include_urea": false
}
```

### Modifying Assumptions (`core/constants.py`)
All numeric assumptions are centralized with comments:
```python
DEFAULT_ELECTROLYSER_EFFICIENCY = 45.0  # kWh/kg H2
DEFAULT_SYNTHESIS_ENERGY = 8.0          # kWh/kg NH3
UAE_GRID_CO2_FACTOR = 0.48              # kg CO2 / kWh
DEFAULT_ELECTRICITY_COST = 0.04         # USD/kWh
BASELINE_IMPORTED_COST = 400            # USD/ton NH3
```

Edit these values to reflect your specific scenario.

---

## Troubleshooting

### Issue: `python: command not found`
**Solution**: 
- Windows: Use `python` or `py` in PowerShell
- macOS/Linux: Use `python3` instead of `python`

### Issue: `ModuleNotFoundError: No module named 'streamlit'`
**Solution**: 
```bash
pip install -r requirements.txt
```

### Issue: `reportlab` not found (PDF export fails)
**Solution**:
```bash
pip install reportlab==4.0.4
```

### Issue: Port 8501 already in use
**Solution**:
```bash
streamlit run app.py --server.port 8502
```

### Issue: Slow optimization (grid search)
**Solution**: 
- Reduce `grid_density` from 5 to 4 (faster)
- Or wait; 5–7 grid points take ~2–5 minutes

### Issue: JSON export fails or empty
**Solution**:
- Go to **Scenarios UAE** page first to generate scenarios
- Then return to **Report Export**

---

## Usage Examples

### Scenario 1: Quick Feasibility Check
1. Open app: `streamlit run app.py`
2. Go to **Process Model**
3. Adjust `solar_capacity_mw` slider (e.g., 50 MW you have available)
4. Note the cost/ton and CO₂ intensity
5. Compare to **Scenarios UAE** baseline import cost

### Scenario 2: Optimize for Cost
1. Go to **AI Optimizer**
2. Set objective to `💰 Cost (USD/ton)`
3. Run optimization with `grid_density=5`
4. Review top 10 solutions
5. Click **Apply to Config** for best solution
6. Go to **Process Model** to inspect details

### Scenario 3: Generate Report for Stakeholders
1. Configure preferred scenario in **Process Model**
2. Go to **Scenarios UAE** to finalize scenario choice
3. Go to **Report Export**
4. Click **Generate PDF Report**
5. Download and share with non-technical stakeholders

---

## API / Integration

### Using S2F-DT in Your Own Python Code
```python
from core.models import ProcessConfig
from core.process import process_model

config = ProcessConfig(
    target_nh3_day=10.0,
    solar_capacity_mw=100.0,
    electrolyser_efficiency=45.0,
    n2_separation_energy=0.5,
    synthesis_energy=8.0,
    catalyst_factor=0.8,  # Improved catalyst
    capacity_factor=0.25,
    water_cost_usd_m3=1.5,
    electricity_cost_usd_kwh=0.04,
    include_urea=False,
)

results = process_model(config)
print(f"Cost: ${results.cost_usd_per_ton_nh3:.0f}/ton")
print(f"CO₂: {results.co2_intensity_kg_per_kg_nh3 * 1000:.1f} kg CO₂/ton")
```

---

## Performance

| Task | Time |
|------|------|
| Single simulation | ~100 ms |
| Optimization (grid_density=4) | ~30 sec |
| Optimization (grid_density=5) | ~2 min |
| PDF generation | ~5 sec |
| JSON export | <1 sec |

---

## Future Enhancements

- [ ] Real IBM Quantum integration (phase 2)
- [ ] Advanced optimizer (SciPy, Optuna)
- [ ] Sensitivity analysis (Tornado charts)
- [ ] Multi-objective optimization (Pareto frontier)
- [ ] Batch processing API
- [ ] Database persistence (scenarios, configs)
- [ ] Advanced catalyst characterization (DFT import)
- [ ] Supply chain cost analysis
- [ ] Investment ROI calculator

---

## License & IP

**Experts Group FZE — Abu Dhabi, UAE**

All Rights Reserved. Confidential. © Experts Group FZE

This document and its contents are proprietary and confidential. 
Unauthorized distribution or reproduction is prohibited.

---

## Support & Contact

For questions, bug reports, or feature requests:
- **Company**: Experts Group FZE
- **Location**: Abu Dhabi, UAE
- **Application**: Solar-to-Fertiliser Digital Twin (S2F-DT)

---

## Changelog

### v1.0.0 (2026-03-02)
- ✅ Complete Streamlit app (6 pages)
- ✅ Process model (stoichiometry, energy, cost, CO₂)
- ✅ 3 strategic scenarios
- ✅ Grid-search optimizer
- ✅ Quantum-ready module (surrogate)
- ✅ PDF + JSON export
- ✅ Unit tests
- ✅ Documentation

---

**Built with ❤️ for UAE Green Innovation**
