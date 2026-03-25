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
    data = ""
    
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
    <html>
    <head>
      <title>ECU Simulator</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          display: flex;
          flex-direction: column;
          align-items: center;
          margin-top: 50px;
          background-color: #f0f0f0;
        }}
        h1 {{
          color: #333;
        }}
        textarea {{
          width: 400px;
          height: 200px;
          font-size: 16px;
          padding: 10px;
          border-radius: 5px;
          border: 1px solid #ccc;
          resize: vertical;
        }}
        button {{
          margin-top: 10px;
          padding: 10px 20px;
          font-size: 16px;
          border-radius: 5px;
          border: none;
          background-color: #007bff;
          color: white;
          cursor: pointer;
        }}
        button:hover {{
          background-color: #0056b3;
        }}
        pre {{
          width: 80%;
          background-color: #fff;
          padding: 10px;
          border-radius: 5px;
          margin-top: 20px;
          overflow-x: auto;
        }}
      </style>
    </head>
    <body>
      <h1>ECU Simulator</h1>
      <form method="post">
          <textarea name="rpm" placeholder="Введите обороты (по одному в строке)">{data}</textarea><br>
          <button type="submit">Start</button>
      </form>
      <pre>{result}</pre>
    </body>
    </html>
    """

# важно для Render
if __name__ == "__main__":
    app.run()
