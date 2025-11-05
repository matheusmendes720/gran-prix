#!/bin/bash
# Git Workflow Script for Nova Corrente Project

set -e  # Exit on any error

echo "==================================="
echo "Nova Corrente Git Workflow Helper"
echo "==================================="

function create_feature_branch() {
    echo "Creating a new feature branch..."
    read -p "Enter feature name (e.g., user-authentication): " feature_name
    git checkout develop
    git pull origin develop
    git checkout -b "feature/$feature_name"
    echo "Created and switched to branch: feature/$feature_name"
}

function create_bugfix_branch() {
    echo "Creating a new bugfix branch..."
    read -p "Enter bug description (e.g., fix-login-error): " bug_name
    git checkout develop
    git pull origin develop
    git checkout -b "bugfix/$bug_name"
    echo "Created and switched to branch: bugfix/$bug_name"
}

function prepare_release() {
    echo "Creating a new release branch..."
    read -p "Enter release version (e.g., v1.2.0): " release_version
    git checkout develop
    git pull origin develop
    git checkout -b "release/$release_version"
    echo "Created and switched to branch: release/$release_version"
    echo "Remember to update version numbers in package.json, etc."
}

function merge_feature_to_develop() {
    echo "Merging current feature branch to develop..."
    current_branch=$(git branch --show-current)
    
    if [[ $current_branch != feature/* ]]; then
        echo "Error: You must be on a feature branch to merge to develop"
        exit 1
    fi
    
    git checkout develop
    git pull origin develop
    git merge "$current_branch" --no-ff
    echo "Merged $current_branch to develop"
}

function merge_release_to_main() {
    echo "Merging release branch to main..."
    current_branch=$(git branch --show-current)
    
    if [[ $current_branch != release/* ]]; then
        echo "Error: You must be on a release branch to merge to main"
        exit 1
    fi
    
    git checkout main
    git pull origin main
    git merge "$current_branch" --no-ff
    echo "Merged $current_branch to main"
    
    # Create tag
    release_version=$(echo "$current_branch" | sed 's/release\///')
    git tag -a "$release_version" -m "Release $release_version"
    echo "Created tag: $release_version"
}

function setup_project() {
    echo "Setting up project branches..."
    
    # Create main branch if it doesn't exist
    git checkout -b main 2>/dev/null || git checkout main
    
    # Create develop branch if it doesn't exist
    git checkout -b develop 2>/dev/null || git checkout develop
    
    # Set up remote tracking
    git push -u origin main
    git push -u origin develop
    
    echo "Project branches set up successfully!"
}

function show_help() {
    echo "Available commands:"
    echo "  setup          - Initialize project branches"
    echo "  feature        - Create a new feature branch"
    echo "  bugfix         - Create a new bugfix branch"
    echo "  release        - Create a new release branch"
    echo "  merge-feature  - Merge current feature to develop"
    echo "  merge-release  - Merge current release to main"
    echo "  help           - Show this help"
}

if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

case "$1" in
    "setup")
        setup_project
        ;;
    "feature")
        create_feature_branch
        ;;
    "bugfix")
        create_bugfix_branch
        ;;
    "release")
        prepare_release
        ;;
    "merge-feature")
        merge_feature_to_develop
        ;;
    "merge-release")
        merge_release_to_main
        ;;
    "help")
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        exit 1
        ;;
esac