"""
Quantum-ready catalyst scoring module.
Mock/surrogate implementation; can be swapped with IBM Quantum jobs in future.
"""
import numpy as np
from typing import Dict, Any
from core.constants import QUANTUM_SEED, CATALYST_CANDIDATES


class QuantumCatalystScorer:
    """
    Mock quantum catalyst scorer using pseudo-random model.
    Represents a placeholder for future quantum chemistry simulations.
    """
    
    def __init__(self, seed: int = QUANTUM_SEED):
        """Initialize with fixed seed for reproducibility."""
        self.rng = np.random.RandomState(seed)
        self.candidates = CATALYST_CANDIDATES.copy()
    
    def score_catalyst(self, candidate: Dict[str, str]) -> Dict[str, Any]:
        """
        Score a catalyst candidate.
        
        Args:
            candidate: dict with 'name' and 'notes'
        
        Returns:
            dict with 'score', 'confidence', 'notes', 'energy_barrier'
        """
        name = candidate.get("name", "Unknown")
        notes = candidate.get("notes", "")
        
        # Pseudo-random score based on name hash
        name_hash = sum(ord(c) for c in name) % 100
        base_score = (50 - name_hash * 0.3) + self.rng.normal(0, 5)
        base_score = np.clip(base_score, 10, 90)
        
        # Energy barrier (lower is better) in kcal/mol
        energy_barrier = 30 + (100 - base_score) * 0.2
        
        # Confidence based on "maturity"
        maturity_keywords = ["state-of-art", "experimental", "theoretical"]
        confidence = 0.7
        if "state-of-art" in notes.lower():
            confidence = 0.85
        elif "theoretical" in notes.lower():
            confidence = 0.60
        
        return {
            "name": name,
            "quantum_score": base_score,
            "energy_barrier_kcal_mol": energy_barrier,
            "confidence": confidence,
            "notes": notes,
            "calculation_type": "Surrogate Model (Mock Quantum)",
        }
    
    def rank_candidates(self) -> list:
        """
        Rank all candidate catalysts.
        
        Returns:
            List of scored candidates sorted by score (descending).
        """
        scores = []
        for candidate in self.candidates:
            score_result = self.score_catalyst(candidate)
            scores.append(score_result)
        
        scores.sort(key=lambda x: x["quantum_score"], reverse=True)
        return scores


def get_scorer() -> QuantumCatalystScorer:
    """Convenience function to get scorer instance."""
    return QuantumCatalystScorer()


# Pre-defined candidates
QUANTUM_CANDIDATES = [
    {"name": "Ruthenium-Carbon Nanofibre", "notes": "State-of-art industrial catalyst"},
    {"name": "Iron-Molybdenum Oxide", "notes": "Low-cost, experimental"},
    {"name": "Perovskite ABO3", "notes": "Emerging structure, theoretical optimum"},
    {"name": "Metal-Organic Framework (MOF)", "notes": "High surface area, experimental"},
    {"name": "Single-Atom Ruthenium on Nitrogen-Doped Carbon", "notes": "Theoretical optimum"},
]
