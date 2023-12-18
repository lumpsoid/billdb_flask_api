# Use the official Python image as a parent image
FROM python:3.11-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

RUN python3 -m pip install poetry==1.7.1

# Set the working directory in the container
WORKDIR /app

# server
RUN touch README.md
COPY ./billdb_flask_api /app/billdb_flask_api
COPY ./poetry.lock ./pyproject.toml ./gunicorn_config.py /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

# Expose a port if your Flask app listens on one gunicorn_config.py
EXPOSE 5001

# Run your Flask app using Gunicorn with the specified configuration
CMD [ "poetry", "run", "gunicorn", "--config", "gunicorn_config.py", "billdb_flask_api.app:app"]

