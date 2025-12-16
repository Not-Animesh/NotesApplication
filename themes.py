"""
WhiskerNotes - Theme Configuration
Defines color schemes and UI styling for light and dark modes
"""

class Theme:
    """Central theme configuration for WhiskerNotes"""
    
    # Light Theme Colors
    LIGHT = {
        "bg": "#F6F1E7",           # Warm cream background
        "fg": "#2C2C2C",           # Dark text
        "accent": "#F6B1C3",       # Pink accent
        "card_bg": "#FFFFFF",      # White card background
        "card_hover": "#FFE5EC",   # Light pink hover
        "button_bg": "#F6B1C3",    # Pink button
        "button_fg": "#2C2C2C",    # Dark button text
        "border": "#E8D5D5",       # Light border
        "scrollbar": "#F6B1C3",    # Pink scrollbar
    }
    
    # Dark Theme Colors
    DARK = {
        "bg": "#0F0F0F",           # Deep black background
        "fg": "#E8E8E8",           # Light text
        "accent": "#F6B1C3",       # Pink accent
        "card_bg": "#1A1A1A",      # Dark card background
        "card_hover": "#2A2A2A",   # Lighter dark hover
        "button_bg": "#F6B1C3",    # Pink button
        "button_fg": "#0F0F0F",    # Dark button text
        "border": "#2A2A2A",       # Dark border
        "scrollbar": "#F6B1C3",    # Pink scrollbar
    }
    
    # Current theme (default to light)
    current_theme = "light"
    
    @classmethod
    def get_colors(cls):
        """Get current theme colors"""
        return cls.LIGHT if cls.current_theme == "light" else cls.DARK
    
    @classmethod
    def toggle_theme(cls):
        """Toggle between light and dark themes"""
        cls.current_theme = "dark" if cls.current_theme == "light" else "light"
        return cls.current_theme
    
    @classmethod
    def is_dark(cls):
        """Check if current theme is dark"""
        return cls.current_theme == "dark"


# Cat-themed feedback messages
CAT_MESSAGES = {
    "note_saved": "Meow! Your note is safe 🐾",
    "note_deleted": "Note deleted... your cat is sad 😿",
    "note_created": "Purr! New note created 🐱",
    "no_notes": "No notes yet... your cat is waiting 🐱",
    "auto_saved": "Auto-saved 🐾",
    "welcome": "Welcome to WhiskerNotes! 🐾",
    "error": "Oops! Something went wrong 😿",
}
