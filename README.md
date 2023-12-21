# FMDA / Scamper comparison

## Run with docker

```bash
docker build -t fmda_scamper_compare
```

```bash
docker run -p 8080:8080 fmda_scamper_compare
```

## Installation (dev)

```sh
poetry install
```

## Add to jupyter kernels (optional)

```sh
poetry run python -m ipykernel install --user
```