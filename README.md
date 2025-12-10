# AI/Spec-Driven Book Creation

A practical guide to building and deploying technical documentation using Spec-Driven Development and AI-assisted authoring.

## Overview

This project demonstrates how to create a production-grade technical book using Docusaurus v3, Spec-Driven Development (via Spec-Kit Plus), and Claude Code for AI-assisted authoring. The implementation emphasizes AI collaboration with human oversight, spec traceability, and automated deployment with quality gates.

## Target Audience

- Mid-to-senior software engineers and technical leads
- Developer advocates and documentation engineers
- Engineering managers exploring AI-native workflows

## Features

- ✅ Production-grade Docusaurus v3 site (responsive, i18n-ready, dark/light mode)
- ✅ Spec-driven content creation (every chapter originates from validated specs)
- ✅ AI collaboration with human oversight
- ✅ Automated deployment to GitHub Pages with CI/CD
- ✅ Quality gates: build validation, link checking, linting
- ✅ Full audit trail of Claude interactions

## Prerequisites

- Node.js (>=18.0)
- npm or yarn
- Git

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run start
   ```

3. Build the book:
   ```bash
   npm run build
   ```

4. Validate content:
   ```bash
   npm run lint
   npm run validate-links
   ```

## Project Structure

```
.
├── docs/                    # Book content source files (MDX)
│   ├── intro.mdx            # Introduction chapter
│   └── ...                  # Additional chapters
├── specs/                   # Specifications for each chapter/section
│   ├── 001-introduction/    # Spec files for introduction
│   │   ├── spec.md
│   │   └── plan.md
│   └── ...                  # Additional chapter specs
├── src/                     # Custom React components for the book
├── static/                  # Static assets (images, files)
├── .github/workflows/       # GitHub Actions CI/CD workflows
├── docusaurus.config.js     # Docusaurus configuration
├── sidebars.js              # Navigation sidebar configuration
└── CLAUDE.md                # Claude interactions documentation
```

## Development Workflow

1. Create a specification for your chapter in `specs/XXX-chapter-name/spec.md`
2. Create an implementation plan in `specs/XXX-chapter-name/plan.md`
3. Create the chapter content in `docs/` using MDX
4. Validate your content with `npm run lint` and `npm run validate-links`
5. Test locally with `npm run start`
6. Build with `npm run build`

## Deployment

The site is automatically deployed to GitHub Pages via GitHub Actions when changes are pushed to the main branch.

## AI Collaboration Guidelines

This project follows AI collaboration principles:
- AI tools are used as collaborative agents, not black boxes
- All AI interactions are documented in `CLAUDE.md`
- Human oversight is maintained throughout the process
- Every edit must be traceable via Git commits

## Success Criteria

✅ Book is fully built with Docusaurus v3 (responsive, i18n-ready, dark/light mode)
✅ Every chapter originates from a validated spec (`specs/XXX-*/spec.md`) and implementation plan (`plan.md`)
✅ All content passes automated checks: `npm run build` succeeds, `lychee` reports 0 broken links, ESLint/Prettier clean
✅ Deployment to GitHub Pages succeeds automatically via GitHub Actions
✅ Human-readable `CLAUDE.md` artifact exists, documenting every interaction
✅ Final artifact includes: book site, source repo, spec artifacts, and audit trail# Hackathon-project-1
