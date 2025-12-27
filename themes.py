"""
WhiskerNotes - Theme Configuration
Defines color schemes and UI styling for light and dark modes
Enhanced with modern design tokens
"""

import os


class Theme:
    """Central theme configuration for WhiskerNotes"""
    
    # Available accent colors with gradients
    ACCENT_COLORS = {
        "pink": {
            "primary": "#F6B1C3",
            "light": "#FFE5EC",
            "dark": "#E89BB5",
            "gradient": ("#FFE5EC", "#F6B1C3")
        },
        "mint": {
            "primary": "#B8E6D5",
            "light": "#E0F5ED",
            "dark": "#9DD9C4",
            "gradient": ("#E0F5ED", "#B8E6D5")
        },
        "yellow": {
            "primary": "#FFE5B4",
            "light": "#FFF4E0",
            "dark": "#FFD99A",
            "gradient": ("#FFF4E0", "#FFE5B4")
        },
        "lavender": {
            "primary": "#E6E6FA",
            "light": "#F0F0FF",
            "dark": "#D4D4F0",
            "gradient": ("#F0F0FF", "#E6E6FA")
        }
    }
    
    # Light Theme Colors - Blended with lavender gradient background
    LIGHT = {
        "bg": "#F5F0FF",           # Light lavender blend (allows background to show)
        "bg_secondary": "#F0EBFF",  # Secondary background blend
        "fg": "#1A1A1A",           # Rich dark text
        "fg_secondary": "#4A4A4A",  # Secondary text
        "accent": "#F6B1C3",       # Pink accent
        "accent_light": "#FFE5EC", # Light accent
        "accent_dark": "#E89BB5",  # Dark accent
        "card_bg": "#FFFFFF",      # Pure white card (for readability)
        "card_hover": "#FFF8FF",   # Light lavender hover
        "card_shadow": "#E8E0D5",  # Subtle shadow
        "button_bg": "#F6B1C3",    # Pink button
        "button_hover": "#E89BB5", # Button hover
        "button_fg": "#1A1A1A",    # Button text
        "border": "#E0D5E8",       # Soft lavender border
        "border_light": "#F0EBF5", # Light lavender border
        "scrollbar": "#F6B1C3",    # Pink scrollbar
        "tag_bg": "#FFE5EC",       # Tag background
        "tag_fg": "#8B4A5C",       # Tag text
        "pin_color": "#FFB800",    # Vibrant gold
        "success": "#4CAF50",      # Success green
        "error": "#F44336",        # Error red
        "warning": "#FF9800",      # Warning orange
        "info": "#2196F3",         # Info blue
    }
    
    # Current accent
    current_accent = "pink"
    
    # Default categories with emojis
    CATEGORIES = ["Personal 🐱", "Study 📘", "Ideas 💡", "Work 💼", "Other 📝"]
    
    @classmethod
    def get_colors(cls):
        """Get theme colors with accent color applied"""
        colors = cls.LIGHT.copy()
        # Apply current accent color
        if cls.current_accent in cls.ACCENT_COLORS:
            accent = cls.ACCENT_COLORS[cls.current_accent]
            colors["accent"] = accent["primary"]
            colors["accent_light"] = accent["light"]
            colors["accent_dark"] = accent["dark"]
        return colors
    
    @classmethod
    def get_accent_gradient(cls):
        """Get gradient colors for current accent"""
        if cls.current_accent in cls.ACCENT_COLORS:
            return cls.ACCENT_COLORS[cls.current_accent]["gradient"]
        return ("#F6B1C3", "#F6B1C3")
    
    @classmethod
    def get_spacing(cls):
        """Get spacing tokens"""
        return {
            "xs": 4,
            "sm": 8,
            "md": 16,
            "lg": 24,
            "xl": 32,
            "xxl": 48
        }
    
    @classmethod
    def get_radius(cls):
        """Get border radius tokens"""
        return {
            "sm": 8,
            "md": 12,
            "lg": 16,
            "xl": 20,
            "full": 999
        }
    
    @classmethod
    def get_shadows(cls):
        """Get shadow definitions"""
        return {
            "sm": ("#00000020", 2),
            "md": ("#00000030", 4),
            "lg": ("#00000040", 8),
        }
    
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
    
    @classmethod
    def get_background_image(cls):
        """Get background image - always uses lavender gradient"""
        bg_path = cls.get_asset_path("bg_lavender_gradient.jpg")
        if bg_path and os.path.exists(bg_path):
            return bg_path
        return None


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
