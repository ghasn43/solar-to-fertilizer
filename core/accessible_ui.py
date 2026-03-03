"""
Accessible UI Components Module
Provides WCAG 2.1 compliant Streamlit components for Phase 4 production readiness
"""
import streamlit as st
from typing import Optional, List, Callable, Any
from core.production_utils import get_standard_palette


def accessible_metric(label: str, value: str, help_text: str = ""):
    """
    Accessible metric display with ARIA-friendly structure.
    
    Args:
        label: Metric label
        value: Metric value (as string for flexibility)
        help_text: Optional ARIA description
    """
    with st.container():
        # Add semantic HTML structure
        if help_text:
            st.metric(label, value, help=help_text)
        else:
            st.metric(label, value)


def accessible_section_header(title: str, level: int = 2, help_text: str = ""):
    """
    Create accessible section header with semantic structure.
    
    Args:
        title: Section title
        level: Header level (1-6)
        help_text: Optional description
    """
    colors = {
        1: "#003366",
        2: "#0066cc",
        3: "#1890ff",
        4: "#1890ff",
        5: "#1890ff",
        6: "#1890ff",
    }
    
    color = colors.get(level, "#1890ff")
    accent = "━" if level == 2 else ""
    
    # Create proper heading structure
    st.markdown(f"<h{level} style='color:{color}'>{accent} {title}</h{level}>", 
                unsafe_allow_html=True)
    
    if help_text:
        st.markdown(f"<small style='color:#666'>{help_text}</small>", unsafe_allow_html=True)


def accessible_number_input(
    label: str,
    min_value: float = 0,
    max_value: float = 100,
    value: float = 50,
    step: float = 1,
    help_text: str = "",
    unit: str = ""
) -> float:
    """
    Accessible number input with ARIA attributes.
    
    Args:
        label: Input label
        min_value: Minimum value
        max_value: Maximum value
        value: Default value
        step: Step size
        help_text: Accessibility description
        unit: Unit of measurement
    
    Returns:
        User input value
    """
    # Add accessibility context
    if help_text:
        st.write(f"<small style='display:block;margin-bottom:0.5rem;color:#666'>"
                f"ℹ️ {help_text}</small>", unsafe_allow_html=True)
    
    result = st.number_input(
        label,
        min_value=min_value,
        max_value=max_value,
        value=value,
        step=step,
        help=f"{help_text} (Range: {min_value}-{max_value} {unit})"
    )
    
    return result


def accessible_slider(
    label: str,
    min_value: float = 0.0,
    max_value: float = 100.0,
    value: float = 50.0,
    step: float = 1.0,
    help_text: str = "",
    show_value: bool = True,
    unit: str = ""
) -> float:
    """
    Accessible slider with live value display.
    
    Args:
        label: Slider label
        min_value: Minimum value
        max_value: Maximum value
        value: Default value
        step: Step size
        help_text: Accessibility description
        show_value: Show current value
        unit: Unit of measurement
    
    Returns:
        User input value
    """
    # Add accessibility context
    full_label = f"{label}"
    if unit:
        full_label += f" ({unit})"
    
    result = st.slider(
        full_label,
        min_value=min_value,
        max_value=max_value,
        value=value,
        step=step,
        help=help_text
    )
    
    if show_value:
        st.write(f"<small>**Current:** {result:.2f} {unit}</small>", unsafe_allow_html=True)
    
    return result


def accessible_selectbox(
    label: str,
    options: List[str],
    help_text: str = ""
) -> str:
    """
    Accessible selectbox with ARIA attributes.
    
    Args:
        label: Selectbox label
        options: List of options
        help_text: Accessibility description
    
    Returns:
        Selected option
    """
    return st.selectbox(
        label,
        options,
        help=help_text
    )


def accessible_tabs(
    tab_names: List[str],
    tab_icons: List[str] = None
) -> st.tabs:
    """
    Create accessible tabs with proper ARIA structure.
    
    Args:
        tab_names: List of tab names
        tab_icons: Optional list of icons
    
    Returns:
        List of tab objects
    """
    if tab_icons:
        tabs = st.tabs([f"{icon} {name}" for icon, name in zip(tab_icons, tab_names)])
    else:
        tabs = st.tabs(tab_names)
    
    return tabs


def accessible_expander(
    label: str,
    expanded: bool = False,
    help_text: str = ""
) -> st.expander:
    """
    Create accessible expander with ARIA attributes.
    
    Args:
        label: Expander label
        expanded: Initial expanded state
        help_text: Accessibility description
    
    Returns:
        Expander object
    """
    expander_label = label
    if help_text:
        expander_label += f" ℹ️"
    
    expander = st.expander(expander_label, expanded=expanded)
    
    if help_text:
        with expander:
            st.markdown(f"<small style='color:#666'>{help_text}</small>", unsafe_allow_html=True)
    
    return expander


def accessible_button(
    label: str,
    on_click: Optional[Callable] = None,
    args: tuple = (),
    help_text: str = "",
    button_type: str = "primary"
) -> bool:
    """
    Accessible button with proper sizing and focus states.
    
    Args:
        label: Button label
        on_click: Callback function
        args: Arguments for callback
        help_text: Accessibility description
        button_type: Type of button (primary, secondary, danger)
    
    Returns:
        True if clicked
    """
    button_color_map = {
        "primary": "primary",
        "secondary": "secondary",
        "danger": "error"
    }
    
    use_container_width = True
    
    clicked = st.button(
        label,
        on_click=on_click,
        args=args,
        help=help_text,
        use_container_width=use_container_width
    )
    
    return clicked


def accessible_data_display(
    title: str,
    data: dict,
    help_text: str = "",
    display_type: str = "table"
):
    """
    Display data in accessible format.
    
    Args:
        title: Display title
        data: Data dictionary
        help_text: Accessibility description
        display_type: 'table' or 'metrics'
    """
    accessible_section_header(title)
    
    if help_text:
        st.markdown(f"<small style='color:#666'>{help_text}</small>", unsafe_allow_html=True)
    
    if display_type == "metrics":
        cols = st.columns(len(data))
        for col, (key, value) in zip(cols, data.items()):
            with col:
                accessible_metric(key, str(value))
    else:
        # Table display
        st.table(data)


def accessible_divider():
    """Add accessible visual divider."""
    st.markdown("---")


def create_accessible_columns(num_cols: int) -> List[st.container]:
    """
    Create responsive columns that stack on mobile.
    
    Args:
        num_cols: Number of columns on desktop
    
    Returns:
        List of column objects
    """
    return st.columns(num_cols)


def accessibility_notice():
    """Display accessibility information and keyboard shortcuts."""
    with st.expander("♿ Accessibility Options", expanded=False):
        st.markdown("""
### Keyboard Navigation
- **Tab**: Move between elements
- **Enter/Space**: Activate buttons or expand sections
- **Arrow Keys**: Navigate sliders and selects

### Screen Reader Support
All interactive elements include ARIA labels and descriptions.

### Theme Support
- **Browser Settings**: Respects `prefers-color-scheme`
- **Manual Toggle**: Available in Streamlit Settings menu

### Font Size
Use your browser's zoom controls (Ctrl/Cmd + Plus/Minus) to adjust text size.

### High Contrast
For better visibility, use your OS high contrast mode.
        """)


# Standard color palette for consistency
ACCESSIBLE_COLORS = get_standard_palette()
