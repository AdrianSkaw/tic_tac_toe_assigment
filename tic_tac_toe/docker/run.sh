#!/bin/bash
export FLASK_APP=tic_tac_toe.application
export FLASK_ENV=development
bash run_migration.sh
flask run --host=0.0.0.0 --port=8000
