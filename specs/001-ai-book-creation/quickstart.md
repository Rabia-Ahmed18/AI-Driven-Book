# Quickstart Guide: AI/Spec-Driven Book Creation

Updated: December 9, 2025

## Overview

This guide will help you quickly set up and start using the AI/Spec-Driven Book Creation system. Follow these steps to create your first technical book with Docusaurus v3.

## Prerequisites

- Node.js 18 or higher
- npm or yarn package manager
- Git
- GitHub account (for deployment to GitHub Pages)

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Initialize Docusaurus

```bash
npx create-docusaurus@latest website classic
```

## Creating Your First Book

### 1. Define Your Book's Specification

Create a specification file in `specs/[###-feature-name]/spec.md` that defines your book's purpose, audience, and requirements.

Example:
```
# Feature Specification: [Your Book Title]

## User Scenarios & Testing

### User Story 1 - [Define your main user goal]

As a [user type], I want [goal] so that [benefit].

**Acceptance Scenarios**:
1. **Given** [context], **When** [action], **Then** [expected outcome]

## Requirements

### Functional Requirements
- **FR-001**: [Define your requirement]

### Non-Functional Requirements
- **NFR-001**: [Define your non-functional requirement]

## Success Criteria
- **SC-001**: [Define measurable outcome]
```

### 2. Generate Implementation Plan

```bash
/sp.plan
```

This will create an implementation plan in `specs/[###-feature-name]/plan.md` with technical details and research findings.

### 3. Create Task Definitions

```bash
/sp.tasks
```

This generates detailed tasks in `specs/[###-feature-name]/tasks.md` based on your spec.

### 4. Start Implementation

```bash
/sp.implement
```

This begins the AI-assisted implementation process for your book content.

## Project Structure

```
my-book/
├── docs/                 # Book content (organized by chapters)
│   ├── 001-intro/
│   ├── 002-spec-cycle/
│   ├── 003-ai-collaboration/
│   ├── 004-deploy-automate/
│   └── 005-governance/
├── src/
│   ├── components/       # Reusable React components
│   ├── pages/            # Custom pages
│   └── theme/            # Theme customization
├── static/               # Static assets (images, files)
├── specs/                # Specifications and plans
│   └── [###-feature-name]/
│       ├── spec.md
│       ├── plan.md
│       ├── research.md
│       ├── data-model.md
│       ├── contracts/
│       └── tasks.md
├── docusaurus.config.js  # Site configuration
├── sidebars.js           # Navigation sidebar
├── package.json          # Dependencies and scripts
└── .github/
    └── workflows/
        └── deploy.yml    # CI/CD workflow for GitHub Pages
```

## Development Workflow

### 1. Local Development

```bash
npm run start
```

This command starts a local development server and opens your site in a browser. Most changes are reflected live without restarting the server.

### 2. Build for Production

```bash
npm run build
```

This command generates static content into the `build` directory and can be served using any static hosting service.

### 3. Testing

```bash
# Linting
npm run lint

# Link checking
npx lychee build/

# Accessibility testing
npx lighthouse <url> --only-categories=accessibility
```

## Deployment

The site is configured to deploy automatically to GitHub Pages via GitHub Actions.

### 1. Configure GitHub Pages

1. Go to your repository Settings → Pages
2. Select "GitHub Actions" as the source

### 2. Push to Main Branch

When you push changes to the main branch, the GitHub Actions workflow will automatically build and deploy your site.

## Integration with AI Tools

### Claude Code Integration

The project is set up to work with Claude Code for AI-assisted development:

1. Use `/sp.*` commands in Claude to manage your development workflow
2. Claude will create diffs that you can review before applying
3. All changes are tracked in Git for auditability

### CLAUDE.md Log

All interactions with Claude will be automatically logged in the `CLAUDE.md` file, maintaining an audit trail of AI-assisted development.

## Best Practices

### Content Creation
- Organize content by chapters in separate directories
- Use MDX for mixing markdown with React components
- Include frontmatter in each document with metadata
- Follow the specifications defined in your spec.md files

### Quality Assurance
- Run `npm run build` frequently to catch issues early
- Use linting to maintain code quality
- Check for broken links using lychee
- Verify accessibility with Lighthouse audits

### Version Control
- Commit frequently with clear, descriptive messages
- Use feature branches for new content or functionality
- Submit pull requests for review before merging to main

## Troubleshooting

### Build Issues
If you encounter build issues, try:
```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Docusaurus Issues
For Docusaurus-specific issues, check the [official documentation](https://docusaurus.io) or run:
```bash
npx docusaurus doctor
```

### Claude Integration Issues
If Claude Code integration isn't working:
- Ensure the `.specify/scripts/update-claude-md.sh` script exists and is executable
- Verify that Claude has access to the project directory