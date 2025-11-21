# ================================================================================
# Author: Vivek Patel
# Title: AI Engineer | Computer Vision Specialist
# Website: https://vivekapatel.com
# Email: contact@vivekapatel.com
# Upwork: https://www.upwork.com/freelancers/vivekpatel99?mp_source=share
# Created: 2025-11-21
# ================================================================================
"""
Configuration loader for signature tool.

Handles loading and merging of global and local configuration files.
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional


class ConfigError(Exception):
    """Raised when configuration is invalid or missing."""
    pass


class Config:
    """Configuration manager for signature tool."""

    REQUIRED_FIELDS = ["author", "email"]
    OPTIONAL_FIELDS = ["title", "website", "upwork"]

    def __init__(self, global_path: Optional[Path] = None, local_path: Optional[Path] = None):
        """
        Initialize configuration.

        Args:
            global_path: Path to global config (default: ~/.signature.json)
            local_path: Path to local config (default: ./.signature.json)
        """
        # Convert to Path objects if strings provided
        self.global_path = Path(global_path) if global_path else Path.home() / ".signature.json"
        self.local_path = Path(local_path) if local_path else Path.cwd() / ".signature.json"
        self.data = self._load_config()
        self._validate()

    def _load_config(self) -> Dict:
        """Load and merge global and local configurations."""
        config = {}

        # Load global config
        if self.global_path.exists():
            try:
                with open(self.global_path, 'r') as f:
                    config = json.load(f)
            except json.JSONDecodeError as e:
                raise ConfigError(f"Invalid JSON in {self.global_path}: {e}")
        else:
            raise ConfigError(
                f"Global configuration not found at {self.global_path}\n"
                f"Please run 'install.sh' or create the config file manually."
            )

        # Load and merge local config if it exists
        if self.local_path.exists():
            try:
                with open(self.local_path, 'r') as f:
                    local_config = json.load(f)
                    # Merge: local overrides global
                    config.update(local_config)
            except json.JSONDecodeError as e:
                raise ConfigError(f"Invalid JSON in {self.local_path}: {e}")

        return config

    def _validate(self):
        """Validate that required fields are present."""
        missing = [field for field in self.REQUIRED_FIELDS if field not in self.data]
        if missing:
            raise ConfigError(
                f"Missing required fields in configuration: {', '.join(missing)}\n"
                f"Please update {self.global_path}"
            )

    def get(self, key: str, default=None):
        """Get configuration value."""
        return self.data.get(key, default)

    def __getitem__(self, key: str):
        """Get configuration value using dict syntax."""
        return self.data[key]

    def __contains__(self, key: str) -> bool:
        """Check if key exists in configuration."""
        return key in self.data

    def to_dict(self) -> Dict:
        """Return configuration as dictionary."""
        return self.data.copy()


def load_config(global_path: Optional[Path] = None, local_path: Optional[Path] = None) -> Config:
    """
    Load configuration from global and local files.

    Args:
        global_path: Path to global config (default: ~/.signature.json)
        local_path: Path to local config (default: ./.signature.json)

    Returns:
        Config object with merged configuration

    Raises:
        ConfigError: If config is missing or invalid
    """
    return Config(global_path, local_path)
