#!/bin/bash
set -e

app_version=$(eval poetry version --short)
python -m celery --app celery_app worker -l WARNING -n resolvrisk:${app_version}@%h
