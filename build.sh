VERSION=$(git tag --sort=-creatordate | head -n 1)
poetry version $VERSION
poetry build
