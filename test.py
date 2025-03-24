import requests
import datetime
import random
import time

SERVER_URL = "http://127.0.0.1:5000/add_log"  # Flask server endpoint

def generate_log():
    return {
        "time_of_check": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        "Heart_beat_rate": random.randint(60, 100),  # Simulated BPM
        "Sp02_level": round(random.uniform(95, 100), 1),  # Simulated SpO2 %
        "Temperature": round(random.uniform(36.0, 37.5), 1)  # Simulated Temperature (°C)
    }

while True:
    log = generate_log()
    print("\nGenerated Log:")
    print(f"Time: {log['time_of_check']}")
    print(f"Heart Rate: {log['Heart_beat_rate']} BPM")
    print(f"SpO2 Level: {log['Sp02_level']}%")
    print(f"Temperature: {log['Temperature']}°C")

    confirm = input("Send this log to the server? (yes/no/exit): ").strip().lower()
    
    if confirm == "y":
        try:
            response = requests.post(SERVER_URL, json=log)
            if response.status_code == 200:
                print("✔ Log sent successfully!")
            else:
                print(f"❌ Error: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to send log: {e}")
    if confirm == "exit":
        break
    
 # Wait before generating the next log
