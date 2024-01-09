# Use the new base image from quay.io
FROM quay.io/jupyter/minimal-notebook

# Set the working directory in the container to /app
WORKDIR /app

# Copy the pyproject.toml and poetry.lock (if exists) files into the container at /app
COPY pyproject.toml poetry.lock* /app/

# Install poetry in the container
RUN pip install --progress-bar off poetry==1.4.2

# Disable virtualenv creation by poetry, as it's not needed in Docker
RUN poetry config virtualenvs.create false

# Install dependencies using poetry
RUN poetry install --only main

# Copy the contents of the pyEdgeworthBox repository into the container
COPY . /app/

# Continue with any other commands you need
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token="]