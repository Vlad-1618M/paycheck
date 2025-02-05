#!/usr/bin/env python

""" ====================================================================================================
Script Name : paycheck_calculator.py
Description : Calculates net pay based on state tax rates, salary, and marital status. 
              Returns formatted results using tables for different pay types [ weekly, bi-weekly, etc.]
              
Author      : Vlad Menshikov
Date        : 2025-01-20
Version     : 1.0
Contact     : dalvqsec@gmail.com

Dependencies:
        - Python 3.x
        - rich lib             [ for colored table formatting ]
        - modules.data_mapping [ for state mappings           ]
        - math_check.PayCheck  [ for paycheck calculations    ]

Usage       : Run the script: 
              follow prompts to input [ salary , marital status, and state selection ]
              Example: `python paycheck_calculator.py`
==================================================================================================== """

import os
import sys
from rich.text import Text
from rich.table import Table
from rich.console import Console

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from math_check import PayCheck
from modules import data_mapping

console = Console()

def format_state_header(state_code, marital_status):
    """Format state code, full state name, and marital status with colors:"""
    state_full_name = data_mapping.us_states().get(state_code, "Unknown")
    return f"[orange3]{state_code} | {state_full_name:<15}[/orange3] | [yellow]{marital_status:<7}[/yellow]"

def display_state_table(states_net_pay, marital_status):
    """ Show table of states | state net pay for all pay types with labels:"""
    table = Table(show_header=True, header_style="bold green")
    for state_code, pay_data in states_net_pay.items():
        header = format_state_header(state_code, marital_status)
        table.add_column(header, style="cyan")

    for pay_type, label in data_mapping.compensation_type().items():
        row = []
        for pay_data in states_net_pay.values():
            amount = pay_data[pay_type]
            formatted_amount = Text()
            formatted_amount.append(f"{label:<17}:    ", style="cyan")
            formatted_amount.append("$", style="green")
            formatted_amount.append(f" {amount:.2f}", style="bold white")
            row.append(formatted_amount)
        table.add_row(*row, end_section=True)
    console.print(table)

def chunk_states(data, chunk_size=5):
    """ Split data dictionary into chunks of `chunk_size` states for horizontal table display:"""
    items = list(data.items())
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

def calculate_net_pay(paycheck):
    """Calculate all net pay types for a given paycheck instance:"""
    return {
        data_mapping.compensation_type()["Weekly"]: paycheck.calculate_weekly_paycheck(),
        data_mapping.compensation_type()["Bi-weekly"]: paycheck.calculate_biweekly_paycheck(),
        data_mapping.compensation_type()["Semi-monthly"]: paycheck.calculate_semi_monthly_paycheck(),
        data_mapping.compensation_type()["Hourly"]: paycheck.calculate_hourly_paycheck()
    }

def get_states_net_pay(state_codes, annual_salary, marital_status_input):
    """Get the net pay dictionary for given state codes:"""
    net_pay_data = {}
    for state_code in state_codes:
        paycheck = PayCheck(annual_salary, marital_status_input, state_code)
        net_pay_data[state_code] = calculate_net_pay(paycheck)
    return net_pay_data


def get_user_input():
    """User prompt for salary and marital status:"""
    console.print("\n[bold white]... Annual Salary  ?[/bold white]", end=" ")
    annual_salary = float(input())
    console.print("[blue]... Marital Status ?[/blue] ('[green]s[/green]' single, '[bold blue]m[/bold blue]' married):", end=" ")
    marital_status_input = input().strip().lower()
    if marital_status_input not in ('s', 'm'):
        console.print("\n[bold red]Error:[/bold red] Invalid marital status. Use '[green]s[/green]' single or '[blue]m[/blue]' married.", style="bold red")
        raise ValueError("Invalid marital status. Use 's' for single or 'm' for married.")
    marital_status = '[cyan]Single[/cyan]' if marital_status_input == 's' else '[magenta]Married[/magenta]'
    return annual_salary, marital_status, marital_status_input

def process_paycheck():
    """ Process paycheck calculation for: | specific state | all states | or a group of states based on user input:"""
    try:
        annual_salary, marital_status, marital_status_input = get_user_input()
        state_choice = console.input("[bold red]... math options are:[/bold red]\n\n" 
                                     "\t [bold white]-->[/bold white] [bold green]'s'[/bold green]\tfor one state:\n"
                                     "\t [bold white]-->[/bold white] [bold yellow]'a'[/bold yellow]\tfor all states:\n" 
                                     "\t [bold white]-->[/bold white] [bold magenta]'g'[/bold magenta]\tfor a group of states: ").strip().lower()

        if state_choice == 's':
            state = console.input("\n[bold white]Enter the state code (e.g.,[bold green]'CA' [/bold green]for [bold green]California [/bold green]): [/bold white]").strip().upper()
            states_net_pay = get_states_net_pay([state], annual_salary, marital_status_input)
            console.print("\nNet pay for the specified state by pay type:\n", style="bold underline green")
            display_state_table(states_net_pay, marital_status)

        elif state_choice == 'a':
            paycheck = PayCheck(annual_salary, marital_status_input, 'ANY')
            states_net_pay = get_states_net_pay(paycheck.all_state_tax_rates.keys(), annual_salary, marital_status_input)
            console.print("\nNet pay for all states by pay type:\n", style="reverse bold yellow underline")
            chunks = chunk_states(states_net_pay, 5)
            for chunk in chunks:
                display_state_table(dict(chunk), marital_status)

        elif state_choice == 'g':
            state_codes = console.input("\n[bold magenta]Enter a comma-separated list of state codes (e.g., [bold white]'CA,IL,FL,NY,TX'[/bold white]):[/bold magenta]").strip().upper().split(',')
            states_net_pay = get_states_net_pay([state.strip() for state in state_codes], annual_salary, marital_status_input)
            console.print("\nNet pay for the specified group of states by pay type:\n", style="bold magenta underline")
            chunks = chunk_states(states_net_pay, 5)
            for chunk in chunks:
                display_state_table(dict(chunk), marital_status)

        else:
            console.print("\nInvalid choice. Please enter [bold green]'state'[/bold green], [bold yellow]'all'[/bold yellow], or [bold magenta]'group'[/bold magenta]", style="bold red")

    except ValueError as input_error:
        console.print(f"\tError: [dim white italic]{input_error}[/dim white italic]", style="bold red")

if __name__ == "__main__":
    process_paycheck()
    