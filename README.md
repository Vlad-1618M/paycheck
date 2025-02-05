# Paycheck Calculator
##  Lightweight Python-based paycheck calculator: <br> 
- Computes `net pay` based on: <br>
    `tax brackets`: <br>
    `deductions`: <br>
    `marital status`: <br>
    US `State` by `State`: <br>
- supports configurable `pay periods`: <br>
---
This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software under the terms of the license.

## Tax Rate Disclaimer:
`NOTE`: Tax rates vary `state` by `state` as well as by `city/county` in some cases: <br> 
The [tax-rates](configs/tax_rates.yml) config file contains state, local, and federal tax rates used by this calculator `However`, tax laws and rates are subject to change: <br> 
To ensure accuracy, you may need to `update` the configuration file regularly based on official tax sources: <br> 
`Failure` to update the config may result in incorrect paycheck calculations:<br>
Official tax rate sources:
- [IRS Federal Tax Brackets](https://www.irs.gov/)
- [State Tax Departments](https://www.taxadmin.org/state-tax-agencies) <br>
Side Note: You may also refer to an alternative [tax-rates-notes](notes/state_per_county_tax_rates.yml) config kept in this repo for reference:
---
# Features:
>- Supports `federal` and `state` income tax calculations:<br>
>- Configurable tax rates via [tax-rates](configs/tax_rates.yml) files: <br>
>- Supports different pay periods:<br>
    `hourly` <br>
    `weekly` <br>
    `biweekly` <br>
    `semi_monthly` <br>
>- Unit [pytest](tests/test_paycheck.py) included: <br>
>- Containerized execution as `py venev` replacemnt using [Docker-Support](env_build/setup.Dockerfile): <br>
---

## Repository Structure:
```bash
|-- LICENSE
|-- README.md
|-- __init__.py
|-- configs
|   -- tax_rates.yml
|-- deps
|   -- requirements.txt
|-- env_build
|   |-- image_version_control.sh
|   |-- setup.Dockerfile
|   |-- ubu_digest
|        -- amd64_digest.json
|        -- arm64_digest.json
|-- modules
|    -- data_mapping.py
|    -- lib_check.py
|-- notes
|   -- state_per_county_tax_rates.yml
|-- pytest.ini
|-- src
|    -- math_check.py
|    -- paycheck_calculator.py
|-- tests
     -- conftest.py
     -- test_paycheck.py
```

## Dependencies:
>- Python [requirements](deps/requirements.txt) libs: 
```bash
    coverage~=7.6.10 
    pytest~=8.3.4
    pytest-benchmark~=5.1.0
    pytest-cov~=6.0.0
    pytest-timeout~=2.3.1
    pytz~=2024.2
    PyYAML~=6.0.2
    colorama~=0.4.6
    tabulate~=0.9.0
    yml~=0.0.1
    setuptools~=75.8.0
    uncompyle6~=3.9.2
    rich~=13.9.4
```
>- Docker Engine:

## Setup & Install:
```bash
git clone https://github.com/Vlad-1618M/paycheck.git
cd paycheck
```
>- Run [Docker](env_build/setup.Dockerfile) build for container image setup: 
```bash
docker build -t 'name' --no-cache --progress=plain -f env_build/setup.Dockerfile .
```
>- shell in container: 
```bash
docker run -it 'name' bash
```
>- Run Paycheck Calculator and follow user prompts:
```bash
python src/paycheck_calculator.py
```
---
## PyTest Configuration and Usage
### The configuration for pytest are in [pytest.ini](pytest.ini) file:

#### PyTest CLI Examples:
>- pytest -vv
>- pytest -m "slow"
>- pytest -m "not slow"
>- pytest -m "slow or integration"
>- pytest --cov=src --cov-report=term-missing
>- pytest -v -r charts
>- pytest -v -r fEsxX
>- pytest --cache-clear

#### [Test Suite](tests/test_paycheck.py): cli-examples:
``` bash
pytest 
pytest -v -r charts tests/test_paycheck.py
pytest -v -r fEsxX tests/test_paycheck.py
pytest -v -r charts -m "not slow" tests/test_paycheck.py
pytest --cache-clear -v -r charts tests/test_paycheck.py
pytest --cache-clear -v -r charts tests/test_paycheck.py::test_state_tax
pytest --cache-clear -v -r charts tests/test_paycheck.py::test_paycheck_calculations
pytest --cache-clear -v -r charts tests/test_paycheck.py::test_calculate_all_states
pytest --cache-clear -v -r charts tests/test_paycheck.py::test_federal_tax
```
>- Run [pytest suite](tests/test_paycheck.py):
```bash
pytest --cache-clear -v -r charts tests/test_paycheck.py
```
---
## Screenshots Examples:
![Single Sate Terminal Output](output_screenshots/one_state.png)
***
![Filtered States Terminal Output](output_screenshots/group_of_states.png)
***
![All States Terminal Output](output_screenshots/all_states.png)

# PyTest Configuration and Usage

This project leverages `pytest` for testing and includes mock and real test examples. Below are the details on running the tests, examples of commands, and visual outputs.

---

## Table of Contents
- [PyTest Configuration](#pytest.ini)
- [Config used in PyTest](configs/tax_rates.yml)
- [Markers and Test Selection](#conftest)
- [PyTests Screenshots & Examples](#pytest-screenshots--examples)

---

## Mock PyTests Screenshots Examples:
![Mock PyTest Collection Terminal Output](output_screenshots/pytests_all.png)
***
![Mock PyTest Test-Case Terminal Output](output_screenshots/pytest_cases.png)
___
