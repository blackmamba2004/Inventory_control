#!/bin/bash

/app/scripts/wait-for-it.sh db:5432 -- alembic upgrade head

gunicorn backend.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000