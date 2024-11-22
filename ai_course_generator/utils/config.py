"""Configuration management utilities."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """Load configuration from YAML file and environment variables."""
    config_path = Path("config.yaml")
    if not config_path.exists():
        raise FileNotFoundError("config.yaml not found in current directory")
    
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    
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
