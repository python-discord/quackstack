FROM python:3.8

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml /app/pyproject.toml

RUN poetry install

COPY . /app

CMD ["poetry", "run", "hypercorn", "main:app", "--bind", "0.0.0.0:80"]
