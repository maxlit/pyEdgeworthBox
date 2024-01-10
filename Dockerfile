# Use a specific base image version from quay.io
FROM quay.io/jupyter/minimal-notebook:x86_64-python-3.11.7

# Set the working directory in the container to /app
WORKDIR /app

# Copy the pyproject.toml and poetry.lock (if exists) files into the container at /app
COPY pyproject.toml poetry.lock* /app/

# Install poetry, disable virtualenv creation, and install dependencies in one layer
RUN pip install --progress-bar off poetry==1.7.1 && \
    poetry config virtualenvs.create false
RUN poetry -v install --no-root

# Copy the contents of the pyEdgeworthBox repository into the container
COPY . /app/

#RUN pip install --progress-bar off twine && python setup.py sdist bdist_wheel


# Continue with any other commands you need
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token="]