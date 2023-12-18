# Use the official Python image as a parent image
FROM python:alpine3.19

# Add ~/.local/bin to PATH
# RUN echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.profile
# RUN source ~/.profile

RUN python3 -m pip install --user pipx
RUN /root/.local/bin/pipx install poetry==1.2.0

# Set the working directory in the container
WORKDIR /app

# server
RUN touch README.md
COPY ./billdb_flask_api /app/billdb_flask_api
COPY ./pyproject.toml /app/pyproject.toml
COPY ./gunicorn_config.py /app/gunicorn_config.py

RUN /root/.local/bin/poetry install

# Expose a port if your Flask app listens on one gunicorn_config.py
EXPOSE 5001

# Run your Flask app using Gunicorn with the specified configuration
CMD [ "/root/.local/bin/poetry", "run", "gunicorn", "--config", "gunicorn_config.py", "billdb_flask_api.app:app"]

