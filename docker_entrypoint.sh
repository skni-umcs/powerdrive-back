#!/usr/bin/env bash

TYPE=$1
PORT=8000

python setup.py

if [ "$TYPE" = "dev" ]; then
    echo "Running in development mode"
    uvicorn src.api:app --reload --host 0.0.0.0 --port "$PORT"

elif [ "$TYPE" = test ] || [ "$TYPE" = pytest ]; then
    echo "Setup test database"
    export DB_NAME=powerdrive_test
    export DB_USER=powerdrive
    export DB_PASSWORD=powerdrive
    export DB_HOST=db
    export DB_PORT=5432
    export DB_TEST_NAME=powerdrive_test
    export DB_URL=postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME
#    export DB_URL="postgresql://postgres:postgres@db:5432/$DB_NAME"
    python setup.py test
    echo "Running tests"
    pytest
    echo "$DB_NAME"
    export

elif [ "$TYPE" = "prod" ]; then
    echo "What do you mean production mode XD"
#    echo "Running in production mode"
#    gunicorn --workers 4 -k uvicorn.workers.UvicornWorker src.api:app --bind 0.0.0.0:"$PORT"
fi
#python main.py
