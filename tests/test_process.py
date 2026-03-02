"""
Unit tests for process model calculations.
"""
import unittest
from core.process import (
    calculate_mass_balance,
    calculate_energy_balance,
    calculate_water_requirement,
    calculate_co2_intensity,
    calculate_cost,
    process_model,
)
from core.models import ProcessConfig
from core.constants import STOICH_H2_TO_NH3, STOICH_N2_TO_NH3, WATER_USAGE_PER_KG_H2


class TestMassBalance(unittest.TestCase):
    """Test stoichiometric mass balance."""
    
    def test_mass_balance_1_ton_nh3(self):
        """Test for 1 ton NH3 production."""
        result = calculate_mass_balance(1.0)
        
        # Expected: N2 + 3H2 → 2NH3
        # 1 ton NH3 = 1000 kg
        expected_h2 = 1000 * STOICH_H2_TO_NH3
        expected_n2 = 1000 * STOICH_N2_TO_NH3
        
        self.assertAlmostEqual(result["h2_kg_day"], expected_h2, places=1)
        self.assertAlmostEqual(result["n2_kg_day"], expected_n2, places=1)
        self.assertAlmostEqual(result["nh3_kg_day"], 1000, places=1)
    
    def test_mass_balance_5_tons_nh3(self):
        """Test for 5 tons NH3 production."""
        result = calculate_mass_balance(5.0)
        
        # Scaling: 5x larger
        self.assertAlmostEqual(result["nh3_kg_day"], 5000, places=0)
        self.assertAlmostEqual(result["h2_kg_day"], 5000 * STOICH_H2_TO_NH3, places=0)
        self.assertAlmostEqual(result["n2_kg_day"], 5000 * STOICH_N2_TO_NH3, places=0)


class TestEnergyBalance(unittest.TestCase):
    """Test energy calculations."""
    
    def test_energy_balance_baseline(self):
        """Test baseline energy calculation."""
        h2_kg = 200  # 200 kg H2/day
        n2_kg = 150  # ~150 kg N2/day (adjustment for stoich)
        nh3_kg = 850  # 850 kg NH3/day
        
        electrolyser_eff = 45.0  # kWh/kg H2
        n2_sep_energy = 0.5  # kWh/kg N2
        synthesis_energy = 8.0  # kWh/kg NH3
        
        total_kwh, breakdown = calculate_energy_balance(
            h2_kg=h2_kg,
            n2_kg=n2_kg,
            nh3_kg=nh3_kg,
            electrolyser_eff=electrolyser_eff,
            n2_sep_energy=n2_sep_energy,
            synthesis_energy=synthesis_energy,
        )
        
        # Verify breakdown
        expected_electrolysis = 200 * 45.0  # 9000 kWh
        self.assertAlmostEqual(breakdown["Electrolysis"], expected_electrolysis, places=0)
        
        # Check total
        self.assertGreater(total_kwh, 0)
        self.assertEqual(total_kwh, sum(breakdown.values()))
    
    def test_catalyst_factor(self):
        """Test catalyst factor reduces synthesis energy."""
        h2_kg, n2_kg, nh3_kg = 100, 75, 500
        electrolyser_eff, n2_sep_energy, synthesis_energy = 45.0, 0.5, 8.0
        
        # Baseline
        total_baseline, breakdown_baseline = calculate_energy_balance(
            h2_kg, n2_kg, nh3_kg, electrolyser_eff, n2_sep_energy, synthesis_energy, 1.0
        )
        
        # With catalyst improvement (0.5x energy)
        total_improved, breakdown_improved = calculate_energy_balance(
            h2_kg, n2_kg, nh3_kg, electrolyser_eff, n2_sep_energy, synthesis_energy, 0.5
        )
        
        # Improved should be significantly lower
        self.assertLess(total_improved, total_baseline)
        self.assertLess(
            breakdown_improved["Synthesis (Haber-Bosch)"],
            breakdown_baseline["Synthesis (Haber-Bosch)"]
        )


class TestWaterRequirement(unittest.TestCase):
    """Test water usage calculations."""
    
    def test_water_requirement(self):
        """Test water requirement for electrolysis."""
        h2_kg = 100  # 100 kg H2
        water_m3 = calculate_water_requirement(h2_kg)
        
        # Expected: 100 kg H2 * 9 kg water/kg H2 = 900 kg water = 0.9 m3
        expected_water = h2_kg * WATER_USAGE_PER_KG_H2 / 1000
        self.assertAlmostEqual(water_m3, expected_water, places=2)


class TestCO2Intensity(unittest.TestCase):
    """Test CO2 emissions calculations."""
    
    def test_co2_solar_vs_grid(self):
        """Test CO2 intensity difference between solar and grid."""
        total_kwh = 10000  # 10,000 kWh/day
        nh3_kg = 1000  # 1000 kg NH3
        
        # Solar
        co2_solar = calculate_co2_intensity(total_kwh, nh3_kg, use_solar=True)
        
        # Grid
        co2_grid = calculate_co2_intensity(total_kwh, nh3_kg, use_solar=False)
        
        # Grid should have much higher CO2
        self.assertLess(co2_solar, co2_grid)
        self.assertGreater(co2_grid, co2_solar * 10)  # Grid >> Solar


class TestCost(unittest.TestCase):
    """Test cost calculations."""
    
    def test_cost_calculation(self):
        """Test cost per ton NH3."""
        nh3_tons_day = 1.0  # 1 ton/day
        water_m3_day = 10.0  # 10 m3/day
        electricity_kwh_day = 15000.0  # 15,000 kWh/day
        water_cost = 1.5  # USD/m3
        elec_cost = 0.04  # USD/kWh
        
        cost = calculate_cost(
            nh3_tons_day=nh3_tons_day,
            water_m3_day=water_m3_day,
            electricity_kwh_day=electricity_kwh_day,
            water_cost_usd_m3=water_cost,
            electricity_cost_usd_kwh=elec_cost,
        )
        
        # Cost should be non-negative and reasonable
        self.assertGreater(cost, 0)
        self.assertLess(cost, 1000)  # Should be under 1000 USD/ton


class TestProcessModel(unittest.TestCase):
    """Test complete process model."""
    
    def test_process_model_execution(self):
        """Test full process model execution."""
        config = ProcessConfig(
            target_nh3_day=5.0,
            solar_capacity_mw=50.0,
            electrolyser_efficiency=45.0,
            n2_separation_energy=0.5,
            synthesis_energy=8.0,
            catalyst_factor=1.0,
            capacity_factor=0.25,
            water_cost_usd_m3=1.5,
            electricity_cost_usd_kwh=0.04,
            include_urea=False,
        )
        
        results = process_model(config)
        
        # Verify results are reasonable
        self.assertEqual(results.nh3_tons_day, 5.0)
        self.assertGreater(results.water_m3_day, 0)
        self.assertGreater(results.electricity_kwh_day, 0)
        self.assertGreater(results.cost_usd_per_ton_nh3, 0)
        self.assertGreaterEqual(results.co2_intensity_kg_per_kg_nh3, 0)
        
        # Energy breakdown should sum to total
        total_energy = sum(results.energy_breakdown.values())
        self.assertAlmostEqual(total_energy, results.electricity_kwh_day, places=0)


if __name__ == "__main__":
    unittest.main()
