"""
utils.py

Provides utility functions for CLI styling, text formatting, and robust user 
input validation with try-except blocks. This forms a foundational layer of 
the application to ensure errors are handled gracefully without application crashes.
"""

import os
import sys

# ANSI Escape Sequences for terminal styling
# These provide the "wow factor" and premium design aesthetic in a standard terminal.
COLOR_HEADER = "\033[95m"    # Light Magenta
COLOR_BLUE = "\033[94m"      # Light Blue
COLOR_CYAN = "\033[96m"      # Light Cyan
COLOR_GREEN = "\033[92m"     # Light Green
COLOR_YELLOW = "\033[93m"    # Light Yellow
COLOR_RED = "\033[91m"       # Light Red
STYLE_BOLD = "\033[1m"       # Bold
STYLE_UNDERLINE = "\033[4m"  # Underline
STYLE_RESET = "\033[0m"      # Reset formatting

# Initialize ANSI on Windows systems where it might be disabled by default
if sys.platform.startswith("win"):
    os.system("color")


def style_text(text: str, *styles: str) -> str:
    """
    Applies ANSI escape styles to a given string.
    
    Parameters:
        text (str): The raw string to be styled.
        *styles (str): One or more ANSI code strings (e.g., COLOR_GREEN, STYLE_BOLD).
        
    Returns:
        str: The styled string.
    """
    prefix = "".join(styles)
    return f"{prefix}{text}{STYLE_RESET}"


def clear_screen() -> None:
    """Clears the terminal screen depending on the OS."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner(title: str) -> None:
    """
    Prints a premium, eye-catching visual banner to separate CLI sections.
    
    Parameters:
        title (str): The title of the banner to print.
    """
    border = "=" * 60
    styled_border = style_text(border, COLOR_CYAN, STYLE_BOLD)
    styled_title = style_text(title.center(60), COLOR_HEADER, STYLE_BOLD)
    print(f"\n{styled_border}")
    print(styled_title)
    print(f"{styled_border}\n")


def get_str_input(prompt: str, allow_empty: bool = False, min_len: int = 1) -> str:
    """
    Prompts the user for a string and validates that it meets length requirements.
    Uses loops and standard logic to prevent invalid empty fields.
    
    Parameters:
        prompt (str): The input prompt message.
        allow_empty (bool): Whether empty strings are permitted.
        min_len (int): Minimum length if allow_empty is False.
        
    Returns:
        str: The validated user input.
    """
    while True:
        try:
            val = input(prompt).strip()
            if not val and not allow_empty:
                print(style_text("Error: Input cannot be empty. Please enter a value.", COLOR_RED))
                continue
            if not allow_empty and len(val) < min_len:
                print(style_text(f"Error: Input must be at least {min_len} characters long.", COLOR_RED))
                continue
            return val
        except (KeyboardInterrupt, EOFError):
            print(style_text("\nOperation interrupted. Reverting to menu.", COLOR_YELLOW))
            raise


def get_int_input(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """
    Prompts the user for an integer and handles invalid conversions using try-except.
    Validates range boundaries if provided.
    
    Parameters:
        prompt (str): The input prompt message.
        min_val (int): Optional minimum acceptable value.
        max_val (int): Optional maximum acceptable value.
        
    Returns:
        int: The validated integer input.
    """
    while True:
        try:
            val_str = input(prompt).strip()
            val = int(val_str)
            
            if min_val is not None and val < min_val:
                print(style_text(f"Error: Value must be at least {min_val}.", COLOR_RED))
                continue
            if max_val is not None and val > max_val:
                print(style_text(f"Error: Value cannot exceed {max_val}.", COLOR_RED))
                continue
            return val
        except ValueError:
            print(style_text("Error: Invalid numeric format. Please enter an integer.", COLOR_RED))
        except (KeyboardInterrupt, EOFError):
            print(style_text("\nOperation interrupted. Reverting to menu.", COLOR_YELLOW))
            raise


def get_float_input(prompt: str, min_val: float = None, max_val: float = None) -> float:
    """
    Prompts the user for a float (e.g. grades) and handles conversions using try-except.
    Validates range boundaries (e.g. 0 to 100).
    
    Parameters:
        prompt (str): The input prompt message.
        min_val (float): Optional minimum acceptable value.
        max_val (float): Optional maximum acceptable value.
        
    Returns:
        float: The validated float input.
    """
    while True:
        try:
            val_str = input(prompt).strip()
            val = float(val_str)
            
            if min_val is not None and val < min_val:
                print(style_text(f"Error: Value must be at least {min_val}.", COLOR_RED))
                continue
            if max_val is not None and val > max_val:
                print(style_text(f"Error: Value cannot exceed {max_val}.", COLOR_RED))
                continue
            return val
        except ValueError:
            print(style_text("Error: Invalid decimal format. Please enter a number.", COLOR_RED))
        except (KeyboardInterrupt, EOFError):
            print(style_text("\nOperation interrupted. Reverting to menu.", COLOR_YELLOW))
            raise


def confirm_action(prompt: str) -> bool:
    """
    Asks the user to confirm an action (y/n).
    
    Parameters:
        prompt (str): The prompt question.
        
    Returns:
        bool: True if confirmed, False otherwise.
    """
    while True:
        try:
            response = input(f"{prompt} (y/n): ").strip().lower()
            if response in ('y', 'yes'):
                return True
            elif response in ('n', 'no'):
                return False
            else:
                print(style_text("Please enter 'y' or 'n'.", COLOR_YELLOW))
        except (KeyboardInterrupt, EOFError):
            return False
