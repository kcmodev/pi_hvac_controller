"""Monitors the thermostat and sprays whenever the HVAC system is heating or cooling."""

from __future__ import annotations

import logging
import sys
from datetime import datetime
from time import sleep

from pi_logic.config import ConfigError
from pi_logic.motor_logic import SprayerBusyError, cycle_sprayer_motor
from pi_logic.thermostat_logic import ThermostatError, get_thermostat

logger = logging.getLogger(__name__)

MINUTE = 60
SPRAY_COOLDOWN_SECONDS = 30 * MINUTE
IDLE_POLL_SECONDS = 5 * MINUTE
NIGHT_POLL_SECONDS = 30 * MINUTE

# Automatic sprays run from 08:00 up to, but not including, 22:00
FIRST_ACTIVE_HOUR = 8
END_ACTIVE_HOUR = 22

ACTIVE_HVAC_STATES = {"COOLING", "HEATING"}


def check_hvac_status(now: datetime | None = None) -> int:
    """Spray if the HVAC system is running and return the seconds until the next check."""
    now = now or datetime.now()

    if not FIRST_ACTIVE_HOUR <= now.hour < END_ACTIVE_HOUR:
        logger.info("Outside active hours, skipping this check")
        return NIGHT_POLL_SECONDS

    try:
        status = get_thermostat().get_hvac_status()
    except ThermostatError as error:
        logger.warning("Could not read the thermostat: %s", error)
        return IDLE_POLL_SECONDS

    logger.info("HVAC status: %s", status)
    if status not in ACTIVE_HVAC_STATES:
        return IDLE_POLL_SECONDS

    try:
        cycle_sprayer_motor()
    except SprayerBusyError:
        logger.info("A manual spray is in progress, skipping this one")
        return IDLE_POLL_SECONDS
    return SPRAY_COOLDOWN_SECONDS


def main() -> int:
    """Run the monitor loop until interrupted."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    try:
        get_thermostat()
    except ConfigError as error:
        logger.error("%s. See .env.example.", error)
        return 1

    logger.info("Starting HVAC monitor")
    try:
        while True:
            sleep(check_hvac_status())
    except KeyboardInterrupt:
        logger.info("Stopping HVAC monitor")
    return 0


if __name__ == "__main__":
    sys.exit(main())
