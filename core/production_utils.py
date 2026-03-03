"""
Production utilities for Phase 4: Production Readiness
Includes error handling, validation, caching, accessibility, and performance optimization
"""
import streamlit as st
import functools
import logging
from typing import Any, Callable, Dict, Optional, Tuple
from datetime import datetime, timedelta
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== ERROR HANDLING & VALIDATION =====

class ValidationError(Exception):
    """Custom validation error for user-facing messages."""
    pass


def validate_numeric_range(
    value: float,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
    name: str = "Value"
) -> float:
    """
    Validate that a numeric value is within acceptable range.
    
    Args:
        value: Value to validate
        min_val: Minimum acceptable value
        max_val: Maximum acceptable value
        name: Display name for error messages
    
    Returns:
        Validated value
    
    Raises:
        ValidationError: If value is outside range
    """
    if min_val is not None and value < min_val:
        raise ValidationError(f"{name} must be ≥ {min_val}")
    if max_val is not None and value > max_val:
        raise ValidationError(f"{name} must be ≤ {max_val}")
    return value


def validate_configuration(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate process configuration dictionary.
    
    Args:
        config: Configuration dictionary from session state
    
    Returns:
        Validated configuration
    
    Raises:
        ValidationError: If any required field is invalid
    """
    required_fields = {
        'target_nh3_day': (float, (0.1, 100)),
        'solar_capacity_mw': (float, (1, 1000)),
        'electrolyser_efficiency': (float, (30, 75)),
        'capacity_factor': (float, (0.1, 0.5)),
        'electricity_cost_usd_kwh': (float, (0.01, 1.0)),
        'water_cost_usd_m3': (float, (0.5, 10)),
    }
    
    validated = {}
    
    for field, (expected_type, (min_val, max_val)) in required_fields.items():
        if field not in config:
            raise ValidationError(f"Missing required field: {field}")
        
        value = config[field]
        
        if not isinstance(value, (int, float)):
            raise ValidationError(f"{field} must be numeric, got {type(value).__name__}")
        
        validated[field] = validate_numeric_range(
            float(value),
            min_val=min_val,
            max_val=max_val,
            name=field.replace('_', ' ').title()
        )
    
    # Copy any additional fields
    for key, value in config.items():
        if key not in validated:
            validated[key] = value
    
    return validated


def safe_execute(func: Callable, *args, **kwargs) -> Tuple[Optional[Any], Optional[str]]:
    """
    Safely execute a function with error handling.
    
    Args:
        func: Function to execute
        *args: Positional arguments
        **kwargs: Keyword arguments
    
    Returns:
        Tuple of (result, error_message)
        - result is None if error occurred
        - error_message is None if successful
    """
    try:
        result = func(*args, **kwargs)
        return result, None
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        return None, str(e)
    except Exception as e:
        logger.error(f"Execution error: {str(e)}", exc_info=True)
        return None, f"An error occurred: {str(e)}. Please check your inputs and try again."


# ===== CACHING & PERFORMANCE OPTIMIZATION =====

def cache_with_ttl(ttl_seconds: int = 3600):
    """
    Decorator for caching function results with TTL (time-to-live).
    More flexible than st.cache_data for complex scenarios.
    
    Args:
        ttl_seconds: Time-to-live in seconds (default 1 hour)
    
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"cache_{func.__name__}_{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Check if result exists in session state and is not expired
            if cache_key in st.session_state:
                cached_data = st.session_state[cache_key]
                if datetime.now() < cached_data['expires_at']:
                    logger.info(f"Cache hit: {func.__name__}")
                    return cached_data['result']
            
            # Execute function and cache result
            logger.info(f"Cache miss: {func.__name__} - executing...")
            result = func(*args, **kwargs)
            
            st.session_state[cache_key] = {
                'result': result,
                'expires_at': datetime.now() + timedelta(seconds=ttl_seconds)
            }
            
            return result
        
        return wrapper
    return decorator


def clear_cache(pattern: str = "cache_"):
    """
    Clear cached items matching pattern.
    
    Args:
        pattern: Pattern to match cache keys
    """
    keys_to_delete = [k for k in st.session_state.keys() if pattern in k]
    for key in keys_to_delete:
        del st.session_state[key]
    logger.info(f"Cleared {len(keys_to_delete)} cache items")


# ===== ACCESSIBILITY & THEMING =====

def configure_theme():
    """Configure Streamlit theme for accessibility and responsiveness."""
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "S2F-DT: Solar to Fertiliser Decision Toolkit v2.0 (Phase 4: Production Ready)"
        }
    )
    
    # Custom CSS for accessibility & dark mode support
    st.markdown("""
    <style>
    /* Dark mode support */
    :root {
        color-scheme: light dark;
    }
    
    /* Accessibility improvements */
    button {
        border: 2px solid currentColor;
        border-radius: 4px;
    }
    
    button:focus {
        outline: 3px solid #4CAF50;
        outline-offset: 2px;
    }
    
    /* Better contrast in dark mode */
    @media (prefers-color-scheme: dark) {
        .stMetric > div:first-child {
            color: #e0e0e0;
        }
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .stColumn {
            flex: 0 0 100% !important;
        }
    }
    
    /* Improve readability */
    .stMarkdown {
        line-height: 1.6;
    }
    
    /* Accessible input styling */
    input, select, textarea {
        min-height: 44px;
    }
    </style>
    """, unsafe_allow_html=True)


def add_aria_label(label: str, description: str = ""):
    """
    Helper to add ARIA-style descriptions for accessibility.
    
    Args:
        label: Main label
        description: Accessible description
    
    Returns:
        HTML string with accessibility attributes
    """
    if description:
        return f'<span title="{description}" role="tooltip">{label}</span>'
    return label


def responsive_columns(num_cols: int, gap: str = "medium"):
    """
    Create responsive columns that stack on mobile.
    
    Args:
        num_cols: Number of columns on desktop
        gap: Gap size (small, medium, large)
    
    Returns:
        List of column objects
    """
    # Streamlit's built-in columns already handle responsiveness
    # This is a wrapper for consistent behavior
    return st.columns(num_cols, gap=gap)


# ===== USER FEEDBACK & LOADING STATES =====

def show_loading_state(message: str = "Processing..."):
    """Display loading state with spinner."""
    with st.spinner(message):
        return True


def show_success_message(message: str, icon: str = "✅"):
    """Show success message."""
    st.success(f"{icon} {message}")


def show_error_message(message: str, icon: str = "❌"):
    """Show error message with icon."""
    st.error(f"{icon} {message}")


def show_warning_message(message: str, icon: str = "⚠️"):
    """Show warning message with icon."""
    st.warning(f"{icon} {message}")


def show_info_message(message: str, icon: str = "ℹ️"):
    """Show info message with icon."""
    st.info(f"{icon} {message}")


# ===== SAFE WIDGET WRAPPERS =====

def safe_number_input(label: str, **kwargs) -> Optional[float]:
    """
    Safe wrapper around st.number_input with validation.
    
    Args:
        label: Input label
        **kwargs: Arguments for st.number_input
    
    Returns:
        Validated numeric value or None if invalid
    """
    try:
        value = st.number_input(label, **kwargs)
        min_value = kwargs.get('min_value')
        max_value = kwargs.get('max_value')
        
        validate_numeric_range(
            value,
            min_val=min_value,
            max_val=max_value,
            name=label
        )
        
        return value
    except ValidationError as e:
        show_error_message(str(e))
        return None


def safe_slider(label: str, **kwargs) -> Optional[float]:
    """
    Safe wrapper around st.slider with validation.
    
    Args:
        label: Slider label
        **kwargs: Arguments for st.slider
    
    Returns:
        Validated slider value or None if invalid
    """
    try:
        value = st.slider(label, **kwargs)
        min_value = kwargs.get('min_value')
        max_value = kwargs.get('max_value')
        
        validate_numeric_range(
            value,
            min_val=min_value,
            max_val=max_value,
            name=label
        )
        
        return value
    except ValidationError as e:
        show_error_message(str(e))
        return None


# ===== PERFORMANCE MONITORING =====

class PerformanceMonitor:
    """Monitor and log performance metrics."""
    
    def __init__(self, operation_name: str):
        """Initialize performance monitor."""
        self.operation_name = operation_name
        self.start_time = None
        self.metrics = {}
    
    def __enter__(self):
        """Start timing."""
        self.start_time = datetime.now()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """End timing and log."""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        logger.info(f"Operation '{self.operation_name}' completed in {elapsed:.3f}s")
        self.metrics['duration_seconds'] = elapsed
        
        if elapsed > 2.0:
            logger.warning(f"Performance warning: {self.operation_name} took {elapsed:.3f}s")


# ===== CONSISTENCY & STANDARDIZATION =====

def get_standard_palette() -> Dict[str, str]:
    """Get standardized color palette for consistent UI."""
    return {
        'primary': '#0066cc',      # Blue
        'success': '#52c41a',      # Green
        'warning': '#faad14',      # Orange
        'danger': '#ff4d4f',       # Red
        'info': '#1890ff',         # Light blue
        'neutral': '#666666',      # Gray
        'light': '#f5f5f5',        # Off-white
    }


def format_energy_value(kwh: float) -> str:
    """Format energy values with appropriate units."""
    if kwh < 1000:
        return f"{kwh:.1f} kWh"
    elif kwh < 1e6:
        return f"{kwh/1000:.2f} MWh"
    else:
        return f"{kwh/1e6:.3f} GWh"


def format_water_value(m3: float) -> str:
    """Format water values with appropriate units."""
    if m3 < 1000:
        return f"{m3:.1f} m³"
    elif m3 < 1e6:
        return f"{m3/1000:.2f}K m³"
    else:
        return f"{m3/1e6:.2f}M m³"


def format_cost_value(usd: float) -> str:
    """Format cost values with appropriate units."""
    if usd < 1000:
        return f"${usd:.2f}"
    elif usd < 1e6:
        return f"${usd/1000:.1f}K"
    elif usd < 1e9:
        return f"${usd/1e6:.1f}M"
    else:
        return f"${usd/1e9:.1f}B"


# ===== SESSION STATE MANAGEMENT =====

def initialize_session_state(defaults: Dict[str, Any]):
    """
    Initialize session state with defaults, preserving existing values.
    
    Args:
        defaults: Dictionary of default values
    """
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def save_session_state(filepath: str = "data/session_backup.json"):
    """
    Save current session state to file for recovery.
    
    Args:
        filepath: Path to save session state
    """
    try:
        # Only save serializable data
        session_data = {}
        for key, value in st.session_state.items():
            try:
                json.dumps(value)  # Test if serializable
                session_data[key] = value
            except (TypeError, ValueError):
                logger.debug(f"Skipping non-serializable session key: {key}")
        
        with open(filepath, 'w') as f:
            json.dump(session_data, f, default=str, indent=2)
        
        logger.info(f"Session state saved to {filepath}")
    except Exception as e:
        logger.error(f"Failed to save session state: {e}")


def restore_session_state(filepath: str = "data/session_backup.json"):
    """
    Restore session state from file.
    
    Args:
        filepath: Path to restore from
    
    Returns:
        Dictionary of restored state or empty dict if file doesn't exist
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        logger.error(f"Failed to restore session state: {e}")
        return {}
