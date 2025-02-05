#!/usr/bin/env python

""" =================================================================================================
Mocked Income-Tax Config used in PayCheck PyTests : conftest.py
    - Data Feeder: 
    - All state income-tax rates: 
    - Local income-tax rates: 
    - Federal income-tax brackets:
    - Pay periods:
    
    - Mocking helps with reducing file I/O by hardcoding values instead of reading from tax_rates.yml
    - Written to inject a stable, test controll environment:

    Author    : Vlad Menshikov
    Date      : 2025-01-20
    Version   : 1.0
    Contact   : dalvqsec@gmail.com
================================================================================================= """

import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from src.math_check import PayCheck

# Mocked Income-Tax Config:
MOCK_TAX_CONFIG = {
    "state_tax_rates": {
        "AL": 0.05, "AK": 0.0, "AZ": 0.041, "AR": 0.065, "CA": 0.093, "CO": 0.0455, "CT": 0.05, "DE": 0.029, "FL": 0.0,
        "GA": 0.0575, "HI": 0.08, "ID": 0.0625, "IL": 0.0495, "IN": 0.0323, "IA": 0.045, "KS": 0.053, "KY": 0.05, "LA": 0.04,
        "ME": 0.0715, "MD": 0.0575, "MA": 0.05, "MI": 0.0425, "MN": 0.0785, "MS": 0.05, "MO": 0.054, "MT": 0.0, "NE": 0.0684,
        "NV": 0.0, "NH": 0.0, "NJ": 0.0637, "NM": 0.049, "NY": 0.0645, "NC": 0.0525, "ND": 0.0227, "OH": 0.048, "OK": 0.05,
        "OR": 0.0875, "PA": 0.0307, "RI": 0.0575, "SC": 0.07, "SD": 0.0, "TN": 0.0, "TX": 0.0, "UT": 0.0495, "VT": 0.086,
        "VA": 0.0575, "WA": 0.0, "WV": 0.06, "WI": 0.053, "WY": 0.0
    },
    "local_tax_rates": {
        "CA": {"state": 0.093, "la_county": 0.01}, "TX": {"state": 0.0, "houston": 0.0}, "NY": {"state": 0.0645, "nyc": 0.038},
        "FL": {"state": 0.0, "miami": 0.01}, "PA": {"state": 0.0307, "philadelphia": 0.035}, "IL": {"state": 0.0495, "chicago": 0.0125},
        "WA": {"state": 0.0, "seattle": 0.0}, "OH": {"state": 0.048, "cleveland": 0.02}
    },
    "fica": {
        "social_security": 0.062,
        "medicare": 0.0145
    },
    "federal_withholding": {
        "single": [
            {"up_to": 9950, "rate": 0.10}, {"up_to": 40525, "rate": 0.12},
            {"up_to": 86375, "rate": 0.22}, {"up_to": 164925, "rate": 0.24}
        ],
        "married": [
            {"up_to": 19900, "rate": 0.10}, {"up_to": 81050, "rate": 0.12},
            {"up_to": 172750, "rate": 0.22}, {"up_to": 329850, "rate": 0.24}
        ]
    },
    "pay_periods": {
        "weekly": 52, "biweekly": 26, "semi_monthly": 24, "monthly": 12
    }
}

# load_config() Mock:
@pytest.fixture
def mock_paycheck(monkeypatch):
    """Mock the PayCheck class to use the predefined tax configuration instead of reading from a file."""
    def mock_load_config():
        return MOCK_TAX_CONFIG
    monkeypatch.setattr(PayCheck, "load_config", staticmethod(mock_load_config))

# Test IDs based on state names:
@pytest.fixture(
    params=MOCK_TAX_CONFIG.get("state_tax_rates", {}).keys(), 
    ids=lambda state: f"State: {state}"
)
def tag_id(request):
    """Fixture to parameterize tests with state codes dynamically."""
    return request.param

