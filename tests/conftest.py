import os

import pytest

# Simulate the GPIO pins so the suite runs without a Raspberry Pi. These must be
# set before gpiozero creates its pin factory.
os.environ["GPIOZERO_PIN_FACTORY"] = "mock"
os.environ["GPIOZERO_MOCK_PIN_CLASS"] = "mockpwmpin"


@pytest.fixture(autouse=True)
def isolated_spray_db(tmp_path, monkeypatch):
    """Keep every test away from the real spray history."""
    monkeypatch.setenv("SPRAY_DB_PATH", str(tmp_path / "db.json"))
