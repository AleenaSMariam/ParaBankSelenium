import pytest
import allure
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", 
                     help="Type of browser: chrome or firefox")


@pytest.fixture(scope="class")
def setup(request):
    """Main setup fixture with Allure support"""
    browser = request.config.getoption("--browser")
    
    if browser == "chrome":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    elif browser == "firefox":
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    driver.implicitly_wait(10)
    driver.maximize_window()
    request.cls.driver = driver
    
    yield driver
    
    # Take screenshot on test failure
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        take_allure_screenshot(driver, request.node.name)
    
    driver.quit()


def take_allure_screenshot(driver, test_name):
    """Take screenshot and attach to Allure report"""
    try:
        # Take screenshot as PNG
        screenshot = driver.get_screenshot_as_png()
        
        # Attach to Allure report
        allure.attach(
            screenshot,
            name=f"screenshot_{test_name}",
            attachment_type=allure.attachment_type.PNG
        )
        print(f"📸 Screenshot captured for failed test: {test_name}")
    except Exception as e:
        print(f"⚠️ Could not capture screenshot: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results for Allure reporting
    Runs automatically for every test
    """
    outcome = yield
    report = outcome.get_result()
    
    # Store test result for later use (screenshots)
    setattr(item, "rep_" + report.when, report)


# Optional: Add environment info to Allure report
def pytest_sessionfinish(session, exitstatus):
    """Add environment properties to Allure results"""
    # Create allure-results directory if it doesn't exist
    os.makedirs("allure-results", exist_ok=True)
    
    # Write environment properties
    env_props = {
        "Python.Version": "3.13.1",
        "Test.Framework": "pytest",
        "Browser.Default": "Chrome",
        "Project": "ParaBank Automation",
        "OS": "Windows",
        "Selenium.Version": "4.15.0"
    }
    
    try:
        with open("allure-results/environment.properties", "w") as f:
            for key, value in env_props.items():
                f.write(f"{key}={value}\n")
        print("✅ Environment properties saved for Allure report")
    except Exception as e:
        print(f"⚠️ Could not save environment properties: {e}")