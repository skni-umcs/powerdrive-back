#!/usr/bin/env bash

TYPE=$1
PORT=8000

RED='\033[0;31m'
CYAN='\033[0;36m'
BRED='\033[1;31m'
NC='\033[0m' # No Color

if [ "$TYPE" = "dev" ]; then
    echo -e "${CYAN}Running in development mode${NC}"
    python setup.py dev
    uvicorn src.api:app --reload --host 0.0.0.0 --port "$PORT"

elif [ "$TYPE" = test ] || [ "$TYPE" = pytest ]; then


    export DB_NAME=powerdrive_test
    python setup.py test

    echo -e "${CYAN}Running tests...${NC}"
    pytest

elif [ "$TYPE" = "prod" ]; then
    echo -e "${BRED}What do you mean production mode XD${NC}"
#    echo "Running in production mode"
#    gunicorn --workers 4 -k uvicorn.workers.UvicornWorker src.api:app --bind 0.0.0.0:"$PORT"
fi
#python main.py
