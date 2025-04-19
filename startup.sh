#!/bin/bash

# Run content update initially
/app/update_content.sh

# Start cron
service cron start

# Start the application
export PYTHONPATH=./public
exec uvicorn public.app:app --host 127.0.0.1 --port 18000 --reload