#!/usr/bin/env python

""" ==========================================================================================================================
PayCheck Class Test Suite : test_paycheck.py
                Purpose   : Tests salary calculations with federal, state and FICA tax deductions with different pay periods.
                Author    : Vlad Menshikov
                Date      : 2025-01-20
                Version   : 1.0
                Contact   : dalvqsec@gmail.com

                Test      : Run script call to print all US state names:
                Example:  : `pytest --cache-clear -v -r charts tests/test_paycheck.py`
========================================================================================================================== """

import pytest
from src.math_check import PayCheck
from conftest import MOCK_TAX_CONFIG

# Test-Case | PayCheck object initialization:
def test_paycheck_initialization(mock_paycheck):
    """Ensure the PayCheck object initializes correctly with expected attributes."""
    paycheck = PayCheck(annual_salary=100000, marital_status='s', state='CA')
    assert paycheck.annual_salary == 100000
    assert paycheck.marital_status == 's'
    assert paycheck.state == 'CA'
    assert paycheck.state_tax_rate == MOCK_TAX_CONFIG["state_tax_rates"]["CA"]

# Test-Case | federal tax calculation:
def test_federal_tax(mock_paycheck):
    """Ensure federal tax is correctly calculated using tax brackets."""
    paycheck = PayCheck(100000, 's', 'CA')
    federal_tax = paycheck._calculate_federal_tax(100000 / 26)
    assert federal_tax > 0  # Federal tax should always be deducted

# Test-Case | FICA tax calculation [ Social Security + Medicare ]:
def test_fica_tax(mock_paycheck):
    """Verify FICA tax is deducted correctly."""
    paycheck = PayCheck(100000, 's', 'CA')
    fica_tax = paycheck._calculate_fica_tax(100000 / 26)
    expected_fica = (MOCK_TAX_CONFIG["fica"]["social_security"] + MOCK_TAX_CONFIG["fica"]["medicare"]) * (100000 / 26)
    assert round(fica_tax, 2) == round(expected_fica, 2)

# Test-Case | state tax calculation dynamically:
@pytest.mark.parametrize("tag_id", MOCK_TAX_CONFIG["state_tax_rates"].keys(), ids=lambda state: f"State: {state}")
def test_state_tax(mock_paycheck, tag_id):
    """Test state tax calculation dynamically for all states."""
    paycheck = PayCheck(100000, 's', tag_id)
    state_tax = paycheck._calculate_state_tax(100000 / 26)

    expected_tax_rate = MOCK_TAX_CONFIG["state_tax_rates"][tag_id]
    expected_tax = (expected_tax_rate * 100000) / 26  # ... biweekly pay-period:

    assert round(state_tax, 2) == round(expected_tax, 2), f"Mismatch for {tag_id}"

# Test-Case | states with 0% tax [e.g., TX, FL, NV, WA ]
@pytest.mark.parametrize("no_tax_state", ["TX", "FL", "NV", "WA"])
def test_state_tax_exempt(mock_paycheck, no_tax_state):
    """Ensure no state tax is deducted for tax-free states."""
    paycheck = PayCheck(100000, 's', no_tax_state)
    state_tax = paycheck._calculate_state_tax(100000 / 26)
    assert state_tax == 0, f"Expected no tax for {no_tax_state}, got {state_tax}"

# Test-Case | various paycheck calculations:
@pytest.mark.parametrize("pay_method", ["calculate_biweekly_paycheck", "calculate_semi_monthly_paycheck", "calculate_weekly_paycheck", "calculate_hourly_paycheck"])
def test_paycheck_calculations(mock_paycheck, pay_method):
    """Ensure paycheck calculations return positive values."""
    paycheck = PayCheck(100000, 's', 'CA')
    net_pay = getattr(paycheck, pay_method)()
    assert net_pay > 0, f"{pay_method} returned non-positive value"

# Test-Case | invalid state handling:
def test_invalid_state(mock_paycheck):
    """Ensure an invalid state raises KeyError."""
    with pytest.raises(KeyError, match="Invalid state code: XX"):
        PayCheck(100000, 's', 'XX')

# Test-Case | invalid marital status handling:
def test_invalid_marital_status(mock_paycheck):
    """Ensure an invalid marital status raises KeyError."""
    with pytest.raises(KeyError, match="Invalid marital status: x"):
        PayCheck(100000, 'x', 'CA')

# Test-Case | all states' net pay calculation:
def test_calculate_all_states(mock_paycheck):
    """Ensure all states' paycheck calculations return expected results."""
    paycheck = PayCheck(100000, 's', 'ANY')
    net_pay_all_states = paycheck.calculate_all_states()
    assert isinstance(net_pay_all_states, dict)
    assert set(MOCK_TAX_CONFIG["state_tax_rates"].keys()) == set(net_pay_all_states.keys())

# Test-Case | federal tax bracket application:
def test_federal_tax_brackets(mock_paycheck):
    """Ensure federal tax bracket calculations apply correctly."""
    paycheck = PayCheck(50000, 's', 'CA')
    federal_tax = paycheck._calculate_federal_tax(50000 / 26)
    assert federal_tax > 0  # ... federal income tax should be deducted:

# Test-Case | full paycheck flow:
def test_full_paycheck_flow(mock_paycheck):
    """Ensure full paycheck calculation works for a high-income scenario."""
    paycheck = PayCheck(120000, 'm', 'NY')
    biweekly_pay = paycheck.calculate_biweekly_paycheck()
    assert biweekly_pay > 0 
