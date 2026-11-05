import pytest

from pi_logic.config import ConfigError, NestCredentials

VALUES = {
    "NEST_CLIENT_ID": "client-id",
    "NEST_CLIENT_SECRET": "client-secret",
    "NEST_REFRESH_TOKEN": "refresh-token",
    "NEST_PROJECT_ID": "project-id",
    "NEST_DEVICE_ID": "device-id",
}


def test_from_env_reads_every_setting(monkeypatch):
    for name, value in VALUES.items():
        monkeypatch.setenv(name, value)

    assert NestCredentials.from_env() == NestCredentials(
        client_id="client-id",
        client_secret="client-secret",
        refresh_token="refresh-token",
        project_id="project-id",
        device_id="device-id",
    )


def test_from_env_names_missing_settings(monkeypatch):
    for name, value in VALUES.items():
        monkeypatch.setenv(name, value)
    monkeypatch.delenv("NEST_CLIENT_SECRET")
    monkeypatch.setenv("NEST_DEVICE_ID", "")

    with pytest.raises(ConfigError) as error:
        NestCredentials.from_env()

    assert "NEST_CLIENT_SECRET" in str(error.value)
    assert "NEST_DEVICE_ID" in str(error.value)
    assert "NEST_PROJECT_ID" not in str(error.value)


def test_repr_hides_secrets():
    credentials = NestCredentials("id", "secret-value", "refresh-value", "project", "device")

    assert "secret-value" not in repr(credentials)
    assert "refresh-value" not in repr(credentials)
