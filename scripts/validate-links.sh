#!/bin/bash

# Script to validate links in documentation using lychee
# This ensures we meet the success criteria of 0 broken links

echo "Validating links in documentation..."

# Check if lychee is installed
if ! command -v lychee &> /dev/null; then
    echo "lychee is not installed. Installing via npm..."
    npm install -g lychee
fi

# Run lychee on all MDX files in docs directory
lychee --verbose --format markdown docs/**/*.mdx

# Capture exit code
exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "✓ All links are valid!"
    exit 0
else
    echo "✗ Broken links found!"
    exit $exit_code
fi