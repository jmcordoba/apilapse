import json
from dataclasses import dataclass

@dataclass
class Config:
    """
    Class responsible for logging in a user and returning an access token.
    """
    def get_config(self):
        """
        Read the configuration parameters from a JSON file and set them in a dictionary.
        """
        # Set the configuration file path
        JSON_CONFIG = 'conf/dev.json'
        
        try:
            with open(JSON_CONFIG, 'r') as file:
                config = json.load(file)
            
            # Extract parameters and set them in a dictionary
            config = {
                'host': config.get('host'),
                'port': config.get('port'),
                'debug': bool(config.get('debug', False)),
                'database_name': config.get('database_name'),
                'email': config.get('email'),
                'email_password': config.get('email_password'),
                'secret_key': config.get('secret_key')
            }
            
            return config

        except FileNotFoundError:
            print(f"Configuration file not found: {JSON_CONFIG}")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the file: {JSON_CONFIG}")
            return None