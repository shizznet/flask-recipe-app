# Use an official Python runtime as a parent image
FROM python:3.10.13-slim-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

COPY pyproject.toml poetry.lock* ./

# Install Poetry and Disable virtualenv creation by Poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev

# Now copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the app
CMD ["flask", "run", "--host=0.0.0.0"]
