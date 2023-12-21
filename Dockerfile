FROM python:3.11

RUN apt install -y unzip

# Set the working directory to /app
WORKDIR /app

RUN python3 -m pip install poetry

# start installing things with poetry
RUN poetry config virtualenvs.create false

COPY ./poetry.lock ./poetry.toml ./pyproject.toml /app

RUN poetry add jupyter 

# Install project dependencies
RUN poetry install

COPY ./data.zip /app

COPY ./fmda_scamper_compare /app/fmda_scamper_compare

COPY ./notebook.ipynb /app

# Expose the port the app runs on
EXPOSE 8080

# Run Jupyter notebook on container startup
CMD ["poetry", "run", "jupyter", "notebook", "--ip='*'", "--port=8080", "--no-browser", "--allow-root"]

