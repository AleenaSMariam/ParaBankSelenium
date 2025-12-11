import configparser
import os


class ConfigReader:
    def __init__(self):
        self.config = configparser.ConfigParser()
        # Get the absolute path to config.ini
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, '..', 'config.ini')
        
        # If config.ini doesn't exist, create default values
        if not os.path.exists(config_path):
            self.set_defaults()
        else:
            self.config.read(config_path)
    
    def set_defaults(self):
        """Set default values if config.ini is missing"""
        self.config['application'] = {
            'base_url': 'https://parabank.parasoft.com/parabank',
            'timeout': '10'
        }
    
    def get_base_url(self):
        try:
            return self.config.get('application', 'base_url')
        except:
            return "https://parabank.parasoft.com/parabank"
    
    def get_timeout(self):
        try:
            return self.config.getint('application', 'timeout')
        except:
            return 10