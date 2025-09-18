"""
Configuration Settings Module
Handles loading and managing application configuration.
"""

import os
import json
import yaml
import logging
from typing import Dict, Any
from pathlib import Path


def load_config() -> Dict[str, Any]:
    """Load configuration from various sources."""
    config = {}
    
    # Load from config files
    config_dir = Path(__file__).parent
    project_root = config_dir.parent.parent
    
    # Load default configuration
    default_config_path = config_dir / "default_config.yaml"
    if default_config_path.exists():
        config.update(_load_yaml_config(default_config_path))
    
    # Load user configuration (overrides defaults)
    user_config_path = project_root / "config.yaml"
    if user_config_path.exists():
        config.update(_load_yaml_config(user_config_path))
    
    # Load environment-specific configuration
    env = os.getenv('ENVIRONMENT', 'development')
    env_config_path = config_dir / f"{env}_config.yaml"
    if env_config_path.exists():
        config.update(_load_yaml_config(env_config_path))
    
    # Override with environment variables
    config.update(_load_env_config())
    
    # Validate configuration
    _validate_config(config)
    
    return config


def _load_yaml_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file) or {}
    except Exception as e:
        logging.warning(f"Failed to load config from {config_path}: {e}")
        return {}


def _load_json_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        logging.warning(f"Failed to load config from {config_path}: {e}")
        return {}


def _load_env_config() -> Dict[str, Any]:
    """Load configuration from environment variables."""
    config = {}
    
    # WhatsApp configuration
    whatsapp_config = {}
    if os.getenv('WHATSAPP_CLIENT_TYPE'):
        whatsapp_config['client_type'] = os.getenv('WHATSAPP_CLIENT_TYPE')
    if os.getenv('WHATSAPP_SESSION_PATH'):
        whatsapp_config['session_path'] = os.getenv('WHATSAPP_SESSION_PATH')
    if os.getenv('WHATSAPP_BUSINESS_API_TOKEN'):
        whatsapp_config['business_api_token'] = os.getenv('WHATSAPP_BUSINESS_API_TOKEN')
    if os.getenv('WHATSAPP_PHONE_NUMBER_ID'):
        whatsapp_config['phone_number_id'] = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    
    if whatsapp_config:
        config['whatsapp'] = whatsapp_config
    
    # AI configuration
    ai_config = {}
    if os.getenv('AI_PROVIDER'):
        ai_config['provider'] = os.getenv('AI_PROVIDER')
    if os.getenv('AI_MODEL'):
        ai_config['model'] = os.getenv('AI_MODEL')
    if os.getenv('OPENAI_API_KEY'):
        ai_config['api_key'] = os.getenv('OPENAI_API_KEY')
    if os.getenv('AI_MAX_TOKENS'):
        ai_config['max_tokens'] = int(os.getenv('AI_MAX_TOKENS'))
    if os.getenv('AI_TEMPERATURE'):
        ai_config['temperature'] = float(os.getenv('AI_TEMPERATURE'))
    if os.getenv('AI_SYSTEM_PROMPT'):
        ai_config['system_prompt'] = os.getenv('AI_SYSTEM_PROMPT')
    
    if ai_config:
        config['ai'] = ai_config
    
    # Messaging configuration
    messaging_config = {}
    if os.getenv('RESPOND_TO_GROUPS'):
        messaging_config['respond_to_groups'] = os.getenv('RESPOND_TO_GROUPS').lower() == 'true'
    if os.getenv('REQUIRE_MENTION_IN_GROUPS'):
        messaging_config['require_mention_in_groups'] = os.getenv('REQUIRE_MENTION_IN_GROUPS').lower() == 'true'
    if os.getenv('RATE_LIMIT_ENABLED'):
        messaging_config['rate_limit_enabled'] = os.getenv('RATE_LIMIT_ENABLED').lower() == 'true'
    if os.getenv('MAX_MESSAGES_PER_HOUR'):
        messaging_config['max_messages_per_hour'] = int(os.getenv('MAX_MESSAGES_PER_HOUR'))
    if os.getenv('BOT_NAME'):
        messaging_config['bot_name'] = os.getenv('BOT_NAME')
    
    # Parse contact lists from environment
    if os.getenv('ALLOWED_CONTACTS'):
        messaging_config['allowed_contacts'] = os.getenv('ALLOWED_CONTACTS').split(',')
    if os.getenv('BLOCKED_CONTACTS'):
        messaging_config['blocked_contacts'] = os.getenv('BLOCKED_CONTACTS').split(',')
    
    if messaging_config:
        config['messaging'] = messaging_config
    
    # General configuration
    if os.getenv('LOG_LEVEL'):
        config['log_level'] = os.getenv('LOG_LEVEL')
    if os.getenv('ENVIRONMENT'):
        config['environment'] = os.getenv('ENVIRONMENT')
    
    return config


def _validate_config(config: Dict[str, Any]):
    """Validate configuration and set defaults."""
    # Set default values
    if 'log_level' not in config:
        config['log_level'] = 'INFO'
    
    if 'environment' not in config:
        config['environment'] = 'development'
    
    # WhatsApp defaults
    if 'whatsapp' not in config:
        config['whatsapp'] = {}
    
    whatsapp_config = config['whatsapp']
    if 'client_type' not in whatsapp_config:
        whatsapp_config['client_type'] = 'web'
    
    # AI defaults
    if 'ai' not in config:
        config['ai'] = {}
    
    ai_config = config['ai']
    if 'provider' not in ai_config:
        ai_config['provider'] = 'openai'
    if 'model' not in ai_config:
        ai_config['model'] = 'gpt-3.5-turbo'
    if 'max_tokens' not in ai_config:
        ai_config['max_tokens'] = 1000
    if 'temperature' not in ai_config:
        ai_config['temperature'] = 0.7
    
    # Messaging defaults
    if 'messaging' not in config:
        config['messaging'] = {}
    
    messaging_config = config['messaging']
    if 'respond_to_groups' not in messaging_config:
        messaging_config['respond_to_groups'] = False
    if 'require_mention_in_groups' not in messaging_config:
        messaging_config['require_mention_in_groups'] = True
    if 'rate_limit_enabled' not in messaging_config:
        messaging_config['rate_limit_enabled'] = True
    if 'max_messages_per_hour' not in messaging_config:
        messaging_config['max_messages_per_hour'] = 30
    if 'bot_name' not in messaging_config:
        messaging_config['bot_name'] = 'AI Assistant'
    
    # Initialize empty contact lists if not provided
    if 'allowed_contacts' not in messaging_config:
        messaging_config['allowed_contacts'] = []
    if 'blocked_contacts' not in messaging_config:
        messaging_config['blocked_contacts'] = []


def get_config_template() -> Dict[str, Any]:
    """Get a template configuration for reference."""
    return {
        "log_level": "INFO",
        "environment": "development",
        
        "whatsapp": {
            "client_type": "web",  # Options: 'web', 'business_api', 'unofficial'
            "session_path": "./session",
            "business_api_token": "your_business_api_token_here",
            "phone_number_id": "your_phone_number_id_here"
        },
        
        "ai": {
            "provider": "openai",  # Options: 'openai', 'anthropic', 'local'
            "model": "gpt-3.5-turbo",
            "api_key": "your_openai_api_key_here",
            "max_tokens": 1000,
            "temperature": 0.7,
            "system_prompt": "You are a helpful AI assistant responding to WhatsApp messages. Be concise, friendly, and helpful."
        },
        
        "messaging": {
            "respond_to_groups": False,
            "require_mention_in_groups": True,
            "rate_limit_enabled": True,
            "max_messages_per_hour": 30,
            "bot_name": "AI Assistant",
            "allowed_contacts": [],  # Empty means all contacts allowed
            "blocked_contacts": [],
            "send_error_notifications": False
        }
    }


def save_config_template(config_path: str = "config.yaml"):
    """Save a template configuration file."""
    template = get_config_template()
    
    try:
        with open(config_path, 'w', encoding='utf-8') as file:
            yaml.dump(template, file, default_flow_style=False, indent=2)
        print(f"Configuration template saved to {config_path}")
    except Exception as e:
        print(f"Error saving configuration template: {e}")


if __name__ == "__main__":
    # Generate config template when run directly
    save_config_template()