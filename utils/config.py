"""
Configuration parameters for the SauceDemo QA Automation Framework.
"""

# Base URL for the demo e-commerce application
BASE_URL = "https://www.saucedemo.com/"

# Explicit wait timeout in seconds
EXPLICIT_WAIT = 10

# Test User Credentials provided by SauceDemo
STANDARD_USER = "standard_user"
LOCKED_USER = "locked_out_user"
PROBLEM_USER = "problem_user"
PERF_GLITCH_USER = "performance_glitch_user"

# Standard Password
PASSWORD = "secret_sauce"
INVALID_PASSWORD = "wrong_password"
INVALID_USER = "invalid_user"
