"""Client for the Google Smart Device Management (Nest) API."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

import requests

from pi_logic.config import NestCredentials

OAUTH_URL = "https://www.googleapis.com/oauth2/v4/token"
SDM_BASE_URL = "https://smartdevicemanagement.googleapis.com/v1"
HVAC_TRAIT = "sdm.devices.traits.ThermostatHvac"
FAN_COMMAND = "sdm.devices.commands.Fan.SetTimer"

REQUEST_TIMEOUT_SECONDS = 10
FAN_DURATION_SECONDS = 900


class ThermostatError(RuntimeError):
    """The thermostat could not be reached or returned an unusable response."""


class NestThermostat:
    """A single Nest thermostat, refreshing its OAuth access token as needed."""

    def __init__(self, credentials: NestCredentials) -> None:
        self._credentials = credentials
        self._session = requests.Session()
        self._access_token: str | None = None
        self._device_url = (
            f"{SDM_BASE_URL}/enterprises/{credentials.project_id}/devices/{credentials.device_id}"
        )

    def get_hvac_status(self) -> str:
        """Return the current HVAC state: ``HEATING``, ``COOLING`` or ``OFF``."""
        device = self._request("GET", self._device_url)
        try:
            return device["traits"][HVAC_TRAIT]["status"]
        except (KeyError, TypeError) as error:
            raise ThermostatError("Device response has no HVAC status") from error

    def run_fan(self, duration_seconds: int = FAN_DURATION_SECONDS) -> None:
        """Run the HVAC fan on its own for the given duration."""
        self._request(
            "POST",
            f"{self._device_url}:executeCommand",
            json={
                "command": FAN_COMMAND,
                "params": {"timerMode": "ON", "duration": f"{duration_seconds}s"},
            },
        )

    def _request(self, method: str, url: str, **kwargs: Any) -> dict:
        """Send an authorized API request, refreshing an expired token at most once."""
        if self._access_token is None:
            self._refresh_access_token()

        response = self._send(method, url, **kwargs)
        if response.status_code == requests.codes.unauthorized:
            self._refresh_access_token()
            response = self._send(method, url, **kwargs)

        if not response.ok:
            raise ThermostatError(f"Nest API returned HTTP {response.status_code}")
        return self._parse_json(response)

    def _send(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        headers = {"Authorization": f"Bearer {self._access_token}"}
        try:
            return self._session.request(
                method, url, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS, **kwargs
            )
        except requests.RequestException as error:
            raise ThermostatError(f"Could not reach the Nest API: {error}") from error

    def _refresh_access_token(self) -> None:
        try:
            response = self._session.post(
                OAUTH_URL,
                data={
                    "client_id": self._credentials.client_id,
                    "client_secret": self._credentials.client_secret,
                    "refresh_token": self._credentials.refresh_token,
                    "grant_type": "refresh_token",
                },
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
        except requests.RequestException as error:
            # Only the type: the exception text can include the request details.
            raise ThermostatError(
                f"Could not reach the OAuth server: {type(error).__name__}"
            ) from None

        if not response.ok:
            raise ThermostatError(f"Token refresh failed with HTTP {response.status_code}")
        try:
            self._access_token = self._parse_json(response)["access_token"]
        except KeyError:
            raise ThermostatError("Token response has no access token") from None

    @staticmethod
    def _parse_json(response: requests.Response) -> dict:
        try:
            return response.json()
        except ValueError as error:
            raise ThermostatError("Response was not valid JSON") from error


@lru_cache(maxsize=1)
def get_thermostat() -> NestThermostat:
    """Return the shared thermostat client, so its access token is reused between calls."""
    return NestThermostat(NestCredentials.from_env())
