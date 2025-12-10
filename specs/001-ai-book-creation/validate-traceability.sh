#!/bin/bash
# validate-traceability.sh
# Script to validate traceability between specifications and content

echo "Validating spec-content traceability..."

# Check if all spec files have corresponding content files
echo "Checking spec-to-content mapping..."

SPEC_DIRS=("001-intro" "002-spec-cycle" "003-ai-collaboration" "004-deploy-automate" "005-governance")

all_valid=true

for dir in "${SPEC_DIRS[@]}"; do
    spec_path="specs/$dir/spec.md"
    plan_path="specs/$dir/plan.md"
    
    # Determine the content file name from the directory name
    if [ "$dir" = "001-intro" ]; then
        content_file="intro"
    elif [ "$dir" = "002-spec-cycle" ]; then
        content_file="spec-cycle"
    elif [ "$dir" = "003-ai-collaboration" ]; then
        content_file="ai-collaboration"
    elif [ "$dir" = "004-deploy-automate" ]; then
        content_file="deploy-automate"
    elif [ "$dir" = "005-governance" ]; then
        content_file="governance"
    fi
    
    content_path="docs/$dir/$content_file.mdx"
    
    if [ -f "$spec_path" ]; then
        if [ -f "$content_path" ]; then
            echo "✓ $dir: spec and content files exist"
        else
            echo "✗ $dir: spec exists but content file missing: $content_path"
            all_valid=false
        fi
    else
        echo "✗ $dir: spec file missing: $spec_path"
        all_valid=false
    fi
    
    if [ -f "$plan_path" ]; then
        echo "  - Plan file exists: $plan_path"
    else
        echo "  - Plan file missing: $plan_path"
        all_valid=false
    fi
done

echo ""
echo "Checking if content files reference their specs..."

# Check if content references are in the sidebar
SIDEBAR_ITEMS=("intro/intro" "spec-cycle/spec-cycle" "ai-collaboration/ai-collaboration" "deploy-automate/deploy-automate" "governance/governance")

for item in "${SIDEBAR_ITEMS[@]}"; do
    if grep -q "$item" sidebars.js; then
        echo "✓ Sidebar contains reference: $item"
    else
        echo "✗ Sidebar missing reference: $item"
        all_valid=false
    fi
done

echo ""
if [ "$all_valid" = true ]; then
    echo "✅ All traceability checks passed!"
    exit 0
else
    echo "❌ Some traceability issues found!"
    exit 1
fi