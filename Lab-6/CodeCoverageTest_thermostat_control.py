"""Code (line) coverage tests for thermostat_control.py.

Goal: execute every line of the module at least once.
One test per return statement / code block is enough for 100% line coverage.
"""
from thermostat_control import target_temperature, hvac_action, energy_alert


# ---------- target_temperature ----------

def test_away_mode():
    # line 3
    assert target_temperature("away", True, 12) == 16


def test_sleep_mode_night():
    # line 6: sleep mode late at night
    assert target_temperature("sleep", True, 23) == 18


def test_sleep_mode_day():
    # line 7: sleep mode during the day
    assert target_temperature("sleep", True, 14) == 20


def test_home_unoccupied():
    # line 9
    assert target_temperature("home", False, 12) == 18


def test_home_morning():
    # line 11: 6 <= hour < 9
    assert target_temperature("home", True, 7) == 22


def test_home_evening():
    # line 13: 17 <= hour < 22
    assert target_temperature("home", True, 19) == 21


def test_home_default():
    # line 14: any other hour
    assert target_temperature("home", True, 12) == 20


# ---------- hvac_action ----------

def test_idle_when_close_to_target():
    # line 20: |diff| < 1
    assert hvac_action(20.5, 21, 15) == "idle"


def test_heat_boost_when_cold_outside():
    # line 23: needs heating and outside < 5
    assert hvac_action(15, 21, 0) == "heat_boost"


def test_heat():
    # line 24: needs heating, outside not cold
    assert hvac_action(18, 21, 15) == "heat"


def test_cool_boost_when_hot_outside():
    # line 26: needs cooling and outside > 30
    assert hvac_action(28, 22, 35) == "cool_boost"


def test_cool():
    # line 27: needs cooling, outside not hot
    assert hvac_action(25, 22, 20) == "cool"


# ---------- energy_alert ----------

def test_energy_ok():
    # line 36: no reading over the limit
    assert energy_alert([5, 8, 9], 10) == "ok"


def test_energy_critical():
    # line 38: more than half the readings over the limit
    assert energy_alert([12, 15, 9], 10) == "critical"


def test_energy_warning():
    # line 39: some, but not more than half, over the limit
    assert energy_alert([12, 5, 6, 7], 10) == "warning"
