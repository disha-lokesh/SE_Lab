def parse_setpoint(text):
    value = float(text[:-1])
    if text[-1].upper() == 'F':
        value = (value - 32) * 5 / 9
    return round(value, 1)

def average_temperature(readings_csv):
    values = [float(r) for r in readings_csv.split(',')]
    return sum(values) / len(values)

def schedule_slot(time_text):
    hour, minute = time_text.split(':')
    hour = int(hour)
    if hour < 6:
        return 'night ' + minute
    return 'day ' + str(int(minute))

def main():
    print("==== Running parse_setpoint ====")
    user_input = input("Enter a setpoint (e.g. 21.5C or 70F): ")
    result = parse_setpoint(user_input)
    print("Setpoint in Celsius:", result)

    print("\n==== Running average_temperature ====")
    user_input = input("Enter sensor readings as CSV (e.g. 20.5,21,22.5): ")
    result = average_temperature(user_input)
    print("Average Temperature:", result)

    print("\n==== Running schedule_slot ====")
    user_input = input("Enter a time as HH:MM (e.g. 07:30): ")
    result = schedule_slot(user_input)
    print("Schedule Slot:", result)

if __name__ == "__main__":
    main()
