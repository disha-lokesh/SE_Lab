"""Smart Thermostat Controller (Lab 7, hardened after fuzz testing).

Every function validates its input and returns None for anything it
cannot handle, instead of crashing or returning a wrong value.
"""
import math
import re

MAX_READING = 1000.0   # sanity limit for a sensor reading (degrees)
# [0-9] (not \d) so only ASCII digits are accepted
_TIME_RE = re.compile(r"([0-9]{1,2}):([0-9]{2})")


def _to_finite_float(text):
    """Convert text to a finite float, or return None."""
    try:
        value = float(text)
    except ValueError:
        return None
    return value if math.isfinite(value) else None


def parse_setpoint(text):
    """Parse '21.5C', '70F' or a plain number (Celsius); return Celsius or None."""
    if not isinstance(text, str):
        return None
    text = text.strip()
    if not text:
        return None
    unit = text[-1].upper()
    if unit in ("C", "F"):
        number = text[:-1]
    else:
        unit, number = "C", text          # no unit given: treat as Celsius
    value = _to_finite_float(number)
    if value is None:
        return None
    if unit == "F":
        value = (value - 32) / 9 * 5      # divide first so huge values can't overflow
    if not math.isfinite(value):
        return None
    return round(value, 1)


def average_temperature(readings_csv):
    """Average of comma-separated readings; None if empty or any value is bad.

    Readings outside +/-MAX_READING are rejected as sensor errors.
    """
    if not isinstance(readings_csv, str):
        return None
    parts = [part.strip() for part in readings_csv.split(",")]
    values = [_to_finite_float(part) for part in parts]
    if not values or None in values:
        return None
    if any(abs(v) > MAX_READING for v in values):
        return None
    return math.fsum(values) / len(values)


def schedule_slot(time_text):
    """Label an 'HH:MM' time as 'night MM' (before 06:00) or 'day MM'; else None."""
    if not isinstance(time_text, str):
        return None
    match = _TIME_RE.fullmatch(time_text.strip())
    if match is None:
        return None
    hour, minute = int(match.group(1)), int(match.group(2))
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        return None
    label = "night" if hour < 6 else "day"
    return f"{label} {minute:02d}"


def _show(label, result, error_message):
    """Print a result, or a friendly error when the input was rejected."""
    if result is None:
        print(error_message)
    else:
        print(label, result)


def main():
    """Ask for three inputs and print the results."""
    print("==== Running parse_setpoint ====")
    user_input = input("Enter a setpoint (e.g. 21.5C or 70F): ")
    _show("Setpoint in Celsius:", parse_setpoint(user_input),
          "Invalid setpoint. Use a number with optional C or F, e.g. 21.5C or 70F.")

    print("\n==== Running average_temperature ====")
    user_input = input("Enter sensor readings as CSV (e.g. 20.5,21,22.5): ")
    _show("Average Temperature:", average_temperature(user_input),
          "Invalid readings. Give numbers separated by commas, e.g. 20.5,21,22.5.")

    print("\n==== Running schedule_slot ====")
    user_input = input("Enter a time as HH:MM (e.g. 07:30): ")
    _show("Schedule Slot:", schedule_slot(user_input),
          "Invalid time. Use HH:MM with hour 0-23 and minute 0-59, e.g. 07:30.")


if __name__ == "__main__":
    main()
