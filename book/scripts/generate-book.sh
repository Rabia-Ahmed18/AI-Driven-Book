#!/bin/bash

# Script to generate book from specifications
# This script will process spec files and generate corresponding book content

echo "Generating book content from specifications..."

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "Node.js is required but not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "npm is required but not installed. Please install npm first."
    exit 1
fi

# Install dependencies if not already installed
echo "Installing dependencies..."
npm install

# Run the build process
echo "Building the book..."
npm run build

echo "Book generation completed successfully!"