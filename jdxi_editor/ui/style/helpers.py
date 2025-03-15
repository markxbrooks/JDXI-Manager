"""
Module: style helpers

This module provides functions for dynamically generating Qt style sheets for
various UI components, including sequencer buttons, general buttons, tabs, and editors.
These functions allow for flexible styling customization based on application states.

Functions:
----------
- generate_polyend_sequencer_button_style(is_checked: bool, is_current: bool) -> str:
    Generates a button style for a Polyend-style sequencer based on its checked and current step state.

- generate_sequencer_button_style(active: bool) -> str:
    Generates a QPushButton style for a step sequencer, updating colors based on active/inactive state.

- generate_button_style(bg, border, radius, text_color, hover, border_pressed, ...) -> str:
    Creates a flexible button style dynamically with customizable properties.

- generate_tab_style(bg, border, radius, text_color, hover_bg, hover_border, ...) -> str:
    Generates a QTabBar style for tabs with selectable and hover effects.

- generate_editor_style(accent, accent_hover, background, foreground, font_family, ...) -> str:
    Defines the style for an editor-like UI component, including sliders, buttons, and group boxes.

- toggle_button_style(button, checked: bool):
    Updates the given button's style based on whether it is checked.

- update_button_style(button, checked: bool):
    Toggles the button style dynamically.

- get_button_styles(active: bool) -> str:
    Returns a style sheet string for buttons in active or inactive states.

These functions help ensure a cohesive and visually distinct UI experience, particularly in MIDI sequencers or
other interactive applications.

"""


def generate_polyend_sequencer_button_style(self, is_checked: bool, is_current: bool = False) -> str:
    """Generate button style based on state and current step"""
    base_color = "#3498db" if is_checked else "#2c3e50"
    border_color = "#e74c3c" if is_current else base_color

    return f"""
        QPushButton {{
            background-color: {base_color};
            border: 2px solid {border_color};
            border-radius: 5px;
            color: white;
            padding: 2px;
        }}
        QPushButton:hover {{
            background-color: {'#2980b9' if is_checked else '#34495e'};
        }}
        QPushButton:pressed {{
            background-color: {'#2472a4' if is_checked else '#2c3e50'};
        }}
    """


def generate_sequencer_button_style(active):
    return f"""
        QPushButton {{
            border: 4px solid {'#ff6666' if active else '#666666'};
            background-color: {'#333333' if active else 'black'};
            border-radius: 3px;
            padding: 0px;
        }}
        QPushButton:hover {{
            background-color: #1A1A1A;
            border-color: #ff4d4d;
        }}
        QPushButton:border_pressed {{
            background-color: #333333;
            border-color: #ff6666;
        }}
    """


def generate_button_style(
        bg,
        border,
        radius,
        text_color,
        hover,
        border_pressed,
        background_pressed="#666666",
        button_border_width=4,
        font_family="Myriad Pro, Arial, sans-serif",
        font_size="12px",
        button_padding=4,
):
    """Generate address button style dynamically."""
    return f"""
            QPushButton {{
                background-color: {bg};
                border: {button_border_width}px solid {border};
                border-radius: {radius}px;
                color: {text_color};
                font-family: {font_family};
                font-size: {font_size};
                padding: {button_padding}px;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
            QPushButton:border_pressed, QPushButton:checked {{
                background-color: {background_pressed};
                border: {button_border_width}px solid {border_pressed};
            }}
        """


def generate_tab_style(
        bg,
        border,
        radius,
        text_color,
        hover_bg,
        hover_border,
        selected_bg,
        selected_border,
        font_family="Myriad Pro, Arial, sans-serif",
        font_size="12px",
        padding="2px 2px",
        margin="2px",
):
    """Generate address tab style dynamically."""
    return f"""
            QTabBar::tab {{
                background: {bg};
                color: {text_color};
                padding: {padding};
                margin: {margin};
                border: 2px solid {border};
                border-radius: {radius}px;
                font-family: {font_family};
                font-size: {font_size};
            }}

            QTabBar::tab:selected {{
                background: {selected_bg};
                color: {text_color};
                border: 2px solid {selected_border};
                font-family: {font_family};
                font-size: {font_size};
            }}

            QTabBar::tab:hover {{
                background: {hover_bg};
                border: 2px solid {hover_border};
                font-family: {font_family};
                font-size: {font_size};
            }}

            QTabWidget::pane {{
                border: 1px solid {selected_border};
            }}
        """

    # Editor Styles


def generate_editor_style(
        accent,
        accent_hover,
        background,
        foreground,
        font_family,
        font_size,
        padding,
        button_padding,
        slider_handle,
        slider_handle_border,
        slider_groove,
):
    return f"""
        QWidget {{
            background-color: {background};
            color: {foreground};
            font-family: {font_family};
            font-size: {font_size};
            padding: 2px;
        }}

        QGroupBox {{
            border: 1px solid {accent};
            border-radius: 3px;
            margin-top: 2px;
            padding: {padding}px;
        }}

        QGroupBox[adsr="true"] {{
            min-height: 300px;  /* Reduced height for horizontal layout */
        }}

        QSlider::handle:vertical {{
            background: {slider_handle};
            border: 2px solid {slider_handle_border};
            margin: 1px 0;
            border-radius: 4px;
        }}

        QSlider::handle:vertical:hover {{
            border-color: {accent_hover};
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 3px;
            color: {foreground};
        }}

        QPushButton {{
            background-color: {background};
            border: 1px solid {accent};
            border-radius: 3px;
            padding: {button_padding}px;
            color: {foreground};
        }}

        QPushButton:hover, QPushButton:checked {{
            background-color: {accent};
            color: {background};
        }}

        QComboBox, QScrollBar {{
            background-color: {background};
            border: 1px solid {accent};
            border-radius: 3px;
            padding: 3px;
            color: {foreground};
        }}

        QScrollBar::handle {{
            background: {slider_handle_border};
            border-radius: 3px;
        }}

        QScrollBar::handle:hover {{
            border: 2px solid {accent};
        }}

        QSlider::groove:horizontal {{
            background: {slider_groove};
            height: 2px;
            border-radius: 1px;
        }}

        QSlider::handle:horizontal{{
            background: {slider_handle};
            border: 2px solid {slider_handle_border};
            width: 18px;
            height: 14px;
            margin: -9px 0;
            border-radius: 9px;
        }}
        QSlider::handle:vertical {{
            background: {slider_handle};
            border: 2px solid {slider_handle_border};
            width: 18px;
            height: 12px;
            margin: -9px 0;
            border-radius: 9px;
        }}
    """

def get_button_styles(active):
    """Returns the appropriate style for active/inactive states"""
    base_style = """
        QPushButton {
            border-radius: 15px;
            border: 4px solid;
        }
        QPushButton:border_pressed {
            background-color: #333333;
            border: 4px solid #ff6666;
        }
        QPushButton:hover {
            background-color: #1A1A1A;
            border: 4px solid #ff4d4d;
        }
    """
    if active:
        return (
                base_style
                + """
            QPushButton {
                background-color: #333333;
                border-color: #ff6666;
            }
        """
        )
    else:
        return (
                base_style
                + """
            QPushButton {
                background-color: #222222;
                border-color: #666666;
            }
        """
        )


def toggle_button_style(button, checked):
    """Update button style based on its checked state"""
    button.setStyleSheet(
        generate_sequencer_button_style(checked)
    )  # Example style for checked


def update_button_style(button, checked):
    """Toggle the button style based on the state"""
    button.setStyleSheet(get_button_styles(checked))
