FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY poetry.lock pyproject.toml /app/

# Install dependencies without creating a virtual environment
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . .

EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh"]

CMD ["poetry", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]
