# Quick Start Guide
## Solar-to-Fertiliser Digital Twin (S2F-DT)

**Experts Group FZE** — Abu Dhabi, UAE  
*All Rights Reserved. Confidential. © Experts Group FZE*

---

## 1️⃣ Install

### Option A: Automated (Windows)
```bash
cd Solar-to-Fertiliser\s2f_dt
.\setup.bat
```

### Option B: Automated (Mac/Linux)
```bash
cd Solar-to-Fertiliser/s2f_dt
bash setup.sh
```

### Option C: Manual
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

---

## 2️⃣ Run

```bash
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## 3️⃣ First 5 Steps

1. **Overview Page**
   - See executive summary of KPIs (Cost, CO₂, Energy, Water)
   - Click "📋 Process Assumptions" to see all inputs

2. **Process Model Page**
   - Adjust sliders in sidebar (NH₃ tons/day, Solar MW, Efficiency, etc.)
   - Watch outputs update in real time
   - Key lever: Lower "Electrolyser Efficiency" to see cost drop

3. **Scenarios UAE Page**
   - Compare S1 (import), S2 (solar today), S3 (future catalyst)
   - Check cost and CO₂ charts
   - Read Strategic Analysis for context

4. **AI Optimizer Page**
   - Set objective (Minimize: Cost / CO₂ / Combined)
   - Click "▶️ Run Optimization"
   - View Top 10 solutions; apply best to configuration

5. **Report Export Page**
   - Generate PDF report (1-page summary)
   - Download JSON config (for archiving)

---

## 4️⃣ Export & Share

### PDF Report
- Use in: presentations, proposals, stakeholder briefings
- **Location:** Report Export page → "📥 Download Report.pdf"

### JSON Configuration
- Use for: archiving, sharing exact parameters, version control
- **Location:** Report Export page → "📥 Download Configuration.json"
- **Store:** `projects/[farm_name]/configs/s2f_dt_config_[date].json`

---

## 5️⃣ Defaults & Settings

### Where Defaults Live
```
data/defaults.json
```

Edit to change starting values:
```json
{
  "target_nh3_day": 5.0,
  "solar_capacity_mw": 50.0,
  "electrolyser_efficiency": 45.0,
  "electricity_cost_usd_kwh": 0.04
}
```

Changes take effect next app restart.

---

## Quick Reference: What Each Slider Does

| Slider | Range | Effect |
|--------|-------|--------|
| **NH₃ Production** | 1–20 tons/day | Daily output target |
| **Solar Capacity** | 10–100 MW | Farm size (kWh available) |
| **Electrolyser Eff.** | 35–50 kWh/kg H₂ | Technology maturity (↓ = better) |
| **N₂ Separation** | 0.5–2.0 kWh/kg | Energy to capture nitrogen from air |
| **Synthesis Energy** | 0.5–15 kWh/kg | Haber-Bosch reactor energy |
| **Catalyst Factor** | 0.5–1.2 | Efficiency multiplier (↓ = breakthrough) |
| **Capacity Factor** | 15–35% | % time solar runs at full power |
| **Electricity Cost** | 0.03–0.08 $/kWh | Cost per kilowatt-hour |
| **Water Cost** | 1–3 $/m³ | Desalination cost |

---

## Common Keystrokes

| Action | Key |
|--------|-----|
| Open app | `streamlit run app.py` |
| Reload page (fix lag) | `F5` or `Ctrl+R` |
| Change page | Click sidebar menu |
| Run optimizer | Click "▶️ Run Optimization" button |
| Download report | Report Export → "📥 Download Report.pdf" |
| Download JSON | Report Export → "📥 Download Configuration.json" |

---

## 🚀 4 Example Scenarios

### A. "Show cost-competitiveness"
1. Overview page
2. Note cost (e.g., $350/ton)
3. Compare to import baseline (~$400/ton)
4. Scenarios UAE → cost chart
5. Export PDF for board deck

### B. "Estimate farm ammonia needs"
1. Process Model page
2. Adjust "Target NH₃" to your farm size (tons/day)
3. Note: Solar MW, Daily Energy, Water needed
4. Share config JSON with solar engineer

### C. "Show CO₂ reduction story"
1. Overview page → note CO₂ value (~50 kg/ton)
2. Scenarios UAE → CO₂ chart
3. Calculate: (tons/year) × 50 kg = annual CO₂ vs. import (2000 kg)
4. Use in ESG report

### D. "Explore breakthrough catalyst"
1. Process Model page
2. Lower "Catalyst Factor" slider to 0.7 (30% better)
3. Watch cost and energy drop
4. Scenarios UAE → S3 catalyst factor changes to match
5. Export PDF as "future scenario"

---

## ⚠️ Important Disclaimers

1. **Simulation, not design:**
   - Educational prototype, not final engineering specification
   - Real plant will differ based on site, technology, operations

2. **Energy estimates:**
   - Simplified linear model
   - Actual cost has economies of scale
   - Use for scenario planning, not final capex

3. **Quantum scores placeholder:**
   - Quantum-Ready page is **not real quantum chemistry**
   - Rankings are seeded randomly
   - Use for "what-if" storytelling only

4. **Emissions factors:**
   - Solar: 0.01 kg CO₂/kWh (lifecycle)
   - Grid (UAE): 0.48 kg CO₂/kWh (actual grid mix)
   - Ballpark estimates; verify with local data

---

## 📚 Learn More

**For detailed explanation:** See `docs/TUTORIAL.md`  
**For formulas & science:** See `docs/TUTORIAL.md` → "For Technical Reviewers"  
**For GitHub source:** github.com/ghasn43/solar-to-fertilizer  

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| App won't start | Check: Python 3.11+, `pip install streamlit` |
| Slider changes don't update | Press `F5` to reload page |
| PDF won't download | Allow pop-ups, try different browser |
| Unrealistic slider values | Rule of thumb: ~10 MW solar per 5 tons/day NH₃ |

---

**Version:** 1.0 | **Last Updated:** March 2026

*Experts Group FZE — Abu Dhabi, UAE — All Rights Reserved*
