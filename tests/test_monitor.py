from datetime import datetime
from unittest.mock import MagicMock

import pytest

import main
from pi_logic.config import ConfigError
from pi_logic.motor_logic import SprayerBusyError
from pi_logic.thermostat_logic import ThermostatError

DAYTIME = datetime(2022, 7, 1, 12, 0)


@pytest.fixture
def thermostat(monkeypatch):
    fake = MagicMock()
    monkeypatch.setattr(main, "get_thermostat", lambda: fake)
    return fake


@pytest.fixture
def sprayer(monkeypatch):
    fake = MagicMock()
    monkeypatch.setattr(main, "cycle_sprayer_motor", fake)
    return fake


@pytest.mark.parametrize("status", ["COOLING", "HEATING"])
def test_active_hvac_sprays_and_starts_the_cooldown(thermostat, sprayer, status):
    thermostat.get_hvac_status.return_value = status

    assert main.check_hvac_status(DAYTIME) == main.SPRAY_COOLDOWN_SECONDS
    sprayer.assert_called_once_with()


def test_idle_hvac_polls_again_without_spraying(thermostat, sprayer):
    thermostat.get_hvac_status.return_value = "OFF"

    assert main.check_hvac_status(DAYTIME) == main.IDLE_POLL_SECONDS
    sprayer.assert_not_called()


@pytest.mark.parametrize(
    ("hour", "minute", "checks_thermostat"),
    [(7, 59, False), (8, 0, True), (21, 59, True), (22, 0, False), (0, 0, False)],
)
def test_thermostat_is_only_checked_during_active_hours(
    thermostat, sprayer, hour, minute, checks_thermostat
):
    thermostat.get_hvac_status.return_value = "OFF"

    main.check_hvac_status(datetime(2022, 7, 1, hour, minute))

    assert thermostat.get_hvac_status.called is checks_thermostat


def test_thermostat_failure_retries_without_spraying(thermostat, sprayer):
    thermostat.get_hvac_status.side_effect = ThermostatError("unreachable")

    assert main.check_hvac_status(DAYTIME) == main.IDLE_POLL_SECONDS
    sprayer.assert_not_called()


def test_busy_sprayer_skips_the_cooldown(thermostat, sprayer):
    thermostat.get_hvac_status.return_value = "COOLING"
    sprayer.side_effect = SprayerBusyError

    assert main.check_hvac_status(DAYTIME) == main.IDLE_POLL_SECONDS


def test_missing_configuration_exits_with_an_error(monkeypatch):
    monkeypatch.setattr(main, "get_thermostat", MagicMock(side_effect=ConfigError("Missing")))

    assert main.main() == 1


def test_interrupt_stops_the_loop_cleanly(monkeypatch, thermostat, sprayer):
    thermostat.get_hvac_status.return_value = "OFF"
    monkeypatch.setattr(main, "sleep", MagicMock(side_effect=KeyboardInterrupt))

    assert main.main() == 0
