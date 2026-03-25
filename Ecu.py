from flask import Flask, request, render_template_string
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
    oil = round(random.uniform(1.0, 5.0), 2)
    temp = round(random.uniform(70, 120), 2)

    results = []
    values = {
        "Öldruck": oil,
        "Temperatur": temp,
        "Drehzahl": rpm_value
    }

    for sensor, value in values.items():
        low, high = LIMITS[sensor]
        error = check_sensor(sensor, value, low, high)
        if error:
            results.append(f"⚠️ {error}")
        else:
            results.append(f"{sensor}: {value} OK")

    return results

HTML = """
<h1>ECU Simulator</h1>
<form method="post">
<textarea name="rpm" rows="10" cols="30" placeholder="Введите обороты по строкам"></textarea><br><br>
<button type="submit">Запустить</button>
</form>

{% if output %}
<h2>Результат:</h2>
<pre>
{% for line in output %}
{{ line }}
{% endfor %}
</pre>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    output = []
    if request.method == "POST":
        data = request.form["rpm"].splitlines()
        cycle = 1

        for line in data:
            if not line.strip():
                continue
            try:
                rpm = float(line.strip())
                output.append(f"\n--- Zyklus {cycle} ---")
                result = simulate_cycle(cycle, rpm)
                output.extend(result)
                cycle += 1
            except:
                output.append(f"Ошибка в строке: {line}")

    return render_template_string(HTML, output=output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
