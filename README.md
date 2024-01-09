# io expander usage example
This is a stripped down version of our pyxdaq library that only contains the necessary code to communicate with the io expander. It is intended to be a demonstration of how to use the io expander in your own code.

## Installation
### Prerequisites
* [Git](https://git-scm.com/)
* [Python](https://www.python.org/downloads/) 3.8 or higher

### macOS
```shell
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
python3 -m pip install .
```

### Windows
```powershell
python --version # check that Python 3.8 or higher is installed
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install .
```

## Running the demo
```shell
python3 io_expander_demo.py # see example_output.txt for expected output
```
