#!/usr/bin/env bash

TYPE=$1
PORT=8000

python setup.py

if [ "$TYPE" = "dev" ]; then
    echo "Running in development mode"
    uvicorn src.rest:app --reload --host 0.0.0.0 --port "$PORT"
elif [ "$TYPE" = test ] || [ "$TYPE" = pytest ]; then
    echo "Running in test mode"
    pytest
elif [ "$TYPE" = "prod" ]; then
    echo "Running in production mode"
    gunicorn --workers 4 -k uvicorn.workers.UvicornWorker rest.rest:app --bind 0.0.0.0:"$PORT"
fi
#python main.py
