#!/bin/bashset -euxo pipefail
cd open-codegen
    export PYTHONPATH=.
    # --- install virtualenv    
    pip install virtualenv

    # --- create virtualenv    
    virtualenv -p python3.8 venv

    # --- activate venv   
    source venv/bin/activate

    # --- upgrade pip within venv    
    pip install --upgrade pip

    # --- install opengen    
    pip install .

    # --- run the tests    
    export PYTHONPATH=.
    python -W ignore test/test_constraints.py -v    
    python -W ignore test/test.py -v