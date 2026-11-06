import pytest
from thermostat_control import target_temperature, hvac_action, energy_alert

#Example test cases:
def test_away_mode():
    assert target_temperature("away", True, 12) == 16

def test_no_readings():
    assert energy_alert([], 10) == "ok"

#Write the rest of the test cases so that the code is 90- 100% covered.
