#!/usr/bin/env bash
TYPE=$1
#PORT=$2
echo "Starting $TYPE on port $APP_PORT"

python setup.py
if [ "$TYPE" = "dev" ]; then
    python main.py
fi

