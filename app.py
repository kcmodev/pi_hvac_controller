"""Web interface for triggering the sprayer and checking on the system."""

from __future__ import annotations

import logging
import os

from flask import Flask, jsonify, render_template

from pi_logic.config import ConfigError
from pi_logic.motor_logic import SprayerBusyError, cycle_sprayer_manually
from pi_logic.spray_log import last_spray
from pi_logic.thermostat_logic import ThermostatError, get_thermostat

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.errorhandler(SprayerBusyError)
def handle_sprayer_busy(error):
    return jsonify(error=str(error)), 409


@app.errorhandler(ThermostatError)
def handle_thermostat_error(error):
    # The cause can include device URLs, so it goes to the log rather than the client.
    logger.warning("Thermostat request failed: %s", error)
    return jsonify(error="Could not reach the thermostat"), 502


@app.errorhandler(ConfigError)
def handle_config_error(error):
    logger.error("%s. See .env.example.", error)
    return jsonify(error="Thermostat credentials are not configured"), 503


@app.get("/")
def index():
    """Serve the control page."""
    return render_template("index.html")


@app.post("/spray")
def spray():
    """Start the fan and run a spray cycle, returning its time once complete."""
    cycle_sprayer_manually()
    return jsonify(last_spray())


@app.get("/timestamp")
def timestamp():
    """Return the time of the most recent spray."""
    latest = last_spray()
    if latest is None:
        return jsonify(error="No sprays recorded"), 404
    return jsonify(latest)


@app.get("/status")
def status():
    """Return the current state of the HVAC system."""
    return jsonify(status=get_thermostat().get_hvac_status())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    # Reachable from other devices so it can be used from a phone. See "Security" in the README.
    app.run(host=os.environ.get("HOST", "0.0.0.0"), port=int(os.environ.get("PORT", "5000")))
