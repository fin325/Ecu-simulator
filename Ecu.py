import random
import sys
import csv
import time

# --- Диапазоны датчиков ---
LIMITS = {
    "Öldruck": (1.5, 4.5),
    "Temperatur": (80, 110),
    "Drehzahl": (800, 4000)
}

errors = []

def check_sensor(name, value, low, high):
    if value < low:
        return f"{name} ZU NIEDRIG ({value})"
    elif value > high:
        return f"{name} ZU HOCH ({value})"
    return None

def simulate_cycle(cycle, rpm_value):
    """Симуляция одного цикла с оборотами из Input"""
    print(f"\n--- Zyklus {cycle} ---")
    
    # Случайное давление и температура
    oil = round(random.uniform(LIMITS["Öldruck"][0]-0.5, LIMITS["Öldruck"][1]+1.0), 2)
    temp = round(random.uniform(LIMITS["Temperatur"][0]-5, LIMITS["Temperatur"][1]+10), 2)
    rpm = rpm_value
    
    values = {
        "Öldruck": oil,
        "Temperatur": temp,
        "Drehzahl": rpm
    }
    
    for sensor, value in values.items():
        low, high = LIMITS[sensor]
        error = check_sensor(sensor, value, low, high)
        if error:
            print(f"⚠️ FEHLER: {error}")
            errors.append(f"Zyklus {cycle}: {error}")
        else:
            print(f"{sensor}: {value} OK")

# --- Чтение оборотов из вкладки Input ---
print("--- ECU SIMULATION: Ввод оборотов через Input ---")
print("Вставьте числа оборотов по одному в каждой строке.")

reader = csv.reader(sys.stdin)  # stdin = вкладка Input
cycle_number = 1

for row in reader:
    if not row:
        continue
    try:
        rpm_value = float(row[0].strip())
        simulate_cycle(cycle_number, rpm_value)
        cycle_number += 1
        time.sleep(0.3)  # имитация времени
    except (ValueError, IndexError):
        continue

# --- Сохранение логов ---
with open("ecu_error_log.txt", "w") as f:
    f.write("ECU Test Report\n")
    f.write("=================\n\n")
    if errors:
        for err in errors:
            f.write(err + "\n")
    else:
        f.write("Keine Fehler erkannt.\n")

print("\nTest abgeschlossen. Bericht gespeichert als ecu_error_log.txt")