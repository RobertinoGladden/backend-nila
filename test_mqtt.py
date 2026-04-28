import paho.mqtt.client as mqtt
import json
import time
import random

BROKER = "broker.hivemq.com"
PORT   = 1883
TOPIC  = "aqua/sensor/data"

def simulate():
    client = mqtt.Client(client_id="sensor-simulator-01")
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()

    print("Sensor Simulator Berjalan...")
    print(f"Publish ke: {TOPIC}\n")

    scenarios = [
        {
            "name":             "Normal",
            "temperature":      27.5,
            "dissolved_oxygen": 6.8,
            "ph":               7.8,
            "turbidity":        3.1,
            "tds":              450.0,
        },
        {
            "name":             "Waspada",
            "temperature":      28.8,
            "dissolved_oxygen": 5.4,
            "ph":               8.2,
            "turbidity":        4.2,
            "tds":              380.0,
        },
        {
            "name":             "Kritis",
            "temperature":      29.8,
            "dissolved_oxygen": 3.8,
            "ph":               8.6,
            "turbidity":        5.1,
            "tds":              280.0,
        },
    ]

    i = 0
    while True:
        scenario = scenarios[i % len(scenarios)]

        payload = {
            "device_id":        "sensor-01",
            "temperature":      round(scenario["temperature"] + random.uniform(-0.2, 0.2), 2),
            "dissolved_oxygen": round(scenario["dissolved_oxygen"] + random.uniform(-0.1, 0.1), 2),
            "ph":               round(scenario["ph"] + random.uniform(-0.05, 0.05), 2),
            "turbidity":        round(scenario["turbidity"] + random.uniform(-0.1, 0.1), 2),
            "tds":              round(scenario["tds"] + random.uniform(-10, 10), 2),
        }

        client.publish(TOPIC, json.dumps(payload), qos=1)

        print(f"[{i+1}] Scenario: {scenario['name']}")
        print(f"     T={payload['temperature']}C  "
              f"DO={payload['dissolved_oxygen']}mg/L  "
              f"pH={payload['ph']}  "
              f"Turb={payload['turbidity']}NTU  "
              f"TDS={payload['tds']}ppm")
        print()

        time.sleep(5)
        i += 1

if __name__ == "__main__":
    try:
        simulate()
    except KeyboardInterrupt:
        print("\nSimulator dihentikan")