# README

## Installation instructions

### MacOS

- This project uses Poetry. To install Poetry do the following
  - Make sure you have `brew` installed
  - Start a terminal
  - Install poetry using `brew install poetry`

## Running the application

- Start a terminal
- Navigate to the `flask-recipe-app` directory
- Install the packages using `poetry install`
- Then run `poetry run flask run`
- Note: You need a local Postgres database instance running

### First Migration

- You need a postgres server up and running with the right credentials. The fastest way is to run the Docker postgres database
- Run the first migration with `poetry run flask db upgrade` or `docker run --rm -it  poetry run flask db upgrade`
  - Subsequent migrations after models changes can be run with `poetry run flask db migrate -m "subsequent migrations"`.

## Working with Docker

- To run the applcation, from the root directory just type `docker-compose up`
- To run tests, run `docker run --rm -it flask-recipe-app poetry run pytest`
