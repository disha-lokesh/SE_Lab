"""Branch coverage tests for thermostat_control.py.

Goal: every decision (if / for) is taken both ways (True and False),
and every part of a compound condition (`or`, chained `<=  <`) is
exercised on its own, including the exact boundary values.
"""
import pytest

from thermostat_control import target_temperature, hvac_action, energy_alert


# ---------- target_temperature ----------
# Decisions: mode == "away" | mode == "sleep" | hour < 6 or hour >= 22
#            not occupied | 6 <= hour < 9 | 17 <= hour < 22

@pytest.mark.parametrize("occupied, hour", [
    (True, 12), (False, 3), (True, 23),
])
def test_away_true_branch(occupied, hour):
    # mode == "away" -> True, regardless of occupancy / hour
    assert target_temperature("away", occupied, hour) == 16


@pytest.mark.parametrize("hour, expected", [
    (0, 18),    # hour < 6 True (left side of `or`)
    (5, 18),    # boundary: last hour before 6
    (6, 20),    # boundary: hour < 6 False, hour >= 22 False
    (21, 20),   # boundary: last hour before 22
    (22, 18),   # hour < 6 False, hour >= 22 True (right side of `or`)
    (23, 18),
])
def test_sleep_mode_branches(hour, expected):
    assert target_temperature("sleep", True, hour) == expected


def test_sleep_mode_ignores_occupancy():
    # sleep branch returns before the occupancy check is reached
    assert target_temperature("sleep", False, 12) == 20


@pytest.mark.parametrize("hour", [0, 7, 19, 23])
def test_not_occupied_true_branch(hour):
    # not occupied -> True: 18 at any hour, even morning / evening
    assert target_temperature("home", False, hour) == 18


@pytest.mark.parametrize("hour, expected", [
    (5, 20),    # 6 <= hour False (lower bound fails)
    (6, 22),    # boundary: morning starts
    (8, 22),    # boundary: last morning hour
    (9, 20),    # hour < 9 False (upper bound fails)
    (16, 20),   # 17 <= hour False
    (17, 21),   # boundary: evening starts
    (21, 21),   # boundary: last evening hour
    (22, 20),   # hour < 22 False
    (12, 20),   # both time windows False -> default
])
def test_occupied_time_windows(hour, expected):
    assert target_temperature("home", True, hour) == expected


def test_unknown_mode_behaves_like_home():
    # mode is neither "away" nor "sleep" -> both mode checks False
    assert target_temperature("eco", True, 7) == 22


# ---------- hvac_action ----------
# Decisions: abs(diff) < 1 | diff > 0 | outside < 5 | outside > 30

@pytest.mark.parametrize("current, target", [
    (21, 21),       # diff == 0
    (20.5, 21),     # diff = +0.5
    (21.5, 21),     # diff = -0.5
    (20.01, 21),    # diff just under +1
])
def test_idle_branch(current, target):
    assert hvac_action(current, target, 15) == "idle"


@pytest.mark.parametrize("outside, expected", [
    (-10, "heat_boost"),
    (4.9, "heat_boost"),    # just under 5
    (5, "heat"),            # boundary: outside < 5 False
    (20, "heat"),
])
def test_heating_branches(outside, expected):
    assert hvac_action(18, 21, outside) == expected


def test_diff_exactly_plus_one_heats():
    # abs(diff) < 1 False at exactly 1 -> heating path
    assert hvac_action(20, 21, 15) == "heat"


@pytest.mark.parametrize("outside, expected", [
    (40, "cool_boost"),
    (30.1, "cool_boost"),   # just over 30
    (30, "cool"),           # boundary: outside > 30 False
    (10, "cool"),
])
def test_cooling_branches(outside, expected):
    assert hvac_action(25, 22, outside) == expected


def test_diff_exactly_minus_one_cools():
    # abs(diff) < 1 False at exactly -1 -> diff > 0 False -> cooling path
    assert hvac_action(22, 21, 20) == "cool"


# ---------- energy_alert ----------
# Decisions: for loop entered / skipped | reading > limit
#            over == 0 | over * 2 > len(readings)

def test_empty_readings_loop_not_entered():
    # for loop body never runs -> over stays 0
    assert energy_alert([], 10) == "ok"


@pytest.mark.parametrize("readings", [
    [5, 8, 9],
    [10, 10],       # boundary: reading == limit is NOT over
])
def test_all_readings_within_limit(readings):
    assert energy_alert(readings, 10) == "ok"


@pytest.mark.parametrize("readings, expected", [
    ([11], "critical"),             # 1 of 1 over
    ([12, 15, 9], "critical"),      # 2 of 3 over
    ([12, 5], "warning"),           # boundary: exactly half over (2 > 2 False)
    ([12, 13, 5, 6], "warning"),    # exactly half over
    ([12, 5, 6, 7], "warning"),     # 1 of 4 over
    ([12, 13, 14, 5], "critical"),  # 3 of 4 over
])
def test_over_limit_branches(readings, expected):
    assert energy_alert(readings, 10) == expected
