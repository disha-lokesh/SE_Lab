def target_temperature(mode, occupied, hour):
    if mode == "away":
        return 16
    if mode == "sleep":
        if hour < 6 or hour >= 22:
            return 18
        return 20
    if not occupied:
        return 18
    if 6 <= hour < 9:
        return 22
    if 17 <= hour < 22:
        return 21
    return 20


def hvac_action(current, target, outside):
    diff = target - current
    if abs(diff) < 1:
        return "idle"
    if diff > 0:
        if outside < 5:
            return "heat_boost"
        return "heat"
    if outside > 30:
        return "cool_boost"
    return "cool"


def energy_alert(readings, limit):
    over = 0
    for reading in readings:
        if reading > limit:
            over += 1
    if over == 0:
        return "ok"
    if over * 2 > len(readings):
        return "critical"
    return "warning"
