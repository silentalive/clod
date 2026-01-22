#!/bin/bash
# Helper script to create a new release

echo "======================================"
echo "Mouse Tracker - Release Creator"
echo "======================================"
echo

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not in a git repository!"
    exit 1
fi

# Get current version from git tags
CURRENT_VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
echo "Current version: $CURRENT_VERSION"
echo

# Ask for new version
echo "Enter new version (e.g., v1.0.0, v1.1.0):"
read NEW_VERSION

# Validate version format
if [[ ! $NEW_VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Version must be in format v1.0.0"
    exit 1
fi

echo
echo "Creating release $NEW_VERSION..."
echo

# Make sure we're on the right branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

if [[ "$CURRENT_BRANCH" != "main" ]] && [[ "$CURRENT_BRANCH" != "master" ]]; then
    echo "Warning: You're not on main/master branch!"
    echo "Continue anyway? (y/n)"
    read CONTINUE
    if [[ "$CONTINUE" != "y" ]]; then
        echo "Cancelled."
        exit 0
    fi
fi

# Create and push tag
echo
echo "Creating git tag..."
git tag -a "$NEW_VERSION" -m "Release $NEW_VERSION"

echo "Pushing tag to remote..."
git push origin "$NEW_VERSION"

echo
echo "======================================"
echo "✓ Release $NEW_VERSION created!"
echo "======================================"
echo
echo "GitHub Actions will now:"
echo "  1. Build executables for Windows, Linux, and macOS"
echo "  2. Create a GitHub Release"
echo "  3. Upload all executables automatically"
echo
echo "Check progress at:"
echo "  https://github.com/$(git config --get remote.origin.url | sed 's/.*:\(.*\)\.git/\1/')/actions"
echo
echo "Release will be available at:"
echo "  https://github.com/$(git config --get remote.origin.url | sed 's/.*:\(.*\)\.git/\1/')/releases"
echo
