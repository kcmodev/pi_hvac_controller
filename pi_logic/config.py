"""Runtime configuration, read from the environment and an optional ``.env`` file."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")


class ConfigError(RuntimeError):
    """A required setting is missing."""


@dataclass(frozen=True)
class NestCredentials:
    """OAuth client and device identifiers for the Smart Device Management API."""

    client_id: str
    client_secret: str = field(repr=False)
    refresh_token: str = field(repr=False)
    project_id: str
    device_id: str

    @classmethod
    def from_env(cls) -> NestCredentials:
        """Build credentials from ``NEST_*`` variables, naming any that are missing."""
        names = {
            "client_id": "NEST_CLIENT_ID",
            "client_secret": "NEST_CLIENT_SECRET",
            "refresh_token": "NEST_REFRESH_TOKEN",
            "project_id": "NEST_PROJECT_ID",
            "device_id": "NEST_DEVICE_ID",
        }
        missing = [env_name for env_name in names.values() if not os.environ.get(env_name)]
        if missing:
            raise ConfigError(f"Missing environment variables: {', '.join(missing)}")
        return cls(**{field_name: os.environ[env] for field_name, env in names.items()})
