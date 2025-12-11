"""
Base Test Class for all test cases
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utilities.config_reader import ConfigReader


class BaseTest:
    """Base class for all test cases with common setup/teardown"""
    
    def setup_method(self):
        """Setup before each test method"""
        # Initialize ConfigReader
        self.config = ConfigReader()
        self.base_url = self.config.get_base_url()
        self.timeout = self.config.get_timeout()
        
        # Setup driver
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.driver.implicitly_wait(self.timeout)
        self.driver.maximize_window()
        
        print(f"\nTest Setup: Using base URL: {self.base_url}")
    
    def teardown_method(self):
        """Teardown after each test method"""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
            print("Test Teardown: Browser closed")
    
    def get_full_url(self, endpoint=""):
        """Get full URL by appending endpoint to base URL"""
        if endpoint.startswith("/"):
            endpoint = endpoint[1:]
        return f"{self.base_url}/{endpoint}"