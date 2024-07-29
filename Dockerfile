# Get the Python 3.11 for this
FROM python:3.11-slim
FROM node:lts-slim as build
WORKDIR /app

# Get the environment for this
ENV PYTHONNUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV POETRY_VERSION=1.5.1

# Install the system dependencies
RUN apt-get update

# Run and uupdate pip
RUN pip3 install --upgrade pip
# Install poetry
RUN pip3 install poetry
# With poetry, install everything
RUN poetry install --no-interaction --no-ansi --no-root


