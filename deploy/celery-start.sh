#!/bin/bash
set -e

app_version=$(eval poetry version --short)

python -m celery -A celery_app:app worker -l WARNING -n resolvrisk:${app_version}@%h
