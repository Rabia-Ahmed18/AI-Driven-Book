# AI/Spec-Driven Book Creation

This project implements a technical book authored and maintained using AI-assisted, spec-first workflows. It follows the principles of Spec-Driven Integrity, AI-Augmented Authoring, and Reproducible Processes.

## Project Structure

```
book/
├── src/                 # Book content source files (Markdown)
│   ├── chapters/        # Individual book chapters
│   ├── sections/        # Book sections within chapters
│   └── assets/          # Images, diagrams, and other assets
├── specs/               # Specifications for each chapter/section
│   └── [chapter-name]/  # Spec files for each chapter
├── build/               # Build artifacts and configuration
│   ├── config/          # Build configuration files
│   └── tools/           # Build scripts and utilities
├── docs/                # Documentation files
├── scripts/             # Utility scripts
│   └── generate-book.sh # Script to generate book from specs
├── templates/           # Content templates
│   ├── chapter-template.md
│   └── section-template.md
└── package.json         # Node.js package configuration for build tools
```

## Getting Started

1. Create specifications for your book chapters in the `specs/` directory
2. Generate initial content from specifications using the provided scripts
3. Run `npm run build` to build the book with zero warnings
4. Run `npm run serve` to serve the book locally for review

## Commands

- `npm run build` - Build the book with zero warnings
- `npm run serve` - Serve the book locally
- `npm run validate` - Validate specs and content
- `npm run generate` - Generate content from specifications

## Spec-Driven Integrity

Every chapter, section, and code example must originate from or be validated against an explicit spec (via `/sp.specify` and `/sp.plan`).

## AI-Augmented Authoring

Leverage Claude Code for drafting, refactoring, and validation—but always maintain human-in-the-loop oversight for accuracy, voice, and coherence.