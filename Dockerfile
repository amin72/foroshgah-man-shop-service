FROM python:3.12-slim

WORKDIR /app

# Copy only dependency files first
COPY pyproject.toml poetry.lock /app/

# Install poetry and dependencies without creating a virtual environment
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the application files
COPY . .

EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh"]
