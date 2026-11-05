import json

import pytest
import requests
import responses

from pi_logic.config import NestCredentials
from pi_logic.thermostat_logic import (
    HVAC_TRAIT,
    OAUTH_URL,
    SDM_BASE_URL,
    NestThermostat,
    ThermostatError,
)

DEVICE_URL = f"{SDM_BASE_URL}/enterprises/project/devices/device"
COOLING = {"traits": {HVAC_TRAIT: {"status": "COOLING"}}}


@pytest.fixture
def thermostat():
    return NestThermostat(NestCredentials("id", "secret", "refresh", "project", "device"))


@pytest.fixture
def api():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as mock:
        yield mock


def add_token(api, token="token-1"):
    api.post(OAUTH_URL, json={"access_token": token, "token_type": "Bearer"})


def calls_to(api, url):
    return [call for call in api.calls if call.request.url == url]


def test_status_fetches_a_token_then_reads_the_trait(api, thermostat):
    add_token(api)
    api.get(DEVICE_URL, json=COOLING)

    assert thermostat.get_hvac_status() == "COOLING"
    assert api.calls[-1].request.headers["Authorization"] == "Bearer token-1"


def test_token_is_reused_between_requests(api, thermostat):
    add_token(api)
    api.get(DEVICE_URL, json=COOLING)

    thermostat.get_hvac_status()
    thermostat.get_hvac_status()

    assert len(calls_to(api, OAUTH_URL)) == 1


def test_expired_token_is_refreshed_and_the_request_retried(api, thermostat):
    add_token(api, "stale")
    add_token(api, "fresh")
    api.get(DEVICE_URL, status=401, json={"error": {"status": "UNAUTHENTICATED"}})
    api.get(DEVICE_URL, json=COOLING)

    assert thermostat.get_hvac_status() == "COOLING"
    assert api.calls[-1].request.headers["Authorization"] == "Bearer fresh"


def test_repeated_unauthorized_gives_up_instead_of_looping(api, thermostat):
    add_token(api)
    api.get(DEVICE_URL, status=401, json={})

    with pytest.raises(ThermostatError, match="401"):
        thermostat.get_hvac_status()

    assert len(calls_to(api, DEVICE_URL)) == 2


def test_api_error_raises_rather_than_returning_a_status(api, thermostat):
    add_token(api)
    api.get(DEVICE_URL, json=COOLING)
    api.get(DEVICE_URL, status=503, json={"error": {"status": "UNAVAILABLE"}})

    assert thermostat.get_hvac_status() == "COOLING"
    with pytest.raises(ThermostatError, match="503"):
        thermostat.get_hvac_status()


def test_network_failure_raises_thermostat_error(api, thermostat):
    add_token(api)
    api.get(DEVICE_URL, body=requests.ConnectionError("no route to host"))

    with pytest.raises(ThermostatError, match="no route to host"):
        thermostat.get_hvac_status()


@pytest.mark.parametrize("body", [{}, {"traits": {}}, {"traits": None}])
def test_response_without_the_hvac_trait_raises(api, thermostat, body):
    add_token(api)
    api.get(DEVICE_URL, json=body)

    with pytest.raises(ThermostatError, match="no HVAC status"):
        thermostat.get_hvac_status()


def test_non_json_response_raises(api, thermostat):
    add_token(api)
    api.get(DEVICE_URL, body="<html>bad gateway</html>")

    with pytest.raises(ThermostatError, match="not valid JSON"):
        thermostat.get_hvac_status()


def test_failed_token_refresh_raises(api, thermostat):
    api.post(OAUTH_URL, status=400, json={"error": "invalid_grant"})

    with pytest.raises(ThermostatError, match="Token refresh failed with HTTP 400"):
        thermostat.get_hvac_status()


def test_network_failure_during_refresh_does_not_expose_the_request(api, thermostat):
    api.post(OAUTH_URL, body=requests.ConnectionError("client_secret=secret"))

    with pytest.raises(ThermostatError) as error:
        thermostat.get_hvac_status()

    assert "secret" not in str(error.value)


def test_run_fan_sends_a_json_set_timer_command(api, thermostat):
    add_token(api)
    api.post(f"{DEVICE_URL}:executeCommand", json={})

    thermostat.run_fan(duration_seconds=60)

    assert json.loads(api.calls[-1].request.body) == {
        "command": "sdm.devices.commands.Fan.SetTimer",
        "params": {"timerMode": "ON", "duration": "60s"},
    }


def test_run_fan_raises_when_the_command_is_rejected(api, thermostat):
    add_token(api)
    api.post(f"{DEVICE_URL}:executeCommand", status=400, json={})

    with pytest.raises(ThermostatError, match="400"):
        thermostat.run_fan()
