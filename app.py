from flask import Flask, request
import random

app = Flask(__name__)

LIMITS = {
    "Öldruck": (1.5, 4.5),
    "Temperatur": (80, 110),
    "Drehzahl": (800, 4000)
}

def check_sensor(name, value, low, high):
    if value < low:
        return f"{name} ZU NIEDRIG ({value})"
    elif value > high:
        return f"{name} ZU HOCH ({value})"
    return None

def simulate_cycle(cycle, rpm_value):
    output = f"\n--- Zyklus {cycle} ---\n"

    oil = round(random.uniform(1.0, 5.0), 2)
    temp = round(random.uniform(70, 120), 2)
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
            output += f"⚠️ FEHLER: {error}\n"
        else:
            output += f"{sensor}: {value} OK\n"

    return output

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""

    if request.method == "POST":
        data = request.form["rpm"]
        lines = data.splitlines()

        cycle = 1
        for line in lines:
            try:
                rpm_value = float(line.strip())
                result += simulate_cycle(cycle, rpm_value)
                cycle += 1
            except:
                continue

    return f"""
    <h1>ECU Simulator</h1>
    <form method="post">
        <textarea name="rpm" rows="10" cols="30" placeholder="Введите обороты (по одному в строке)"></textarea><br><br>
        <button type="submit">Start</button>
    </form>
    <pre>{result}</pre>
    """

# важно для Render
if __name__ == "__main__":
    app.run()
