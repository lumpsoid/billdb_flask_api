# Use the official Python image as a parent image
FROM python:3.11-slim

# Update package lists and install git
RUN apt-get update \
    && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

COPY ./requirements.txt /app/
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# server
RUN touch README.md
RUN touch bills.db
COPY ./billdb_flask_api /app/billdb_flask_api
COPY ./gunicorn_config.py /app/

# Expose a port if your Flask app listens on one gunicorn_config.py
EXPOSE 5001
# Run your Flask app using Gunicorn with the specified configuration
CMD [ "gunicorn", "--config", "gunicorn_config.py", "billdb_flask_api.app:create_app()"]

