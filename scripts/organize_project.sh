#!/bin/bash
# Script to organize the project structure for Hugging Face Spaces deployment

# Create directory structure
mkdir -p app/api
mkdir -p app/models
mkdir -p app/schemas
mkdir -p app/database
mkdir -p app/utils
mkdir -p app/core

# Move existing files to appropriate locations if needed
if [ -f main.py ]; then
    mv main.py app/
fi

if [ -f models.py ]; then
    mv models.py app/models/
fi

if [ -f config.py ]; then
    mv config.py app/core/
fi

# Create __init__.py files to make directories into Python packages
touch app/__init__.py
touch app/api/__init__.py
touch app/models/__init__.py
touch app/schemas/__init__.py
touch app/database/__init__.py
touch app/utils/__init__.py
touch app/core/__init__.py

echo "Project structure organized successfully!"
echo "New structure:"
echo "app/"
echo "├── __init__.py"
echo "├── main.py"
echo "├── api/"
echo "│   └── __init__.py"
echo "├── models/"
echo "│   └── __init__.py"
echo "├── schemas/"
echo "│   └── __init__.py"
echo "├── database/"
echo "│   └── __init__.py"
echo "├── utils/"
echo "│   └── __init__.py"
echo "└── core/"
echo "    └── __init__.py"