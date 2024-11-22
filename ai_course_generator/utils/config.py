"""Configuration management utilities."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any
import re

def _replace_env_vars(config: Dict[str, Any]) -> Dict[str, Any]:
    """Replace environment variable placeholders in config values."""
    def _replace_value(value):
        if isinstance(value, str):
            # Find all ${VAR} patterns
            env_vars = re.findall(r'\${([^}]+)}', value)
            for var in env_vars:
                env_value = os.getenv(var)
                if env_value is None:
                    raise ValueError(f"Environment variable {var} not set")
                value = value.replace(f"${{{var}}}", env_value)
            return value
        elif isinstance(value, dict):
            return {k: _replace_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [_replace_value(item) for item in value]
        return value

    return _replace_value(config)

def load_config() -> Dict[str, Any]:
    """Load configuration from YAML file and environment variables."""
    config_path = Path("config.yaml")
    if not config_path.exists():
        raise FileNotFoundError("config.yaml not found in current directory")
    
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    
    # Replace environment variables in config
    config = _replace_env_vars(config)
    
    # Override with environment variables if they exist
    if os.getenv("GROQ_API_KEY"):
        config["groq"]["api_key"] = os.getenv("GROQ_API_KEY")
    if os.getenv("RESEND_API_KEY"):
        config["email"]["api_key"] = os.getenv("RESEND_API_KEY")
    if os.getenv("SENDER_EMAIL"):
        config["email"]["from_email"] = os.getenv("SENDER_EMAIL")
    if os.getenv("RECIPIENT_EMAIL"):
        config["email"]["recipient_email"] = os.getenv("RECIPIENT_EMAIL")
    
    return config

def save_master_prompt(prompt: str) -> None:
    """Save the master prompt to config.yaml."""
    config_path = Path("config.yaml")
    if not config_path.exists():
        raise FileNotFoundError("config.yaml not found in current directory")
    
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    
    config["content"]["current_master_prompt"] = prompt
    
    with open(config_path, "w") as file:
        yaml.dump(config, file, default_flow_style=False, sort_keys=False)
