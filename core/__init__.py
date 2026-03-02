"""
Core package for S2F-DT.
"""
from core.models import ProcessConfig, ProcessResults
from core.process import (
    calculate_mass_balance,
    calculate_energy_balance,
    calculate_water_requirement,
    calculate_co2_intensity,
    calculate_cost,
    process_model,
)
from core.scenarios import (
    create_scenario_1_baseline,
    create_scenario_2_uae_green,
    create_scenario_3_future_catalyst,
    compare_scenarios,
)
from core.optimizer import grid_search_optimizer, display_top_solutions
from core.quantum_stub import QuantumCatalystScorer, get_scorer
from core.reporting import generate_pdf_report, export_config_json
from core.utils import load_defaults, save_defaults, format_currency, format_metric

__all__ = [
    "ProcessConfig",
    "ProcessResults",
    "calculate_mass_balance",
    "calculate_energy_balance",
    "calculate_water_requirement",
    "calculate_co2_intensity",
    "calculate_cost",
    "process_model",
    "create_scenario_1_baseline",
    "create_scenario_2_uae_green",
    "create_scenario_3_future_catalyst",
    "compare_scenarios",
    "grid_search_optimizer",
    "display_top_solutions",
    "QuantumCatalystScorer",
    "get_scorer",
    "generate_pdf_report",
    "export_config_json",
    "load_defaults",
    "save_defaults",
    "format_currency",
    "format_metric",
]
