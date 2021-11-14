#!/bin/bash
set -e

python -m uvicorn fastapi_app:fastapi_app --reload
