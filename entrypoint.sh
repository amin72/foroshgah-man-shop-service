# Clear Python caches
find . -name "*.pyc" -exec rm -f {} \;

# Init database
echo "\nInitializing database...\n"
poetry run aerich init -t app.core.config.TORTOISE_ORM 

# Apply migrations
echo "\nApplying migrations...\n"
poetry run aerich upgrade

# Run consumer
echo "\nRunning consumer...\n"
python app/consumer.py &

if [ "$DEBUG" = True ]; then
  # Development command
  echo "\nRunning in development mode...\n"
  poetry run fastapi dev --host 0.0.0.0 --port 8000
else
  # Production command
  echo "\nRunning in production mode...\n"
  poetry run fastapi run --host 0.0.0.0 --port 8000
fi

exec "$@"
