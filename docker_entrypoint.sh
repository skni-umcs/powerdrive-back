#!/usr/bin/env bash

TYPE=$1
PORT=8000

RED='\033[0;31m'
CYAN='\033[0;36m'
BRED='\033[1;31m'
NC='\033[0m' # No Color

#whoami

if [ "$TYPE" = "dev" ]; then
    echo -e "${CYAN}SETUP in development mode${NC}"

    python setup.py dev

    echo -e "${CYAN}Running in development mode${NC}"

    uvicorn src.api:app --reload --host 0.0.0.0 --port "$PORT"

elif [ "$TYPE" = "test" ] || [ "$TYPE" = "pytest" ]; then


    export PD_DB_NAME=powerdrive_test
    python setup.py test

    echo -e "${CYAN}Running tests...${NC}"
    pytest

elif [ "$TYPE" = "prod" ]; then
    echo -e "${BRED}What do you mean production mode XD${NC}"
#    echo "Running in production mode"
#    gunicorn --workers 4 -k uvicorn.workers.UvicornWorker src.api:app --bind 0.0.0.0:"$PORT"

else # pass arguments to bash
    echo -e "Other arguments passed: ${RED}$@${NC}"
    exec "$@"

#elif [ "$TYPE" = "drop_db" ]; then
#    echo -e "${BRED}Dropping database...${NC}"
#    python cmd_utils.py drop_db

fi
#python main.py
