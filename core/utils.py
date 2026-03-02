"""
Utility functions.
"""
import json
from typing import Dict, Any
from pathlib import Path


def load_defaults(filepath: str = "data/defaults.json") -> Dict[str, Any]:
    """
    Load default configuration from JSON file.
    
    Args:
        filepath: Path to defaults.json
    
    Returns:
        Dictionary of default values
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_defaults(config: Dict[str, Any], filepath: str = "data/defaults.json") -> None:
    """
    Save configuration to JSON file.
    
    Args:
        config: Configuration dictionary
        filepath: Path to save
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(config, f, indent=2)


def format_currency(value: float, currency: str = "USD") -> str:
    """Format value as currency."""
    if currency == "USD":
        return f"${value:.2f}"
    elif currency == "AED":
        return f"{value:.2f} AED"
    return f"{value:.2f}"


def format_metric(value: float, unit: str, decimals: int = 2) -> str:
    """Format metric value with unit."""
    return f"{value:.{decimals}f} {unit}"
