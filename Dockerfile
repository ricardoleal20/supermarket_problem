# Get the Python 3.11 for this
FROM python:3.11-slim
WORKDIR /app

# Get node JS
RUN apt-get update && \
    apt-get install -y curl gnupg build-essential unzip && \
    curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Get the environment for this
ENV PYTHONNUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV POETRY_VERSION=1.5.1

# Install the system dependencies and install poetry
RUN apt-get update && \
    apt-get install -y build-essential && \
    pip install --upgrade pip && \
    pip install poetry

# Copy the pyproject.toml
COPY pyproject.toml poetry.lock* /app/

# With poetry, install everything
RUN poetry lock && poetry install --no-interaction --no-ansi --no-root

# Copy everything of the code
COPY . /app/

# Add the command to run
CMD ["poetry", "run", "reflex", "run", "--env", "prod"]
