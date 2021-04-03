FROM python:3.8

RUN apt update && apt install -y git

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml /app/pyproject.toml

RUN poetry install

COPY . /app

RUN git submodule update --init

CMD ["poetry", "run", "hypercorn", "main:app", "--bind", "0.0.0.0:80"]
