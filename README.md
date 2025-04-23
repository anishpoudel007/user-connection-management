# User Connection Management
This project helps to connect to different users.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/anishpoudel007/user-connection-management.git
cd user-connection-management
```

### 2. Copy env.example to .env file and make necessary changes

```bash
cp env.example .env
```

For development

```bash
DJANGO_SETTINGS_MODULE=project.settings.development
```

For production

```bash
DJANGO_SETTINGS_MODULE=project.settings.production
```


### 3. Build and run with Docker

```bash
docker compose up --build
```

This will:
- Build the Docker image
- Start the Django server at http://localhost:8000


### For Local Development:

You can start local development without docker.

1. Setup uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Initialize your environment

```bash
uv venv
```

This creates a virtual environment in .venv/ (by default).

Activate it:

```bash
source .venv/bin/activate
```

3. Install packages

```bash
uv pip install -r pyproject.toml
```

4. Run

```bash
uv run manage.py runserver
```


### Note:

I have attached the postman collection in the repo.
