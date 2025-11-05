#!/bin/bash
# Setup script for Nova Corrente Git Workflow

echo "==================================="
echo "Nova Corrente Git Setup"
echo "==================================="

# Check if in git repository
if [ ! -d ".git" ]; then
    echo "Error: Not in a git repository"
    exit 1
fi

echo "Setting up Git workflow for Nova Corrente project..."

# Configure git user.name and user.email if not set
if [ -z "$(git config user.name)" ]; then
    read -p "Enter your name for Git commits: " git_name
    git config user.name "$git_name"
fi

if [ -z "$(git config user.email)" ]; then
    read -p "Enter your email for Git commits: " git_email
    git config user.email "$git_email"
fi

# Set up branch protection and workflow
echo "Setting up branch structure..."

# Create main branch if it doesn't exist
if ! git show-ref --verify --quiet refs/heads/main; then
    git checkout -b main
    echo "Created main branch"
else
    echo "Main branch already exists"
fi

# Create develop branch if it doesn't exist
if ! git show-ref --verify --quiet refs/heads/develop; then
    git checkout -b develop
    echo "Created develop branch"
else
    echo "Develop branch already exists"
fi

# Configure git settings from .gitconfig
echo "Applying Git configurations..."
git config core.autocrlf true
git config push.default current
git config pull.rebase true

# Install pre-commit hooks (if pre-commit is available)
if command -v pre-commit &> /dev/null; then
    echo "Installing pre-commit hooks..."
    pre-commit install
else
    echo "Pre-commit not found. Install with: pip install pre-commit"
fi

# Set up remote origin if not set
if [ -z "$(git remote)" ]; then
    read -p "Enter remote repository URL: " remote_url
    git remote add origin "$remote_url"
    echo "Added remote origin: $remote_url"
else
    echo "Remote origin already configured"
fi

# Push initial branches
echo "Pushing initial branches..."
git push -u origin main
git push -u origin develop

echo "==================================="
echo "Git workflow setup completed!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Create feature branches from 'develop':"
echo "   git checkout develop && git pull origin develop"
echo "   git checkout -b feature/name-of-feature"
echo ""
echo "2. Follow the workflow documented in docs/GIT_WORKFLOW.md"
echo "3. Use conventional commit messages"
echo "4. Run tests before pushing"
echo ""
echo "Available git aliases:"
echo "   git st   - git status"
echo "   git co   - git checkout"
echo "   git br   - git branch"
echo "   git cm   - git commit -m"
echo "   git tree - git log --oneline --graph --all"
echo ""