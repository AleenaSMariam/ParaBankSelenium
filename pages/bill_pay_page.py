from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class BillPayPage:
    """Page Object for Bill Pay"""
    
    # Complete locators
    PAYEE_NAME = (By.NAME, "payee.name")
    PAYEE_ADDRESS = (By.NAME, "payee.address.street")
    PAYEE_CITY = (By.NAME, "payee.address.city")
    PAYEE_STATE = (By.NAME, "payee.address.state")
    PAYEE_ZIP_CODE = (By.NAME, "payee.address.zipCode")
    PAYEE_PHONE = (By.NAME, "payee.phoneNumber")
    PAYEE_ACCOUNT = (By.NAME, "payee.accountNumber")
    VERIFY_ACCOUNT = (By.NAME, "verifyAccount")
    AMOUNT = (By.NAME, "amount")
    FROM_ACCOUNT = (By.NAME, "fromAccountId")
    SEND_BUTTON = (By.XPATH, "//input[@value='Send Payment']")
    
    def __init__(self, driver):
        self.driver = driver
    
    # METHOD 1: fill_form (new name)
    def fill_form(self, bill_data):
        """Fill form with provided data"""
        # Fill all fields
        self.driver.find_element(*self.PAYEE_NAME).send_keys(bill_data.get('payee_name', ''))
        self.driver.find_element(*self.PAYEE_ADDRESS).send_keys(bill_data.get('payee_address', ''))
        self.driver.find_element(*self.PAYEE_CITY).send_keys(bill_data.get('payee_city', ''))
        self.driver.find_element(*self.PAYEE_STATE).send_keys(bill_data.get('payee_state', ''))
        self.driver.find_element(*self.PAYEE_ZIP_CODE).send_keys(bill_data.get('payee_zip', ''))
        self.driver.find_element(*self.PAYEE_PHONE).send_keys(bill_data.get('payee_phone', ''))
        self.driver.find_element(*self.PAYEE_ACCOUNT).send_keys(bill_data.get('payee_account', ''))
        
        # Verify account (use same as payee_account if not provided)
        verify_account = bill_data.get('verify_account', bill_data.get('payee_account', ''))
        self.driver.find_element(*self.VERIFY_ACCOUNT).send_keys(verify_account)
        
        self.driver.find_element(*self.AMOUNT).send_keys(bill_data.get('amount', ''))
        
        # Select from account
        dropdown = Select(self.driver.find_element(*self.FROM_ACCOUNT))
        if dropdown.options:
            dropdown.select_by_index(0)
        
        return self
    
    # METHOD 2: fill_form_with_data (for compatibility)
    def fill_form_with_data(self, bill_data=None):
        """Legacy method name"""
        if bill_data is None:
            bill_data = self.get_default_data()
        return self.fill_form(bill_data)
    
    # METHOD 3: fill_valid_data (shortcut)
    def fill_valid_data(self):
        """Fill form with valid test data"""
        return self.fill_form_with_data()
    
    def get_default_data(self):
        """Get default test data"""
        return {
            'payee_name': 'Test Payee',
            'payee_address': '123 St',
            'payee_city': 'City',
            'payee_state': 'ST',
            'payee_zip': '12345',
            'payee_phone': '555-1234',
            'payee_account': '123456789',
            'amount': '5.50'
        }
    
    def submit(self):
        """Submit the form"""
        self.driver.find_element(*self.SEND_BUTTON).click()
        return self
    
    def is_successful(self):
        """Check if payment was successful"""
        return "Bill Payment Complete" in self.driver.page_source
    
    def has_errors(self):
        """Check if there are errors"""
        page_text = self.driver.page_source.lower()
        return "error" in page_text or "required" in page_text
    
    def clear_amount(self):
        """Clear the amount field"""
        self.driver.find_element(*self.AMOUNT).clear()
        return self
    
    def set_amount(self, amount):
        """Set amount field to specific value"""
        self.clear_amount()
        self.driver.find_element(*self.AMOUNT).send_keys(amount)
        return self
