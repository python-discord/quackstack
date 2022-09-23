FROM --platform=linux/amd64 ghcr.io/chrislovering/python-poetry-base:3.10-slim

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev

COPY . .

ENTRYPOINT ["poetry"]
CMD ["run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
