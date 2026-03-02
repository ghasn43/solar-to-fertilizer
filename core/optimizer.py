"""
Simple grid-search optimizer for minimizing cost or CO2 intensity.
"""
from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd
from core.constants import OPTIMIZER_SEARCH_SPACE
from core.models import ProcessConfig
from core.process import process_model


def grid_search_optimizer(
    target_nh3_tons_day: float,
    objective: str = "cost",
    lambda_weight: float = 1.0,
    grid_density: int = 5,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Grid search optimization: minimize (cost + lambda*CO2).
    
    Args:
        target_nh3_tons_day: Target production
        objective: 'cost', 'co2', or 'combined'
        lambda_weight: Weight for CO2 in combined objective
        grid_density: Number of points per dimension
    
    Returns:
        (list of solution dicts, best solution dict)
    """
    search_space = OPTIMIZER_SEARCH_SPACE
    
    # Create grid
    electrolyser_vals = np.linspace(
        search_space["electrolyser_efficiency"][0],
        search_space["electrolyser_efficiency"][1],
        grid_density
    )
    catalyst_vals = np.linspace(
        search_space["catalyst_factor"][0],
        search_space["catalyst_factor"][1],
        grid_density
    )
    solar_vals = np.linspace(
        search_space["solar_capacity_mw"][0],
        search_space["solar_capacity_mw"][1],
        grid_density
    )
    capacity_vals = np.linspace(
        search_space["capacity_factor"][0],
        search_space["capacity_factor"][1],
        grid_density
    )
    
    solutions = []
    
    for electrolyser in electrolyser_vals:
        for catalyst in catalyst_vals:
            for solar_mw in solar_vals:
                for cap_factor in capacity_vals:
                    config = ProcessConfig(
                        target_nh3_day=target_nh3_tons_day,
                        solar_capacity_mw=solar_mw,
                        electrolyser_efficiency=electrolyser,
                        n2_separation_energy=0.5,
                        synthesis_energy=8.0,
                        catalyst_factor=catalyst,
                        capacity_factor=cap_factor,
                        water_cost_usd_m3=1.5,
                        electricity_cost_usd_kwh=0.04,
                        include_urea=False,
                    )
                    
                    results = process_model(config)
                    
                    # Compute objective
                    cost = results.cost_usd_per_ton_nh3
                    co2 = results.co2_intensity_kg_per_kg_nh3 * 1000
                    
                    if objective == "cost":
                        score = cost
                    elif objective == "co2":
                        score = co2
                    else:  # 'combined'
                        # Normalize: cost in USD, CO2 in kg; scale appropriately
                        score = cost + lambda_weight * (co2 / 100)
                    
                    solutions.append({
                        "electrolyser_efficiency": electrolyser,
                        "catalyst_factor": catalyst,
                        "solar_capacity_mw": solar_mw,
                        "capacity_factor": cap_factor,
                        "cost_usd_per_ton": cost,
                        "co2_kg_per_ton": co2,
                        "score": score,
                    })
    
    # Sort by score
    solutions.sort(key=lambda x: x["score"])
    best = solutions[0]
    
    return solutions, best


def display_top_solutions(solutions: List[Dict[str, Any]], top_n: int = 10) -> pd.DataFrame:
    """
    Format top N solutions as DataFrame.
    """
    top = solutions[:top_n]
    data = [
        {
            "Rank": i + 1,
            "Electrolyser (kWh/kg H2)": f"{s['electrolyser_efficiency']:.1f}",
            "Catalyst Factor": f"{s['catalyst_factor']:.2f}",
            "Solar (MW)": f"{s['solar_capacity_mw']:.0f}",
            "Capacity Factor": f"{s['capacity_factor']:.2%}",
            "Cost (USD/ton)": f"{s['cost_usd_per_ton']:.0f}",
            "CO2 (kg/ton)": f"{s['co2_kg_per_ton']:.1f}",
        }
        for i, s in enumerate(top)
    ]
    return pd.DataFrame(data)
