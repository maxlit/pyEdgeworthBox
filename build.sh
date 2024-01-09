VERSION=$(git describe --tags $(git rev-list --tags --max-count=1))
poetry version $VERSION
poetry build
