# Flask Hello World Application

## Description

This is a simple "Hello, World!" application built with Flask, containerized with Docker, and deployed to a Kubernetes cluster.

## Prerequisites

- Docker
- Kubernetes (Minikube or a cloud provider)
- GitHub Actions for CI/CD

## Steps

1. Clone the repository.
2. Build and run the Docker image locally:
```bash
make
```

## Developing

This is a flask project.

use `pipenv shell` to activate the virtual environment

use `pipenv run` to run the script or docker to build and run

use `pip install pre-commit && pre-commit install` to install the pre-commit git hooks

