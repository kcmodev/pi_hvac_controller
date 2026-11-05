"""Drives the motor that presses the air freshener can."""

from __future__ import annotations

import fcntl
import logging
from collections.abc import Iterator
from contextlib import contextmanager
from time import sleep

from gpiozero import Motor

from pi_logic.config import spray_db_path
from pi_logic.spray_log import record_spray
from pi_logic.thermostat_logic import get_thermostat

logger = logging.getLogger(__name__)

# BCM pin numbers for the motor driver
FORWARD_PIN = 23
BACKWARD_PIN = 24
ENABLE_PIN = 12

SPRAYS_PER_CYCLE = 2
PRESS_SPEED = 0.4
PRESS_SECONDS = 0.6
RELEASE_SPEED = 0.3
RELEASE_SECONDS = 0.3
SECONDS_BETWEEN_SPRAYS = 1

# Gives the fan time to get air moving through the filter before spraying onto it
FAN_SPIN_UP_SECONDS = 10


class SprayerBusyError(RuntimeError):
    """Another thread or process is already using the sprayer."""


@contextmanager
def _exclusive_sprayer() -> Iterator[None]:
    """Claim the sprayer across processes, since the web app and monitor both drive it."""
    with open(spray_db_path().with_suffix(".lock"), "w") as lock_file:
        try:
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise SprayerBusyError("The sprayer is already running") from error
        yield  # Closing the file releases the lock


def _run_motor(num_sprays: int) -> None:
    # The pins are held only while spraying, so the other process can open them next.
    with Motor(forward=FORWARD_PIN, backward=BACKWARD_PIN, enable=ENABLE_PIN, pwm=True) as motor:
        for spray in range(1, num_sprays + 1):
            logger.info("Spray %d of %d", spray, num_sprays)
            motor.forward(speed=PRESS_SPEED)
            sleep(PRESS_SECONDS)
            motor.backward(speed=RELEASE_SPEED)
            sleep(RELEASE_SECONDS)
            motor.stop()
            sleep(SECONDS_BETWEEN_SPRAYS)
    record_spray()


def cycle_sprayer_motor(num_sprays: int = SPRAYS_PER_CYCLE) -> None:
    """Spray while the HVAC system is already moving air."""
    with _exclusive_sprayer():
        _run_motor(num_sprays)


def cycle_sprayer_manually(num_sprays: int = SPRAYS_PER_CYCLE) -> None:
    """Start the fan, then spray once it is moving air."""
    with _exclusive_sprayer():
        logger.info("Manual spray requested, starting the fan")
        get_thermostat().run_fan()
        sleep(FAN_SPIN_UP_SECONDS)
        _run_motor(num_sprays)
