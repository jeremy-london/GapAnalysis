# GapAnalysis Dev Container

This folder contains a development container configuration for the GapAnalysis project. The devcontainer is configured to provide a consistent development environment using Docker and Visual Studio Code.

## Setup

### Prerequisites

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
