#!/bin/bash
export FLASK_APP=tic_tac_toe.application
flask run --host=0.0.0.0
#flask db migrate -m "Initial migration."
#flask db upgrade