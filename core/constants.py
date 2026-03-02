"""
Constants and default assumptions for S2F-DT model.
All values documented with units and sources.
"""

# ============================================================================
# STOICHIOMETRY & MASS BALANCE
# ============================================================================
# Synthesis reaction: N2 + 3H2 → 2NH3
# Molecular weights: N2=28, H2=2, NH3=17
STOICH_N2_TO_NH3 = 28 / 34  # kg N2 per kg NH3
STOICH_H2_TO_NH3 = 6 / 34   # kg H2 per kg NH3
STOICH_NH3_TO_UREA = 60 / 68  # kg NH3 per kg Urea (2NH3 + CO2 → (NH2)2CO)

# ============================================================================
# ELECTROLYSIS (H2 PRODUCTION)
# ============================================================================
# Electrolyser efficiency in kWh/kg H2 (fuel cell / alkaline / PEM typical)
DEFAULT_ELECTROLYSER_EFFICIENCY = 45.0  # kWh/kg H2 (conservative baseline)
# Water requirement: ~9 kg water per kg H2 (at electrochemistry optimal)
WATER_USAGE_PER_KG_H2 = 9.0  # kg water / kg H2

# ============================================================================
# N2 SEPARATION (Air Separation Unit - ASU)
# ============================================================================
# Energy to extract N2 from ambient air (often as byproduct or dedicated cryogenic)
DEFAULT_N2_SEPARATION_ENERGY = 0.5  # kWh/kg N2 (crude estimate; often free as byproduct)

# ============================================================================
# HABER-BOSCH / SYNTHESIS
# ============================================================================
# Energy for ammonia synthesis (N2 + 3H2 → 2NH3) at reactor pressure/temperature
DEFAULT_SYNTHESIS_ENERGY = 8.0  # kWh/kg NH3 (catalytic synthesis baseline)
# Catalyst improvement factor: 0.5 = 50% reduction, 1.2 = 20% increase
DEFAULT_CATALYST_FACTOR = 1.0

# ============================================================================
# SOLAR & CAPACITY
# ============================================================================
# Solar capacity factor for UAE (duty cycle of solar generation)
DEFAULT_CAPACITY_FACTOR = 0.25  # 25% (annual average for UAE)
# Solar irradiance in UAE: ~5.5-6.0 kWh/m²/day
# Typical PV efficiency: 18-22%, so ~1 MW => ~240-350 MWh/year
# Translates to ~240/365*0.25 ≈ 0.164 MW capacity factor, conservative 0.25

# ============================================================================
# EMISSIONS FACTORS
# ============================================================================
# CO2 intensity of grid electricity in UAE (2024 estimates)
UAE_GRID_CO2_FACTOR = 0.48  # kg CO2 / kWh (gas + solar mix)
SOLAR_CO2_FACTOR = 0.01     # kg CO2 / kWh (minimal, lifecycle only)

# ============================================================================
# COSTS
# ============================================================================
# Default electricity cost (AED or USD/kWh equivalent)
DEFAULT_ELECTRICITY_COST = 0.04  # USD/kWh (approximately 0.15 AED/kWh)
DEFAULT_WATER_COST = 1.5         # USD/m³ (1000 kg; UAE desalination ~1.5 AED/m³)
# Capital cost amortized into product (simplified model)
DEFAULT_CAPEX_AMORTIZATION = 50  # USD/ton NH3 (years of depreciation embedded)

# ============================================================================
# UREA PRODUCTION
# ============================================================================
# CO2 source for urea: captured from atmosphere or industrial (assume 1 kg CO2 available)
DEFAULT_CO2_FOR_UREA_COST = 10   # USD/ton CO2 (future cost)

# ============================================================================
# SCENARIO DEFAULTS
# ============================================================================
# Baseline: imported fertiliser
BASELINE_IMPORTED_COST = 400     # USD/ton NH3 equivalent
BASELINE_IMPORTED_CO2 = 2.0      # kg CO2 / kg NH3 (accounting for transport)

# ============================================================================
# OPTIMIZER
# ============================================================================
# Search space bounds for optimization
OPTIMIZER_SEARCH_SPACE = {
    "electrolyser_efficiency": [35.0, 50.0],      # kWh/kg H2
    "catalyst_factor": [0.7, 1.2],                # multiplier on synthesis energy
    "solar_capacity_mw": [10.0, 100.0],           # MW
    "capacity_factor": [0.15, 0.35],              # fraction
}

# ============================================================================
# QUANTUM STUB (MOCK)
# ============================================================================
# Pseudo-random seed for reproducibility of mock quantum scores
QUANTUM_SEED = 42
# Catalyst candidates for demonstration
CATALYST_CANDIDATES = [
    {"name": "Ruthenium-Carbon", "notes": "State-of-art catalyst"},
    {"name": "Iron-based", "notes": "Low-cost alternative"},
    {"name": "Perovskite Novel", "notes": "Emerging structure"},
    {"name": "Metal-Organic Framework", "notes": "High surface area"},
    {"name": "Single-Atom Ruthenium", "notes": "Theoretical optimum"},
]

# ============================================================================
# REPORTING & EXPORT
# ============================================================================
# PDF report title and footer
COMPANY_NAME = "Experts Group FZE"
COMPANY_LOCATION = "Abu Dhabi, UAE"
IP_NOTICE = (
    "All Rights Reserved. Confidential. © Experts Group FZE. "
    "This document and its contents are proprietary and confidential. "
    "Unauthorized distribution is prohibited."
)
