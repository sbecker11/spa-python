import os
from typing import Dict, Any
import yaml
import logging

class ApplicationSettings:
    """
    Centralized configuration management for the application
    """
    _instance = None
    _config: dict[str, Any] = {}

    def __new__(cls):
        """
        Singleton implementation to ensure only one config instance
        """
        if not cls._instance:
            cls._instance = super(ApplicationSettings, cls).__new__(cls)
            cls._load_config()
        return cls._instance

    @classmethod
    def _load_config(cls):
        """
        Load configuration from multiple potential sources
        """
        # Potential config file locations
        config_paths = [
            'config/app_config.yaml',
            'app_config.yaml',
            os.path.expanduser('~/.user_management_app/config.yaml')
        ]

        # Default configuration
        cls._config = {
            'app_name': 'User Management App',
            'version': '1.0.0',
            'logging': {
                'level': 'INFO',
                'file': 'app.log'
            },
            'authentication': {
                'max_login_attempts': 5,
                'password_min_length': 8
            },
            'database': {
                'type': 'json',
                'path': 'accounts.json'
            }
        }

        # Try to load from config files
        for path in config_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as config_file:
                        file_config = yaml.safe_load(config_file)
                        # Deep merge configurations
                        cls._deep_merge(cls._config, file_config)
                    break
                except (yaml.YAMLError, OSError) as e:
                    logging.warning(f"Error loading config from {path}: {e}")

        # Configure logging based on config
        cls._configure_logging()

    @classmethod
    def _deep_merge(cls, base: Dict, update: Dict):
        """
        Recursively merge configuration dictionaries
        """
        for key, value in update.items():
            if isinstance(value, dict):
                base[key] = cls._deep_merge(base.get(key, {}), value)
            else:
                base[key] = value
        return base

    @classmethod
    def _configure_logging(cls):
        """
        Configure application-wide logging
        """
        log_config = cls._config.get('logging', {})
        log_level = getattr(logging, log_config.get('level', 'INFO').upper())
        log_file = log_config.get('file', 'app.log')

        # Configure logging
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename=log_file,
            filemode='a'
        )

    @classmethod
    def get(cls, key: str, default=None):
        """
        Retrieve a configuration value
        
        Args:
            key (str): Dot-separated configuration key
            default: Default value if key not found
        
        Returns:
            Configuration value or default
        """
        try:
            value = cls._config
            for k in key.split('.'):
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    @classmethod
    def reload(cls):
        """
        Reload configuration from files
        """
        cls._load_config()

# Example usage
def main():
    # Get singleton instance
    config = ApplicationSettings()
    
    # Retrieve configuration values
    print(f"App Name: {config.get('app_name')}")
    print(f"Max Login Attempts: {config.get('authentication.max_login_attempts')}")

if __name__ == '__main__':
    main()