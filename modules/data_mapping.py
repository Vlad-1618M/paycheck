#!/usr/bin/env python

""" =============================================================================
Module Name : data_mapping.py
Description : Handles data mappings of US state abbreviations to full names: 
              Handles data mappings for different compensation types:

Author      : Vlad Menshikov
Date        : 2025-01-20
Version     : 1.0
Contact     : dalvqsec@gmail.com

Usage       : This module is used in `paycheck_calculator.py` for data lookups: 
              It should be imported as: `from modules import data_mapping`
        
Test:       : Run script call to print all US state names:
              Example: `python data_mapping.py`
============================================================================= """

def us_states():
    """Returns a dictionary of US state abbreviations mapped to full names:"""
    states = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado',
        'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
        'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
        'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
        'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
        'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
        'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota',
        'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington',
        'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
    }
    return states


def compensation_type():
    """Returns a dictionary of different compensation types: """
    pay_types = {
        "Weekly": "Weekly",
        "Bi-weekly": "Bi-weekly",
        "Semi-monthly": "Semi-monthly",
        "Hourly": "Hourly"
    }
    return pay_types


if __name__ == "__main__":
    pass
    # Debug Calls
    # -----------------------
    # print(us_states())
    # print(us_states().get("CA"))
    # [print(_) for _ in us_states().items()]
    # [print(_) for _ in us_states().keys()]
    # [print(_) for _ in us_states().values()]