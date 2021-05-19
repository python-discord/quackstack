# quackstack

An on-demand procedural ducky delivery service. An infinite stack of duckies!

## Server Setup

### Poetry

1. Install Poetry with `pip install poetry`
2. Install the dependencies with Poetry: `poetry install`
3. Run the server: `poetry run uvicorn main:app --host 127.0.0.1 --port 8077`

### Docker Compose

#### Linux

`sudo docker-compose up`

#### Windows

`docker-compose up`
