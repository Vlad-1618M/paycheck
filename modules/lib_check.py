#!/usr/bin/env python

""" ====================================================================
Script Name : lib_check.py
Description : Dynamically inspects methods and classes inside a given Python library/module. 
              Intent is to have a function that can inspect a module or specific component filter by type.

Author      : Vlad Menshikov
Date        : 2025-01-20
Version     : 1.0
Contact     : dalvqsec@gmail.com

Dependencies:
    - Python 3.x
    - rich [ optional, as subject lib used in this repo ]

    Usage   : Run the script directly to inspect attributes of 
              `rich`, `Table`, and `Console` modules:

Example:    python lib_check.py
            Or use it as module:
            from inspect_libs import inspect_libs
            print(inspect_libs("os"))
==================================================================== """

import inspect
import importlib

def inspect_libs(lib, component=None, filter_type=None):
    """ Inspects methods and classes inside a given library or a specific component: 
        Optionally filtering by type (e.g., function, class).
        Parameters:
            - lib: The library as a module object or its name as a string.
            - component: The specific component [ e.g., class or method ] of the library to inspect. [ Optional param:]
            - filter_type: The type of members to filter by [ e.g., inspect.isfunction ] [ Optional param:]
        Returns:
            A list of tuples with member name and attribute, filtered by the specified type if provided."""
    
    if isinstance(lib, str):
        try:
            lib = importlib.import_module(lib)
        except ImportError:
            return f"Library {lib} could not be imported."
    if component:
        check_attr = getattr(lib, component, None)
        if not check_attr:
            return f"The component '{component}' is not available in the selected library."
    else:
        check_attr = lib
    members = inspect.getmembers(check_attr, filter_type)
    return members


if __name__ == "__main__":
    import rich
    from rich.table import Table
    from rich.console import Console
    print("="*80)
    [print(_) for _ in inspect_libs(lib=rich)]
    print("="*80)
    [print(_) for _ in inspect_libs(lib=Table)]
    print("="*80)
    [print(_) for _ in inspect_libs(lib=Console)]
    print("="*80)
