from unittest.mock import MagicMock

import pytest
from gpiozero import Device

from pi_logic import motor_logic
from pi_logic.motor_logic import SprayerBusyError, cycle_sprayer_manually, cycle_sprayer_motor
from pi_logic.spray_log import last_spray
from pi_logic.thermostat_logic import ThermostatError


@pytest.fixture
def sleeps(monkeypatch):
    """Skip real delays and record the requested durations."""
    recorded = []
    monkeypatch.setattr(motor_logic, "sleep", recorded.append)
    return recorded


@pytest.fixture
def thermostat(monkeypatch):
    fake = MagicMock()
    monkeypatch.setattr(motor_logic, "get_thermostat", lambda: fake)
    return fake


@pytest.fixture
def motor_speeds(monkeypatch, sleeps):
    """Record the value of the motor at each delay, using the mock GPIO pins."""
    speeds = []
    real_motor = motor_logic.Motor

    def spying_motor(**kwargs):
        motor = real_motor(**kwargs)
        monkeypatch.setattr(
            motor_logic,
            "sleep",
            lambda seconds: (sleeps.append(seconds), speeds.append(motor.value)),
        )
        return motor

    monkeypatch.setattr(motor_logic, "Motor", spying_motor)
    return speeds


def test_each_spray_presses_then_releases_then_stops(motor_speeds):
    cycle_sprayer_motor(num_sprays=2)

    assert motor_speeds == [0.4, -0.3, 0, 0.4, -0.3, 0]


def test_motor_uses_the_wired_pins_and_releases_them(sleeps):
    Device.pin_factory.reset()

    cycle_sprayer_motor(num_sprays=1)

    assert {info.name for info in Device.pin_factory.pins} == {"GPIO23", "GPIO24", "GPIO12"}
    # Reopening raises GPIOPinInUse if the previous cycle kept hold of the pins.
    cycle_sprayer_motor(num_sprays=1)


def test_motor_cycle_records_the_spray(sleeps):
    assert last_spray() is None

    cycle_sprayer_motor(num_sprays=1)

    assert last_spray() is not None


def test_manual_spray_starts_the_fan_and_waits_before_spraying(sleeps, thermostat):
    cycle_sprayer_manually(num_sprays=1)

    thermostat.run_fan.assert_called_once_with()
    assert sleeps[0] == motor_logic.FAN_SPIN_UP_SECONDS
    assert last_spray() is not None


def test_manual_spray_does_not_spray_if_the_fan_fails(sleeps, thermostat):
    thermostat.run_fan.side_effect = ThermostatError("unreachable")

    with pytest.raises(ThermostatError):
        cycle_sprayer_manually()

    assert sleeps == []
    assert last_spray() is None


def test_sprayer_cannot_be_claimed_twice(sleeps):
    with motor_logic._exclusive_sprayer():
        with pytest.raises(SprayerBusyError):
            cycle_sprayer_motor()

    assert last_spray() is None


def test_sprayer_is_available_again_after_a_failure(sleeps, thermostat):
    thermostat.run_fan.side_effect = [ThermostatError("unreachable"), None]

    with pytest.raises(ThermostatError):
        cycle_sprayer_manually(num_sprays=1)
    cycle_sprayer_manually(num_sprays=1)

    assert last_spray() is not None
