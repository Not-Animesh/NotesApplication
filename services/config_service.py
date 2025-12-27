"""
WhiskerNotes - Configuration Service
Manages application configuration and settings
"""

import json
import os
from typing import Dict, Any, Optional


class ConfigService:
    """Service for managing application configuration"""
    
    CONFIG_FILE = "config.json"
    
    @classmethod
    def get_config_path(cls) -> str:
        """Get the path to the config file"""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, cls.CONFIG_FILE)
    
    @classmethod
    def load_config(cls) -> Dict[str, Any]:
        """Load configuration from file or return defaults"""
        config_path = cls.get_config_path()
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Return default configuration
        return {
            "theme": "light",
            "accent_color": "pink",
            "window_width": 900,
            "window_height": 700,
            "auto_save_delay": 2000,
            "font_size": 14
        }
    
    @classmethod
    def save_config(cls, config: Dict[str, Any]) -> bool:
        """Save configuration to file"""
        try:
            config_path = cls.get_config_path()
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            return True
        except IOError:
            return False
    
    @classmethod
    def get_setting(cls, key: str, default: Any = None) -> Any:
        """Get a specific setting value"""
        config = cls.load_config()
        return config.get(key, default)
    
    @classmethod
    def set_setting(cls, key: str, value: Any) -> bool:
        """Set a specific setting value"""
        config = cls.load_config()
        config[key] = value
        return cls.save_config(config)

