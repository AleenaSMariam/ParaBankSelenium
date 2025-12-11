# ParaBank Selenium Automation Testing

Automated test suite for ParaBank application using Selenium WebDriver with Python.

## Table of Contents
- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Test Reports](#test-reports)
- [Configuration](#configuration)

## Project Overview

This project contains automated UI tests for the ParaBank application using industry best practices and modern testing frameworks.

### What We Test
- User Registration
- Login Functionality
- Bill Payment
- Account Management
- Other critical user workflows

### Technology Stack
| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.8+ |
| **UI Automation** | Selenium WebDriver 4.15.0 |
| **Design Pattern** | Page Object Model (POM) |
| **Testing Framework** | pytest |
| **Test Reporting** | Allure Reports |
| **WebDriver Management** | webdriver-manager |
| **Data Handling** | openpyxl (Excel support) |

### Architecture & Design Patterns
- **Page Object Model (POM):** All UI interactions are encapsulated in page objects for better maintainability
- **Selenium WebDriver:** Industry-standard WebDriver for cross-browser automation
- **Python:** Clean, readable, and maintainable test code
- **Explicit Waits:** Reliable element interactions using WebDriverWait
- **Data-Driven Testing:** Separate test data from test logic
- **Allure Reports:** Beautiful, detailed HTML test reports with history tracking  

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/AleenaSMariam/ParaBankSelenium.git
cd ParaBankSelenium
```

2. **Create a virtual environment (optional but recommended):**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Project Structure

```
ParaBankSelenium/
├── pages/                    # Page Object Models
│   ├── register_page.py
│   ├── login_page.py
│   ├── bill_pay_page.py
│   └── ...
├── tests/                    # Test cases
│   ├── test_registration.py
│   ├── test_login.py
│   ├── test_bill_pay.py
│   └── ...
├── utilities/                # Helper functions and utilities
│   ├── driver_setup.py
│   ├── common_functions.py
│   └── ...
├── test_data/                # Test data and fixtures
├── conftest.py               # pytest configuration and fixtures
├── requirements.txt          # Project dependencies
├── pytest.ini                # pytest settings
├── allure.yml                # Allure configuration
└── README.md                 # This file
```

## Running Tests

### Run all tests:
```bash
pytest -v
```

### Run specific test file:
```bash
pytest tests/test_registration.py -v
```

### Run specific test class:
```bash
pytest tests/test_registration.py::TestRegistration -v
```

### Run with Allure reporting:
```bash
pytest --alluredir=allure-results
```

## Test Reports

### Generate Allure Report:
```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

Or use the provided script:
```powershell
.\run_allure.ps1
```

This will generate and open the Allure report in your default browser.

## Continuous Integration (Jenkins)

This project is configured for CI/CD using Jenkins.

### Configuration
- **Source Code Management:** Git (GitHub)
- **Build Triggers:** Poll SCM (`H/5 * * * *` runs every 5 minutes if changes are detected)
- **Build Environment:** Python 3.8+

### Build Steps
1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run Tests:**
   ```bash
   pytest --alluredir=allure-results
   ```

### Reporting
- **Allure Plugin:** The Allure Jenkins plugin is used to generate trend reports and visualize test results within Jenkins.

## Configuration

### pytest.ini
Contains pytest configuration including test discovery patterns and marker definitions.

### conftest.py
Contains shared pytest fixtures such as:
- WebDriver setup and teardown
- Test data fixtures
- Logging configuration

### allure.yml
Allure-specific configuration for report generation.

## Dependencies

- `selenium==4.15.0` - WebDriver automation
- `pytest==7.4.0` - Testing framework
- `pytest-html==4.1.1` - HTML test reports
- `webdriver-manager==4.0.1` - WebDriver management
- `openpyxl==3.1.2` - Excel file handling
- `pytest-allure==4.0.2` - Allure report integration

## Best Practices

1. **Page Object Model:** All UI elements and interactions are encapsulated in page objects
2. **Explicit Waits:** Used for reliable element interactions
3. **Data-Driven Testing:** Test data is separated from test logic
4. **Screenshots:** Automatic screenshots on test failures for debugging
5. **Logging:** Comprehensive logging for test execution tracking

## Troubleshooting

### Import errors for selenium:
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### WebDriver issues:
The project uses `webdriver-manager` to automatically download the correct WebDriver version.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For issues or questions, please create an issue in the GitHub repository.
