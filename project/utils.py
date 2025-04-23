import os
from pathlib import Path


def load_env_file(env_path=None):
    if env_path is None:
        env_path = Path(__file__).resolve().parent.parent / ".env"

    if not os.path.exists(env_path):
        return

    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())
