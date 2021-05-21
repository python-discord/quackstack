# quackstack

An on-demand procedural ducky delivery service. An infinite stack of duckies!

## Server Setup

### Poetry

1. Install Poetry with `pip install poetry`
2. Install the dependencies with Poetry: `poetry install`
3. Run the server: `poetry run uvicorn main:app --host 127.0.0.1 --port 8077`

Note: to run the server for development you can use `poetry run task start-dev` which will start the server on port 8000.

### Docker Compose

#### Linux

`sudo docker-compose up`

#### Windows

`docker-compose up`
