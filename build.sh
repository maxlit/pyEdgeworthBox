#!/bin/bash

# Fetch all tags and ensure they are up to date
git fetch --tags

# Get the latest tag
VERSION=$(git tag --sort=-creatordate | head -n 1)

# Update the version in pyproject.toml
poetry version $VERSION

# Now run poetry build
poetry build
