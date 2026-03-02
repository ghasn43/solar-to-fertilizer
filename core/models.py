"""
Pydantic data models for configuration and results.
"""
from typing import Optional, Dict, Any
from dataclasses import dataclass

try:
    from pydantic import BaseModel, Field
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False


if HAS_PYDANTIC:
    class ProcessConfig(BaseModel):
        """Process configuration parameters."""
        target_nh3_day: float = Field(..., description="Target NH3 output (tons/day)")
        solar_capacity_mw: float = Field(..., description="Solar capacity (MW)")
        electrolyser_efficiency: float = Field(..., description="kWh/kg H2")
        n2_separation_energy: float = Field(..., description="kWh/kg N2")
        synthesis_energy: float = Field(..., description="kWh/kg NH3")
        catalyst_factor: float = Field(1.0, description="Catalyst efficiency multiplier")
        capacity_factor: float = Field(..., description="Capacity factor (fraction)")
        water_cost_usd_m3: float = Field(..., description="USD/m³")
        electricity_cost_usd_kwh: float = Field(..., description="USD/kWh")
        include_urea: bool = Field(False, description="Include Urea production")

        class Config:
            arbitrary_types_allowed = True

    class ProcessResults(BaseModel):
        """Process calculation results."""
        nh3_tons_day: float
        water_m3_day: float
        electricity_kwh_day: float
        co2_intensity_kg_per_kg_nh3: float
        cost_usd_per_ton_nh3: float
        urea_tons_day: Optional[float] = None
        energy_breakdown: Dict[str, float]

else:
    # Fallback to dataclasses if pydantic not available
    @dataclass
    class ProcessConfig:
        target_nh3_day: float
        solar_capacity_mw: float
        electrolyser_efficiency: float
        n2_separation_energy: float
        synthesis_energy: float
        catalyst_factor: float = 1.0
        capacity_factor: float = 0.25
        water_cost_usd_m3: float = 1.5
        electricity_cost_usd_kwh: float = 0.04
        include_urea: bool = False

    @dataclass
    class ProcessResults:
        nh3_tons_day: float
        water_m3_day: float
        electricity_kwh_day: float
        co2_intensity_kg_per_kg_nh3: float
        cost_usd_per_ton_nh3: float
        urea_tons_day: Optional[float] = None
        energy_breakdown: Optional[Dict[str, float]] = None


@dataclass
class ScenarioComparison:
    """Container for scenario comparison."""
    name: str
    cost_usd_per_ton: float
    co2_kg_per_ton: float
    nh3_tons_day: float
    description: str
