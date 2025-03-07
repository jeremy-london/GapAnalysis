# Use an official Python runtime as a parent image
FROM python:3.11-bookworm

SHELL ["/bin/bash", "-c"]

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
RUN . ~/.nvm/nvm.sh && nvm install 22

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY pyproject.toml ./

# Install any needed packages specified in requirements.txt
RUN pip install poetry
RUN poetry install --no-root --all-extras --with dev

# Make port 8000 available to the world outside this container
EXPOSE 8000

# CMD sleep infinity
CMD ["sleep", "infinity"]