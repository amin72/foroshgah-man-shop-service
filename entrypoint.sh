# Clear Python caches
find . -name "*.pyc" -exec rm -f {} \;

# Apply migrations
poetry run aerich upgrade

exec "$@"
