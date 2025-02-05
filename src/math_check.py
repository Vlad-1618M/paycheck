#!/usr/bin/env python

""" ==========================================================================================================
Module Name  : math_check.py
Description  : Defines the PayCheck class to calculate net pay across different pay periods 
               [ weekly, bi-weekly, semi-monthly, hourly ] while applying:
                 - Federal tax deductions:
                 - State tax deductions [ including local tax rates  ]
                 - FICA tax deductions  [ Social Security & Medicare ]
               
Author       : Vlad Menshikov
Date         : 2025-01-20
Version      : 1.0
Contact      : dalvqsec@gmail.com

Dependencies :
    - Python 3.x
    - PyYAML    [ for loading tax configurations ]
    - pathlib   [ for handling file paths        ]

       Usage : This module is imported in `paycheck_calculator.py`:              
               from math_check import PayCheck

     Example :
            paycheck = PayCheck(annual_salary=100000, marital_status='m', state='CA')
            net_biweekly = paycheck.calculate_biweekly_paycheck()
            print(f"Net Biweekly Pay: ${net_biweekly:.2f}")

=========================================================================================================="""

import yaml
from pathlib import Path

class PayCheck:
    """ Class to calculate net pay for different pay periods [ weekly, bi-weekly, semi-monthly, hourly ]
            federal, state, and FICA tax deductions inlcuded:
        Attributes:
            annual_salary (float): The gross annual salary of the employee:
            marital_status (str): 's' for Single, 'm' for Married:
            state (str): Two-letter state code (e.g., 'CA' for California):"""
    
    def __init__(self, annual_salary, marital_status, state):
        self.annual_salary = annual_salary
        self.marital_status = marital_status.lower()
        self.state = state.upper()
        config = self.load_config()

        if self.state != "ANY" and self.state not in config['state_tax_rates']:
            raise KeyError(f"Invalid state code: {self.state}")

        if self.marital_status not in ['s', 'm']:
            raise KeyError(f"Invalid marital status: {self.marital_status}")

        if self.state != "ANY":
            self.state_tax_rate = config['state_tax_rates'][self.state]
            self.local_tax_rate = config['local_tax_rates'].get(self.state, {}).get('state', 0.0)
        else:
            self.state_tax_rate = 0.0
            self.local_tax_rate = 0.0

        self.social_security_rate = config['fica']['social_security']
        self.medicare_rate = config['fica']['medicare']
        self.federal_tax_brackets = config['federal_withholding']['single' if self.marital_status == 's' else 'married']
        self.pay_periods = config['pay_periods']
        self.all_state_tax_rates = config['state_tax_rates']
        self.local_tax_rates = config['local_tax_rates']
        
    @staticmethod
    def load_config():
        """ Load tax_rates.yml config """
        yml_files = list(Path(__file__).resolve().parent.parent.glob('configs/*.yml'))
        if not yml_files:
            raise FileNotFoundError("\t.yml config not found:")
        
        with open(yml_files[0], 'r') as tax_config:
            return yaml.safe_load(tax_config)

    def _calculate_federal_tax(self, gross_pay):
        """Calculate federal tax using progressive tax brackets."""
        annual_income = gross_pay * self.pay_periods['biweekly']
        federal_tax = 0.0
        remaining_income = annual_income
        
        for bracket in self.federal_tax_brackets:
            if remaining_income <= bracket['up_to']:
                federal_tax += remaining_income * bracket['rate']
                break
            else:
                federal_tax += bracket['up_to'] * bracket['rate']
                remaining_income -= bracket['up_to']
        
        return federal_tax / self.pay_periods['biweekly']

    def _calculate_fica_tax(self, gross_pay):
        """Calculate FICA (Social Security & Medicare) tax."""
        return (self.social_security_rate + self.medicare_rate) * gross_pay
    
    def _calculate_state_tax(self, gross_pay):
        """Calculate state and local taxes correctly, avoiding duplication of state tax."""
        local_tax_only = self.local_tax_rate if self.local_tax_rate != self.state_tax_rate else 0.0
        return (self.state_tax_rate * gross_pay) + (local_tax_only * gross_pay)

    def calculate_biweekly_paycheck(self):
        """Calculate the bi-weekly paycheck after federal, FICA, and state tax deductions."""
        biweekly_gross_pay = self.annual_salary / self.pay_periods['biweekly']
        federal_tax = self._calculate_federal_tax(biweekly_gross_pay)
        fica_tax = self._calculate_fica_tax(biweekly_gross_pay)
        state_tax = self._calculate_state_tax(biweekly_gross_pay)
        return biweekly_gross_pay - (federal_tax + fica_tax + state_tax)

    def calculate_semi_monthly_paycheck(self):
        """Calculate the semi-monthly paycheck after federal, FICA, and state tax deductions."""
        semi_monthly_gross_pay = self.annual_salary / self.pay_periods['semi_monthly']
        federal_tax = self._calculate_federal_tax(semi_monthly_gross_pay)
        fica_tax = self._calculate_fica_tax(semi_monthly_gross_pay)
        state_tax = self._calculate_state_tax(semi_monthly_gross_pay)
        return semi_monthly_gross_pay - (federal_tax + fica_tax + state_tax)

    def calculate_weekly_paycheck(self):
        """Calculate the weekly paycheck after federal, FICA, and state tax deductions."""
        weekly_gross_pay = self.annual_salary / self.pay_periods['weekly']
        federal_tax = self._calculate_federal_tax(weekly_gross_pay)
        fica_tax = self._calculate_fica_tax(weekly_gross_pay)
        state_tax = self._calculate_state_tax(weekly_gross_pay)
        return weekly_gross_pay - (federal_tax + fica_tax + state_tax)

    def calculate_hourly_paycheck(self, hours_per_week=40):
        """Calculate the hourly rate after federal, FICA, and state tax deductions."""
        hourly_gross_pay = self.annual_salary / (self.pay_periods['weekly'] * hours_per_week)
        federal_tax = self._calculate_federal_tax(hourly_gross_pay)
        fica_tax = self._calculate_fica_tax(hourly_gross_pay)
        state_tax = self._calculate_state_tax(hourly_gross_pay)
        return hourly_gross_pay - (federal_tax + fica_tax + state_tax)

    def calculate_all_states(self):
        """Calculate net bi-weekly pay for all states using the same annual salary and marital status."""
        all_states_net_pay = {}
        for state, tax_rate in self.all_state_tax_rates.items():
            local_rate = self.local_tax_rates.get(state, {}).get('state', 0.0)
            self.state_tax_rate = tax_rate
            self.local_tax_rate = local_rate
            net_pay = self.calculate_biweekly_paycheck()
            all_states_net_pay[state] = net_pay
        return all_states_net_pay

if __name__ == "__main__":
    pass
    # debug calls: 
    # annual_salary = 2320000
    # marital_status = 'm'
    # state = "CA"
    
    # paycheck = PayCheck(annual_salary, marital_status, state)
    # net_weekly_paycheck = paycheck.calculate_weekly_paycheck()
    # net_biweekly_paycheck = paycheck.calculate_biweekly_paycheck()
    # net_semi_monthly_paycheck = paycheck.calculate_semi_monthly_paycheck()
    # net_hourly_paycheck = paycheck.calculate_hourly_paycheck()
    
    # print(f"\n\t{state:<3}Net bi-weekly paycheck:\t ${net_biweekly_paycheck:>8.2f}")
    # print(f"\t{state:<3}Net weekly paycheck:\t\t ${net_weekly_paycheck:>8.2f}")
    # print(f"\t{state:<3}Net semi-monthly paycheck:\t ${net_semi_monthly_paycheck:>8.2f}")
    # print(f"\t{state:<3}Net hourly paycheck:\t\t ${net_hourly_paycheck:>8.2f}")

