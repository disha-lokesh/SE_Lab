"""Hypothesis fuzz tests for thermostat_control.py (Lab 7).

Two kinds of test for each function:
  1. "no crash" fuzzing: random text / None must never raise an exception.
  2. property tests: for generated valid inputs, the answer must be right,
     and for anything invalid the function must return None.
"""
import math

from hypothesis import given, strategies as st

from thermostat_control import parse_setpoint, average_temperature, schedule_slot


# ---------------------------------------------------------------- parse_setpoint

@given(st.text() | st.none())
def test_parse_setpoint_no_crash(s):
    try:
        result = parse_setpoint(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"parse_setpoint crashed with: {e!r}"
    # Either rejected (None) or a real, finite temperature
    assert result is None or (isinstance(result, float) and math.isfinite(result))


@given(st.integers(min_value=-50, max_value=150))
def test_parse_setpoint_plain_number_is_celsius(n):
    # "70" has no unit: it must be read as 70 C, not chopped to 7
    assert parse_setpoint(str(n)) == n


@given(st.integers(min_value=-100, max_value=300), st.sampled_from(["F", "f"]))
def test_parse_setpoint_fahrenheit_conversion(f, unit):
    assert parse_setpoint(f"{f}{unit}") == round((f - 32) * 5 / 9, 1)


@given(st.floats(min_value=-100, max_value=100), st.sampled_from(["C", "c"]))
def test_parse_setpoint_celsius_round_trip(c, unit):
    assert parse_setpoint(f"{c}{unit}") == round(c, 1)


@given(st.sampled_from(["nanC", "infF", "-infC", "NaN", "inf"]))
def test_parse_setpoint_rejects_nan_and_inf(s):
    assert parse_setpoint(s) is None


# ------------------------------------------------------------ average_temperature

@given(st.text() | st.none())
def test_average_temperature_no_crash(s):
    try:
        result = average_temperature(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"average_temperature crashed with: {e!r}"
    assert result is None or (isinstance(result, float) and math.isfinite(result))


@given(st.lists(st.floats(min_value=-1000, max_value=1000),
                min_size=1, max_size=20))
def test_average_is_between_min_and_max(values):
    result = average_temperature(",".join(repr(v) for v in values))
    assert result is not None and math.isfinite(result)
    # Small tolerance for floating-point rounding
    tol = 1e-9 * max(1.0, max(abs(v) for v in values))
    assert min(values) - tol <= result <= max(values) + tol


@given(st.lists(st.floats(min_value=-1000, max_value=1000), max_size=5),
       st.floats(min_value=1000.001, max_value=1e308), st.booleans())
def test_average_rejects_impossible_readings(values, huge, negative):
    # A reading beyond +/-1000 degrees is a sensor fault, not a temperature
    bad = -huge if negative else huge
    text = ",".join(repr(v) for v in values + [bad])
    assert average_temperature(text) is None


@given(st.lists(st.floats(min_value=-50, max_value=60), min_size=1, max_size=10))
def test_average_ignores_spaces_around_values(values):
    text = " , ".join(str(v) for v in values)
    expected = sum(values) / len(values)
    assert math.isclose(average_temperature(text), expected, abs_tol=1e-9)


@given(st.sampled_from(["", " ", ",", "20,,21", "20,abc", "nan", "20,inf"]))
def test_average_rejects_bad_csv(s):
    assert average_temperature(s) is None


# ------------------------------------------------------------------ schedule_slot

@given(st.text() | st.none())
def test_schedule_slot_no_crash(s):
    try:
        result = schedule_slot(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"schedule_slot crashed with: {e!r}"
    assert result is None or result.startswith(("night ", "day "))


@given(st.integers(min_value=0, max_value=23), st.integers(min_value=0, max_value=59))
def test_schedule_slot_valid_times(hour, minute):
    expected = ("night " if hour < 6 else "day ") + f"{minute:02d}"
    assert schedule_slot(f"{hour:02d}:{minute:02d}") == expected
    assert schedule_slot(f"{hour}:{minute:02d}") == expected


@given(st.one_of(
    st.tuples(st.integers(min_value=24, max_value=999), st.integers(0, 59)),
    st.tuples(st.integers(min_value=-999, max_value=-1), st.integers(0, 59)),
    st.tuples(st.integers(0, 23), st.integers(min_value=60, max_value=999)),
))
def test_schedule_slot_rejects_out_of_range(hm):
    hour, minute = hm
    assert schedule_slot(f"{hour}:{minute:02d}") is None
