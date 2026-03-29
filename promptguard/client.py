"""HTTP client for PromptGuard environment."""
import requests
from typing import Optional
from promptguard.models import PromptGuardAction, PromptGuardObservation, PromptGuardState


class PromptGuardEnv:
    """Simple HTTP client for the PromptGuard environment."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def reset(self, task_id: str = "easy") -> dict:
        """Reset environment for a new episode."""
        resp = self.session.post(
            f"{self.base_url}/reset",
            json={"task_id": task_id},
        )
        resp.raise_for_status()
        return resp.json()

    def step(self, action: dict) -> dict:
        """Submit defense configuration and get graded results."""
        resp = self.session.post(
            f"{self.base_url}/step",
            json=action,
        )
        resp.raise_for_status()
        return resp.json()

    def state(self) -> dict:
        """Get current episode state."""
        resp = self.session.get(f"{self.base_url}/state")
        resp.raise_for_status()
        return resp.json()

    def health(self) -> dict:
        """Check server health."""
        resp = self.session.get(f"{self.base_url}/health")
        resp.raise_for_status()
        return resp.json()

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
