from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utilities.config_reader import ConfigReader
except ImportError:
    # Fallback if config_reader fails
    class ConfigReader:
        def get_base_url(self):
            return "https://parabank.parasoft.com/parabank"
        def get_timeout(self):
            return 10


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.config = ConfigReader()
        self.wait = WebDriverWait(driver, self.config.get_timeout())
    
    def click(self, by_locator):
        self.wait.until(EC.element_to_be_clickable(by_locator)).click()
    
    def send_keys(self, by_locator, text):
        self.wait.until(EC.visibility_of_element_located(by_locator)).send_keys(text)
    
    def get_element_text(self, by_locator):
        element = self.wait.until(EC.visibility_of_element_located(by_locator))
        return element.text
    
    def is_visible(self, by_locator):
        element = self.wait.until(EC.visibility_of_element_located(by_locator))
        return bool(element)