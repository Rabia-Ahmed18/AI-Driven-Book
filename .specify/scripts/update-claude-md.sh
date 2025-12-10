#!/bin/bash

# Script to update CLAUDE.md with interaction records
# This script will be called by SpecKit Plus commands to maintain audit trail

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <command> <description>"
    exit 1
fi

COMMAND=$1
DESCRIPTION=$2
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

# Check if CLAUDE.md exists, create if it doesn't
if [ ! -f "CLAUDE.md" ]; then
    cat > CLAUDE.md << 'EOF'
# CLAUDE Interactions Documentation

This document tracks all Claude Code interactions for the AI/Spec-Driven Book Creation project. Each interaction is documented to maintain transparency and traceability as required by the project's success criteria.
EOF
fi

# Get the next interaction number
NEXT_NUM=$(($(grep -c "^## Interaction #" CLAUDE.md) + 1))

# Append the new interaction record
cat >> CLAUDE.md << EOF


## Interaction #$NEXT_NUM: $COMMAND

**Date**: $(date -u +"%Y-%m-%d")
**Command**: $COMMAND
**Purpose**: $DESCRIPTION
**Actions Taken**:
-

**Outcome**:

EOF

echo "Interaction #$NEXT_NUM added to CLAUDE.md"