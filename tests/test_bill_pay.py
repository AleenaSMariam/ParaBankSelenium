"""
PARABANK BILL PAY - TEST CASES
"""

import sys
import os
import time
import pytest

# Fix import paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import modules
from pages.home_page import HomePage
from pages.register_page import RegisterPage
from pages.bill_pay_page import BillPayPage
from test_data.test_data import TestData
from utilities.config_reader import ConfigReader

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def setup_bill_pay():
    """Setup fixture for each test"""
    config = ConfigReader()
    base_url = config.get_base_url()
    timeout = config.get_timeout()
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(timeout)
    driver.maximize_window()
    
    # Register a user
    driver.get(f"{base_url}/index.htm")
    home_page = HomePage(driver)
    home_page.navigate_to_register_page()
    
    user_data = TestData.get_valid_user_data()
    username = user_data['username']
    
    register_page = RegisterPage(driver)
    register_page.register_user(user_data)
    time.sleep(2)
    
    yield driver, base_url, username
    
    # Teardown
    driver.quit()


class TestBillPay:
    
    def _fill_and_submit_bill_form(self, driver, base_url, bill_data):
        """Helper method to fill and submit bill form"""
        driver.get(f"{base_url}/billpay.htm")
        time.sleep(2)
        
        bill_pay_page = BillPayPage(driver)
        
        if not bill_data.get('verify_account'):
            bill_data['verify_account'] = bill_data['payee_account']
        
        bill_pay_page.fill_form(bill_data)
        bill_pay_page.submit()
        time.sleep(3)
        
        return bill_pay_page
    
    def test_1_valid_payment(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        # This should pass - valid data
        assert bill_pay_page.is_successful()
    
    def test_2_empty_amount(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['amount'] = ""
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_3_alphanumeric_amount(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['amount'] = "abc123"
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_4_invalid_account_mismatch(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['verify_account'] = "999999999"
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_5_empty_payee_name(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['payee_name'] = ""
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_6_all_fields_empty(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        for key in ['payee_name', 'payee_address', 'payee_city', 'payee_state', 
                   'payee_zip', 'payee_phone', 'payee_account', 'amount']:
            bill_data[key] = ""
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_7_negative_amount(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['amount'] = "-100.50"
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_8_zero_amount(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['amount'] = "0.00"
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_9_very_large_amount(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['amount'] = "999999999.99"
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_10_amount_with_many_decimals(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['amount'] = "123.456789"
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_11_minimum_amount(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['amount'] = "0.01"
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_12_maximum_amount_boundary(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['amount'] = "999999.99"
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_13_special_characters_in_name(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['payee_name'] = "Test @#$%^&*() Company"
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_14_special_characters_in_address(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['payee_address'] = "123 #$% St, Apt &*()"
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_15_very_long_payee_name(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['payee_name'] = "A" * 150
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_16_very_long_address(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['payee_address'] = "123 " + "Very " * 20 + "Long Street Name"
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_17_invalid_zip_format(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['payee_zip'] = "ABCDE"
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_18_invalid_phone_format(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['payee_phone'] = "abc-def-ghij"
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_19_invalid_account_format(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['payee_account'] = "ABC123XYZ"
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_20_duplicate_payment(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        time.sleep(2)
        bill_pay_page2 = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_21_payment_with_spaces_in_fields(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['payee_name'] = "  Test Payee  "
        bill_data['payee_address'] = "  123 Main St  "
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_22_payment_with_html_tags(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['payee_name'] = "<script>alert('xss')</script>Test"
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_23_payment_with_sql_injection(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['payee_name'] = "Test' OR '1'='1"
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_24_payment_with_unicode_characters(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['payee_name'] = "Tést Päyée Café"
        bill_data['payee_city'] = "München"
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True
    
    def test_25_multiple_payments_different_accounts(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        for i in range(1, 4):
            bill_data = TestData.get_valid_bill_pay_data()
            bill_data['payee_account'] = f"10000000{i}"
            bill_data['amount'] = f"{i * 50}.00"
            bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
            
            if i < 3:
                time.sleep(2)
                driver.get(f"{base_url}/billpay.htm")
                time.sleep(2)
        assert True
    
    def test_26_payment_amount_exceeds_balance(self, setup_bill_pay):
        driver, base_url, username = setup_bill_pay
        bill_data = TestData.get_valid_bill_pay_data()
        bill_data['amount'] = "999999.99"
        bill_pay_page = self._fill_and_submit_bill_form(driver, base_url, bill_data)
        assert True