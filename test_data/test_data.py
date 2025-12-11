import random
import string
import time


class TestData:
    
    @staticmethod
    def get_timestamp():
        """Get current timestamp for uniqueness"""
        return str(int(time.time()))
    
    @staticmethod
    def generate_random_digits(length=9):
        """Generate random digits of given length"""
        digits = string.digits
        return ''.join(random.choice(digits) for _ in range(length))
    
    @staticmethod
    def get_valid_user_data():
        timestamp = TestData.get_timestamp()[-6:]
        random_id = ''.join(random.choices(string.ascii_lowercase, k=4))
        
        return {
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'zip_code': f"{random.randint(10000, 99999)}",
            'phone': f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            'ssn': TestData.generate_random_digits(9),
            'username': f'user_{random_id}{timestamp}',
            'password': 'password123'
        }
    
    # MAKE SURE THIS METHOD EXISTS
    @staticmethod
    def get_valid_bill_pay_data():
        """Get valid bill payment data"""
        print(f"[TestData] Generating bill pay data at {time.time()}")
        return {
            'payee_name': 'Test Payee',
            'payee_address': '123 Payment St',
            'payee_city': 'Payment City',
            'payee_state': 'CA',
            'payee_zip': f"{random.randint(10000, 99999)}",
            'payee_phone': f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            'payee_account': TestData.generate_random_digits(9),
            'verify_account': '',  # Will be set in test
            'amount': '100.50'
        }