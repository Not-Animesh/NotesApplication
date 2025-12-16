"""
WhiskerNotes - Theme Configuration
Defines color schemes and UI styling for light and dark modes
"""

import os


class Theme:
    """Central theme configuration for WhiskerNotes"""
    
    # Available accent colors
    ACCENT_COLORS = {
        "pink": "#F6B1C3",
        "mint": "#B8E6D5",
        "yellow": "#FFE5B4",
        "lavender": "#E6E6FA"
    }
    
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
        "tag_bg": "#FFE5EC",       # Tag background
        "pin_color": "#FFD700",    # Gold pin color
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
        "tag_bg": "#2A2A2A",       # Tag background
        "pin_color": "#FFD700",    # Gold pin color
    }
    
    # Current theme (default to light)
    current_theme = "light"
    current_accent = "pink"
    
    # Default categories with emojis
    CATEGORIES = ["Personal 🐱", "Study 📘", "Ideas 💡", "Work 💼", "Other 📝"]
    
    @classmethod
    def get_colors(cls):
        """Get current theme colors"""
        colors = cls.LIGHT.copy() if cls.current_theme == "light" else cls.DARK.copy()
        # Apply current accent color
        if cls.current_accent in cls.ACCENT_COLORS:
            colors["accent"] = cls.ACCENT_COLORS[cls.current_accent]
        return colors
    
    @classmethod
    def toggle_theme(cls):
        """Toggle between light and dark themes"""
        cls.current_theme = "dark" if cls.current_theme == "light" else "light"
        return cls.current_theme
    
    @classmethod
    def is_dark(cls):
        """Check if current theme is dark"""
        return cls.current_theme == "dark"
    
    @classmethod
    def set_accent(cls, accent: str):
        """Set the accent color"""
        if accent in cls.ACCENT_COLORS:
            cls.current_accent = accent
            return True
        return False
    
    @classmethod
    def get_asset_path(cls, asset_name: str) -> str:
        """Get the full path to an asset"""
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Determine asset directory
        if asset_name.startswith("bg_"):
            subdir = "backgrounds"
        elif asset_name.startswith("cat_"):
            subdir = "cats"
        else:
            subdir = "icons"
        
        path = os.path.join(base_path, "assets", subdir, asset_name)
        return path if os.path.exists(path) else None


# Cat-themed feedback messages
CAT_MESSAGES = {
    "note_saved": "Meow! Your note is safe 🐾",
    "note_deleted": "Note deleted... your cat is sad 😿",
    "note_created": "Purr! New note created 🐱",
    "no_notes": "No notes yet... your cat is waiting 🐱",
    "auto_saved": "Meow! Auto-saved 🐾",
    "welcome": "Welcome to WhiskerNotes! 🐾",
    "error": "Oops! Something went wrong 😿",
    "note_pinned": "Note pinned to top! 📌🐾",
    "note_unpinned": "Note unpinned 🐾",
    "hooman_reminder": "Hooman, don't forget me! 🐱",
}

# Extended cat messages for random selection
RANDOM_CAT_MESSAGES = [
    "Meow! Note saved 🐾",
    "Purr... Everything is safe 🐱",
    "Hooman, don't forget me! 🐱",
    "Your note is purr-fect! 🐾",
    "Meow meow! Saved successfully 🐱",
]
