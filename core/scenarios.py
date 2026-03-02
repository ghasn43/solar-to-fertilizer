"""
Scenario definitions and comparison utilities.
"""
from typing import List
import pandas as pd
from core.models import ProcessConfig, ScenarioComparison
from core.process import process_model
from core.constants import (
    BASELINE_IMPORTED_COST,
    BASELINE_IMPORTED_CO2,
)


def create_scenario_1_baseline(target_nh3_tons_day: float) -> ScenarioComparison:
    """
    Scenario 1: Imported fertiliser baseline.
    User can override cost and CO2.
    """
    return ScenarioComparison(
        name="S1: Imported Fertiliser (Baseline)",
        cost_usd_per_ton=BASELINE_IMPORTED_COST,
        co2_kg_per_ton=BASELINE_IMPORTED_CO2 * 1000,  # Convert to kg
        nh3_tons_day=target_nh3_tons_day,
        description="Conventional imported ammonia/fertiliser with transport emissions."
    )


def create_scenario_2_uae_green(config: ProcessConfig) -> ScenarioComparison:
    """
    Scenario 2: UAE green ammonia (solar + electrolysis).
    """
    results = process_model(config)
    return ScenarioComparison(
        name="S2: UAE Green Ammonia (Solar)",
        cost_usd_per_ton=results.cost_usd_per_ton_nh3,
        co2_kg_per_ton=results.co2_intensity_kg_per_kg_nh3 * 1000,  # Convert to kg
        nh3_tons_day=results.nh3_tons_day,
        description="Solar-powered green ammonia production in UAE."
    )


def create_scenario_3_future_catalyst(
    base_config: ProcessConfig,
    catalyst_factor_improvement: float = 0.8
) -> ScenarioComparison:
    """
    Scenario 3: Future breakthrough catalyst (lower synthesis energy).
    """
    improved_config = ProcessConfig(
        target_nh3_day=base_config.target_nh3_day,
        solar_capacity_mw=base_config.solar_capacity_mw,
        electrolyser_efficiency=base_config.electrolyser_efficiency,
        n2_separation_energy=base_config.n2_separation_energy,
        synthesis_energy=base_config.synthesis_energy,
        catalyst_factor=catalyst_factor_improvement,
        capacity_factor=base_config.capacity_factor,
        water_cost_usd_m3=base_config.water_cost_usd_m3,
        electricity_cost_usd_kwh=base_config.electricity_cost_usd_kwh,
        include_urea=base_config.include_urea,
    )
    results = process_model(improved_config)
    return ScenarioComparison(
        name="S3: Future Breakthrough Catalyst (UAE)",
        cost_usd_per_ton=results.cost_usd_per_ton_nh3,
        co2_kg_per_ton=results.co2_intensity_kg_per_kg_nh3 * 1000,
        nh3_tons_day=results.nh3_tons_day,
        description="Solar ammonia with improved catalyst (lower synthesis energy)."
    )


def compare_scenarios(
    scenarios: List[ScenarioComparison],
) -> pd.DataFrame:
    """
    Create comparison DataFrame.
    """
    data = [
        {
            "Scenario": s.name,
            "NH3 (tons/day)": f"{s.nh3_tons_day:.2f}",
            "Cost (USD/ton)": f"{s.cost_usd_per_ton:.0f}",
            "CO2 Intensity (kg CO2/ton)": f"{s.co2_kg_per_ton:.1f}",
        }
        for s in scenarios
    ]
    return pd.DataFrame(data)


def uae_greening_text() -> str:
    """Return bullet points on how S2F supports UAE greening."""
    return """
### How Solar-to-Fertiliser Supports UAE Greening & Food Security

- **Sustainable Fertiliser**: Reduce agricultural input costs and import dependency via local, green ammonia.
- **Circular Economy**: Use desert solar + air + water → eliminates mining/transport of phosphate/potash alternatives.
- **Carbon Neutrality**: Align with UAE Net Zero 2050 and UAE Green Agenda 2030.
- **Water Reuse**: Integrate with desalination wastewater; close the loop in arid regions.
- **Employment**: Create skilled jobs in green hydrogen, process engineering, and digital twins.
- **Export Opportunity**: Produce export-quality green ammonia/urea for GCC and global markets.
- **Food Security**: Support local agriculture with affordable, clean-energy fertiliser.
- **Tech Leadership**: Position UAE as innovation hub for green chemistry and quantum-optimized catalysts.
    """
