FROM python:3.9

RUN apt update && apt install -y git

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml /app/pyproject.toml

RUN poetry install --no-dev

COPY . /app

CMD ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
