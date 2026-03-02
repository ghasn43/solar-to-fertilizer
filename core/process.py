"""
Core process model: stoichiometry, energy balance, and KPI calculations.
"""
from typing import Dict, Tuple
from core.constants import (
    STOICH_N2_TO_NH3,
    STOICH_H2_TO_NH3,
    STOICH_NH3_TO_UREA,
    WATER_USAGE_PER_KG_H2,
    DEFAULT_CATALYST_FACTOR,
    SOLAR_CO2_FACTOR,
)
from core.models import ProcessConfig, ProcessResults


def calculate_mass_balance(target_nh3_tons_day: float) -> Dict[str, float]:
    """
    Calculate mass balance for ammonia synthesis.
    Reaction: N2 + 3H2 → 2NH3
    
    Args:
        target_nh3_tons_day: Target production in tons/day
    
    Returns:
        Dictionary with H2_tons_day, N2_tons_day
    """
    nh3_kg_day = target_nh3_tons_day * 1000
    h2_required_kg = nh3_kg_day * STOICH_H2_TO_NH3
    n2_required_kg = nh3_kg_day * STOICH_N2_TO_NH3
    
    return {
        "h2_kg_day": h2_required_kg,
        "n2_kg_day": n2_required_kg,
        "nh3_kg_day": nh3_kg_day,
    }


def calculate_energy_balance(
    h2_kg_day: float,
    n2_kg_day: float,
    nh3_kg_day: float,
    electrolyser_eff: float,
    n2_sep_energy: float,
    synthesis_energy: float,
    catalyst_factor: float = DEFAULT_CATALYST_FACTOR,
) -> Tuple[float, Dict[str, float]]:
    """
    Calculate total daily energy requirement and energy breakdown.
    
    Args:
        h2_kg_day: H2 requirement (kg/day)
        n2_kg_day: N2 requirement (kg/day)
        nh3_kg_day: NH3 production (kg/day)
        electrolyser_eff: Efficiency (kWh/kg H2)
        n2_sep_energy: Energy for N2 (kWh/kg N2)
        synthesis_energy: Energy for synthesis (kWh/kg NH3)
        catalyst_factor: Catalyst multiplier (0.5-1.2)
    
    Returns:
        (total_kwh_day, energy_breakdown_dict)
    """
    electrolysis_energy = h2_kg_day * electrolyser_eff
    n2_separation = n2_kg_day * n2_sep_energy
    synthesis = nh3_kg_day * synthesis_energy * catalyst_factor
    
    total_kwh = electrolysis_energy + n2_separation + synthesis
    
    breakdown = {
        "Electrolysis": electrolysis_energy,
        "N2 Separation": n2_separation,
        "Synthesis (Haber-Bosch)": synthesis,
    }
    
    return total_kwh, breakdown


def calculate_water_requirement(h2_kg_day: float) -> float:
    """
    Calculate daily water requirement for electrolysis.
    
    Args:
        h2_kg_day: H2 requirement (kg/day)
    
    Returns:
        Water requirement (m³/day)
    """
    water_kg = h2_kg_day * WATER_USAGE_PER_KG_H2
    water_m3 = water_kg / 1000  # 1 m³ = 1000 kg water
    return water_m3


def calculate_co2_intensity(
    total_kwh_day: float,
    nh3_kg_day: float,
    use_solar: bool = True,
    grid_co2_factor: float = 0.48,
    solar_co2_factor: float = SOLAR_CO2_FACTOR,
) -> float:
    """
    Calculate CO2 intensity (kg CO2 per kg NH3).
    
    Args:
        total_kwh_day: Daily energy requirement (kWh/day)
        nh3_kg_day: Daily NH3 production (kg/day)
        use_solar: If True, use solar factor; else grid factor
        grid_co2_factor: kg CO2 / kWh from grid
        solar_co2_factor: kg CO2 / kWh from solar
    
    Returns:
        CO2 intensity (kg CO2 / kg NH3)
    """
    co2_factor = solar_co2_factor if use_solar else grid_co2_factor
    total_co2_day = total_kwh_day * co2_factor
    co2_per_kg = total_co2_day / nh3_kg_day if nh3_kg_day > 0 else 0
    return co2_per_kg


def calculate_cost(
    nh3_tons_day: float,
    water_m3_day: float,
    electricity_kwh_day: float,
    water_cost_usd_m3: float,
    electricity_cost_usd_kwh: float,
    capex_amortization_usd_per_ton: float = 50,
) -> float:
    """
    Calculate cost per ton of NH3.
    
    Args:
        nh3_tons_day: Daily production (tons/day)
        water_m3_day: Daily water use (m³/day)
        electricity_kwh_day: Daily electricity (kWh/day)
        water_cost_usd_m3: Cost per m³
        electricity_cost_usd_kwh: Cost per kWh
        capex_amortization_usd_per_ton: Fixed cost per ton
    
    Returns:
        Cost (USD/ton NH3)
    """
    nh3_kg_day = nh3_tons_day * 1000
    daily_water_cost = water_m3_day * water_cost_usd_m3
    daily_electricity_cost = electricity_kwh_day * electricity_cost_usd_kwh
    daily_opex = daily_water_cost + daily_electricity_cost
    
    opex_per_kg = daily_opex / nh3_kg_day if nh3_kg_day > 0 else 0
    cost_per_kg = (opex_per_kg * 1000) + capex_amortization_usd_per_ton / 1000
    cost_per_ton = cost_per_kg * 1000
    
    return cost_per_ton


def process_model(config: ProcessConfig) -> ProcessResults:
    """
    Complete process model: stoichiometry → energy → cost → results.
    
    Args:
        config: ProcessConfig instance
    
    Returns:
        ProcessResults with all KPIs
    """
    # Mass balance
    mass_balance = calculate_mass_balance(config.target_nh3_day)
    h2_kg_day = mass_balance["h2_kg_day"]
    n2_kg_day = mass_balance["n2_kg_day"]
    nh3_kg_day = mass_balance["nh3_kg_day"]
    
    # Energy balance
    total_kwh, energy_breakdown = calculate_energy_balance(
        h2_kg_day=h2_kg_day,
        n2_kg_day=n2_kg_day,
        nh3_kg_day=nh3_kg_day,
        electrolyser_eff=config.electrolyser_efficiency,
        n2_sep_energy=config.n2_separation_energy,
        synthesis_energy=config.synthesis_energy,
        catalyst_factor=config.catalyst_factor,
    )
    
    # Water requirement
    water_m3 = calculate_water_requirement(h2_kg_day)
    
    # CO2 intensity
    co2_intensity = calculate_co2_intensity(
        total_kwh_day=total_kwh,
        nh3_kg_day=nh3_kg_day,
        use_solar=True,  # Assume solar by default
    )
    
    # Cost
    cost_per_ton = calculate_cost(
        nh3_tons_day=config.target_nh3_day,
        water_m3_day=water_m3,
        electricity_kwh_day=total_kwh,
        water_cost_usd_m3=config.water_cost_usd_m3,
        electricity_cost_usd_kwh=config.electricity_cost_usd_kwh,
    )
    
    # Urea production (optional)
    urea_tons_day = None
    if config.include_urea:
        urea_kg_day = nh3_kg_day * STOICH_NH3_TO_UREA
        urea_tons_day = urea_kg_day / 1000
    
    return ProcessResults(
        nh3_tons_day=config.target_nh3_day,
        water_m3_day=water_m3,
        electricity_kwh_day=total_kwh,
        co2_intensity_kg_per_kg_nh3=co2_intensity,
        cost_usd_per_ton_nh3=cost_per_ton,
        urea_tons_day=urea_tons_day,
        energy_breakdown=energy_breakdown,
    )
