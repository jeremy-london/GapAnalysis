# Gap Analysis

A hackathon demo for finding gaps in coporate anit-phising processes.

## Setup

1. Setup your `.env` see steps below
1. Have docker engine running on your system
1. In this directory `docker compose -f .devcontainer/docker-compose.yml up -d`
1. Go to `localhost:8000` to access the API

### Env

Make a file in this directory called .env then write this in it with the env variables you get from Open AI / Arango respectively.

````env
OPENAI_API_KEY=<key>
ENV=development
````

## Important API Endpoints

TBD

## GapAnalysis Dev Container

This folder contains a development container configuration for the GapAnalysis project. The devcontainer is configured to provide a consistent development environment using Docker and Visual Studio Code.

### Setup

#### Prerequisites

1. **Docker**: Ensure Docker is installed and running on your system.
2. **Visual Studio Code**: Install Visual Studio Code.
3. **Remote - Containers Extension**: Install the Remote - Containers extension in Visual Studio Code.

### Steps to Launch the Dev Container

1. **Clone the Repository**: Clone this repository to your local machine.

```sh
git clone <repository-url>
cd <repository-directory>
```

1. **Open in VS Code**: Open the repository in Visual Studio Code.

```sh
code .
```

1. **Open the Dev Container**: Press `F1` or `CMD/Ctrl` + `Shift` + `P` to open the command palette, then type and select `Remote-Containers: Reopen in Container`. This will build and start the devcontainer defined in `.devcontainer/devcontainer.json`.

### Environment Variables

Create a `.env` file in the root directory of the project and add the necessary environment variables:

```env
OPENAI_API_KEY=<your_openai_api_key>
ENV=development
```

### Running Services

Go to Run and Debug section in VSCode to Launch the services

- `Run Uvicorn`: Launches the FastAPI server

>Alternatively you can run `poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload` in the integrated terminal
