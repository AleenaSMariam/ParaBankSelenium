from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class RegisterPage:
    FIRST_NAME_FIELD = (By.ID, "customer.firstName")
    LAST_NAME_FIELD = (By.ID, "customer.lastName")
    ADDRESS_FIELD = (By.ID, "customer.address.street")
    CITY_FIELD = (By.ID, "customer.address.city")
    STATE_FIELD = (By.ID, "customer.address.state")
    ZIP_CODE_FIELD = (By.ID, "customer.address.zipCode")
    PHONE_FIELD = (By.ID, "customer.phoneNumber")
    SSN_FIELD = (By.ID, "customer.ssn")
    USERNAME_FIELD = (By.ID, "customer.username")
    PASSWORD_FIELD = (By.ID, "customer.password")
    CONFIRM_PASSWORD_FIELD = (By.ID, "repeatedPassword")
    REGISTER_BUTTON = (By.XPATH, "//input[@value='Register']")
    SUCCESS_MESSAGE = (By.XPATH, "//h1[contains(text(), 'Welcome')]")
    ERROR_MESSAGE = (By.CLASS_NAME, "error")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def click(self, by_locator):
        self.wait.until(EC.element_to_be_clickable(by_locator)).click()
    
    def send_keys(self, by_locator, text):
        element = self.wait.until(EC.visibility_of_element_located(by_locator))
        element.clear()  # Clear field first
        element.send_keys(text)
    
    def get_element_text(self, by_locator):
        element = self.wait.until(EC.visibility_of_element_located(by_locator))
        return element.text
    
    def is_visible(self, by_locator):
        try:
            element = self.wait.until(EC.visibility_of_element_located(by_locator))
            return bool(element)
        except:
            return False
    
    def is_present(self, by_locator):
        """Check if element is present in DOM (not necessarily visible)"""
        try:
            elements = self.driver.find_elements(*by_locator)
            return len(elements) > 0
        except:
            return False
    
    def fill_field_with_delay(self, by_locator, text, delay=5):
        self.send_keys(by_locator, text)
        time.sleep(delay)
    
    def register_user(self, user_data, confirm_password=None):
        """Register a new user with provided data"""
        # If confirm_password is provided, use it. Otherwise use password from user_data
        confirm = confirm_password if confirm_password else user_data['password']
        
        self.send_keys(self.FIRST_NAME_FIELD, user_data['first_name'])
        self.send_keys(self.LAST_NAME_FIELD, user_data['last_name'])
        self.send_keys(self.ADDRESS_FIELD, user_data['address'])
        self.send_keys(self.CITY_FIELD, user_data['city'])
        self.send_keys(self.STATE_FIELD, user_data['state'])
        self.send_keys(self.ZIP_CODE_FIELD, user_data['zip_code'])
        self.send_keys(self.PHONE_FIELD, user_data['phone'])
        self.send_keys(self.SSN_FIELD, user_data['ssn'])
        self.send_keys(self.USERNAME_FIELD, user_data['username'])
        self.send_keys(self.PASSWORD_FIELD, user_data['password'])
        self.send_keys(self.CONFIRM_PASSWORD_FIELD, confirm)
        self.click(self.REGISTER_BUTTON)
    
    def get_success_message(self):
        """Get success message if registration succeeded"""
        try:
            # Try multiple success message locators
            success_locators = [
                (By.XPATH, "//h1[contains(text(), 'Welcome')]"),
                (By.XPATH, "//h1[contains(text(), 'Account')]"),
                (By.XPATH, "//p[contains(text(), 'created')]"),
                (By.XPATH, "//*[contains(text(), 'success')]"),
                (By.ID, "rightPanel")
            ]
            
            for locator in success_locators:
                try:
                    element = self.driver.find_element(*locator)
                    if element.is_displayed():
                        return element.text
                except:
                    continue
                    
            return ""
        except Exception as e:
            print(f"Error getting success message: {e}")
            return ""
    
    def is_registration_successful(self):
        """Check if registration was successful"""
        try:
            # Check URL first
            current_url = self.driver.current_url.lower()
            if "overview" in current_url or "account" in current_url:
                return True
            
            # Check for success indicators
            success_indicators = [
                "welcome",
                "account",
                "created",
                "success",
                "logged in"
            ]
            
            body_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            if any(indicator in body_text for indicator in success_indicators):
                return True
            
            # Check specific success elements
            success_elements = [
                (By.XPATH, "//h1[contains(text(), 'Welcome')]"),
                (By.XPATH, "//h1[contains(text(), 'Account')]"),
                (By.XPATH, "//b[contains(text(), 'Welcome')]")
            ]
            
            for locator in success_elements:
                if self.is_present(locator):
                    return True
            
            return False
            
        except Exception as e:
            print(f"Error checking registration success: {e}")
            return False
    
    def get_error_messages(self):
        """Get all error messages on the page"""
        errors = []
        
        try:
            # Try multiple error element selectors
            error_selectors = [
                (By.CLASS_NAME, "error"),  # Original
                (By.CSS_SELECTOR, ".error"),  # CSS version
                (By.XPATH, "//*[contains(@class, 'error')]"),  # Any element with error class
                (By.XPATH, "//span[@class='error']"),  # Span errors
                (By.XPATH, "//td[@class='error']"),  # TD errors
                (By.XPATH, "//font[@color='red']"),  # Red text (common for errors)
                (By.XPATH, "//*[contains(text(), 'is required')]"),  # Required field errors
                (By.XPATH, "//*[contains(text(), 'did not match')]"),  # Password mismatch
                (By.XPATH, "//*[contains(text(), 'already exists')]")  # Duplicate username
            ]
            
            for selector in error_selectors:
                try:
                    elements = self.driver.find_elements(*selector)
                    for element in elements:
                        if element.is_displayed() and element.text.strip():
                            text = element.text.strip()
                            if text not in errors:
                                errors.append(text)
                except:
                    continue
            
            # Also check for inline errors next to form fields
            form_errors = self.driver.find_elements(By.XPATH, 
                "//table[@class='form2']//td[contains(@class, 'error') or font[@color='red']]")
            for error in form_errors:
                if error.text.strip() and error.text.strip() not in errors:
                    errors.append(error.text.strip())
            
            # Check for error messages in the right panel
            try:
                right_panel = self.driver.find_element(By.ID, "rightPanel")
                if right_panel and "error" in right_panel.text.lower():
                    # Extract error sentences
                    lines = right_panel.text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and ("error" in line.lower() or "please" in line.lower() or "required" in line.lower()):
                            if line not in errors:
                                errors.append(line)
            except:
                pass
                
        except Exception as e:
            print(f"Error in get_error_messages: {e}")
        
        return errors
    
    def is_on_register_page(self):
        """Check if still on registration page"""
        current_url = self.driver.current_url.lower()
        return "register" in current_url
    
    def get_page_text(self):
        """Get all text from the page"""
        try:
            return self.driver.find_element(By.TAG_NAME, "body").text
        except:
            return ""