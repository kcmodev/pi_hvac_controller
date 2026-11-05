import pytest


@pytest.fixture(autouse=True)
def isolated_spray_db(tmp_path, monkeypatch):
    """Keep every test away from the real spray history."""
    monkeypatch.setenv("SPRAY_DB_PATH", str(tmp_path / "db.json"))
