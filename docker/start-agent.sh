#!/bin/bash
set -e

echo "Environment variables:"
env

echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la

echo "Python version:"
python --version

echo "Checking for required modules..."
python -c "import dotenv; import fastapi; import langchain_google_genai; import langgraph; print('All required modules are available')"

echo "Starting Database Agent..."
python -m agent.__main__