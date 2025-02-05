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
>- Configurable tax rates via [.yml](configs/tax_rates.yml) config: <br>
>- Resulsts are the following pay periods:<br>
    `hourly` <br>
    `weekly` <br>
    `biweekly` <br>
    `semi_monthly` <br>
>- Unit [pytest](tests/test_paycheck.py) included: <br>
>- Run containerized code as `pyvenv` alternative using [Docker](env_build/setup.Dockerfile): <br>
---

### Repository Container Structure:
```bash
/paycheck# ls -als
total 84
8 drwxr-xr-x 1 root root 4096 Feb  5 04:21 .
4 drwxr-xr-x 1 root root 4096 Feb  5 04:19 ..
4 drwxr-xr-x 7 root root 4096 Feb  5 00:04 .git
4 drwxr-xr-x 3 root root 4096 Feb  4 23:14 .github
4 -rw-r--r-- 1 root root 3526 Feb  4 21:56 .gitignore
4 -rw-r--r-- 1 root root 1759 Feb  4 21:57 LICENSE
8 -rw-r--r-- 1 root root 4922 Feb  4 23:07 README.md
0 -rwx------ 1 root root    0 Feb  4 21:57 __init__.py
4 drwx------ 2 root root 4096 Feb  4 21:57 configs
4 drwx------ 2 root root 4096 Feb  4 21:58 deps
4 drwxr-xr-x 2 root root 4096 Feb  5 04:07 env_build
8 drwx------ 1 root root 4096 Feb  5 04:22 modules
4 drwxr-xr-x 2 root root 4096 Feb  4 21:58 notes
4 drwxr-xr-x 2 root root 4096 Feb  4 21:58 output_screenshots
4 -rw-r--r-- 1 root root  714 Feb  4 21:59 pytest.ini
8 drwx------ 1 root root 4096 Feb  5 04:22 src
8 drwxr-xr-x 1 root root 4096 Feb  5 04:22 tests
```
### Container FS Tree:
```bash
/paycheck# tree .
|-- LICENSE
|-- README.md
|-- __init__.py
|-- configs
|   `-- tax_rates.yml
|-- deps
|   `-- requirements.txt
|-- env_build
|   |-- build_docker.sh
|   |-- image_digests.ini
|   |-- setup.Dockerfile
|   `-- setup.Dockerfile.bak
|-- modules
|   |-- data_mapping.py
|   `-- lib_check.py
|-- notes
|   `-- state_per_county_tax_rates.yml
|-- output_screenshots
|   |-- all_states.png
|   |-- group_of_states.png
|   |-- one_state.png
|   |-- pytest_cases.png
|   `-- pytests_all.png
|-- pytest.ini
|-- src
|   |-- math_check.py
|   `-- paycheck_calculator.py
`-- tests
    |-- conftest.py
    `-- test_paycheck.py

9 directories, 22 files
/paycheck#
```
## Dependencies:
#### Python & Required Libraries:
>- Written and tested on `Python` `3.13`, also compatible with lower versions if needed [e.g., `~=3.10`] assuming deps are installed: <br>
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
#### Containerized Execution by Docker Engine:
>- Docker Engine needs to be installed and running prior the Docker-based setup:
>- build on `Docker version 27.4.0`
```bash
docker --version
```
```bash
docker info
```

# Setup & Install:
>- Clone repo: 
```bash
git clone https://github.com/Vlad-1618M/paycheck.git
cd paycheck
```
### <span style="color:magenta;">Option 1:</span> Build Using `build_docker.sh` [ Recommended ]
>- <span style="color:magenta;"> Run [build_docker.sh](./env_build/build_docker.sh) </span> script | follow user prompts:

![Setup Output](output_screenshots/env_setup.png)
>- <span style="color:magenta;"> bash</span> in to your <span style="color:magenta;">tagged</span> container image:
```bash
docker images -a
REPOSITORY   TAG       IMAGE ID       CREATED              SIZE
paycheck     arm64        x           About a minute ago   657MB
```
```bash
docker run -it paycheck:arm64 bash
```
---
### <span style="color:yellow;"> Option 2:</span> Manual Build Without [build_docker.sh](./env_build/build_docker.sh) script:
>- NOTE:<br> <span style="color:yellow;"> docker build </span> doesn’t support direct substitution in the <span style="color:yellow;"> FROM </span> statement without pre-processing the Dockerfile: <br>
Since this project is desinged to support both <span style="color:yellow;">linux</span> and <span style="color:yellow;">macOS</span> architecture by tagging <span style="color:yellow;">arm</span> or <span style="color:yellow;">amd</span> during build stages using single <span style="color:yellow;">Dockerfile</span> instead of one for each, the <span style="color:yellow;">build_docker.sh</span> shell script automation hack was writtent as a work around for Docker limitations, which now helps to retain single Dockerfile to support `>1` architecture design: `-->` see <span style="color:magenta;">Option 1</span> above:
#### If you prefer to build <span style="color:yellow;"> container manually</span>: without existing shell hack, follow the steps below:<br>
>- Step <span style="color:yellow;">1</span>. Export Architecture-Specific Digest
```bash
export ARCH=arm64  # ... for macOS:
export DIGEST=$(awk -F ' = ' "/$ARCH/ {print \$2}" env_build/image_digests.ini)
echo -e "\tArchitecture Digest in use:\t --> [ $DIGEST ]"
```
```bash
export ARCH=amd64  # ... for Linux or != macOS:
export DIGEST=$(awk -F ' = ' "/$ARCH/ {print \$2}" env_build/image_digests.ini)
echo -e "\tArchitecture Digest in use:\t --> [ $DIGEST ]"
```
>- Step <span style="color:yellow;">2</span>. Replace the PLACEHOLDER_DIGEST variable in Dockerfile dynamically:
```bash
sed "s|PLACEHOLDER_DIGEST|$DIGEST|g" env_build/setup.Dockerfile > env_build/setup.Dockerfile.tmp
```
>- Step <span style="color:yellow;">3</span>. Now you can build using new <span style="color:yellow;">Dockerfile.tmp</span> where Architecture has been correctly configured and <span style="color:yellow;"> docker build </span> is happy:
```bash
docker build -t paycheck --no-cache --progress=plain -f env_build/setup.Dockerfile.tmp .
```
>- Final <span style="color:yellow;">Step</span>:
You can now bash in to your container: 
```bash
docker images -a
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
paycheck     latest      x            18 minutes ago   657MB
```
```bash
docker run -it paycheck bash
```
```bash                                                                                                                                                                     took  
docker images -a
EPOSITORY   TAG       IMAGE ID       CREATED          SIZE
paycheck    latest      x            21 minutes ago   657MB

docker run -it paycheck bash

root@:/paycheck# ls -asl
total 136
 4 drwxr-xr-x 1 root root  4096 Feb  5 17:45 .
 4 drwxr-xr-x 1 root root  4096 Feb  5 18:05 ..
 4 drwxr-xr-x 2 root root  4096 Feb  5 17:45 .benchmarks
52 -rw-r--r-- 1 root root 53248 Feb  5 17:45 .coverage
 4 drwxr-xr-x 7 root root  4096 Feb  5 17:06 .git
 4 drwxr-xr-x 3 root root  4096 Feb  4 23:14 .github
 4 -rw-r--r-- 1 root root  3526 Feb  4 21:56 .gitignore
 4 drwxr-xr-x 3 root root  4096 Feb  5 17:45 .pytest_cache
 4 -rw-r--r-- 1 root root  1759 Feb  4 21:57 LICENSE
12 -rw-r--r-- 1 root root  8259 Feb  5 17:42 README.md
 0 -rwx------ 1 root root     0 Feb  4 21:57 __init__.py
 4 drwxr-xr-x 2 root root  4096 Feb  5 17:45 __pycache__
 4 drwx------ 2 root root  4096 Feb  4 21:57 configs
 4 drwx------ 2 root root  4096 Feb  4 21:58 deps
 4 drwxr-xr-x 2 root root  4096 Feb  5 17:44 env_build
 4 drwx------ 3 root root  4096 Feb  4 21:58 modules
 4 drwxr-xr-x 2 root root  4096 Feb  4 21:58 notes
 4 drwxr-xr-x 2 root root  4096 Feb  5 04:34 output_screenshots
 4 -rw-r--r-- 1 root root   714 Feb  4 21:59 pytest.ini
 4 drwx------ 1 root root  4096 Feb  4 21:59 src
 4 drwxr-xr-x 1 root root  4096 Feb  4 21:59 tests
root@:/paycheck#
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
