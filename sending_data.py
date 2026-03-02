import firebase_admin
from firebase_admin import credentials, db
import random
import time
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://final-year-project-abedc-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

# Reference to appliances node
appliances_ref = db.reference("appliances")

# Base values
motor_health = 95
pump_health = 90
bulb_health = 100

def generate_appliance_data():
    global motor_health, pump_health, bulb_health

    # Simulate current fluctuations
    motor_current = round(random.uniform(0.8, 2.0), 2)
    pump_current = round(random.uniform(0.0, 1.5), 2)
    bulb_current = round(random.uniform(0.3, 0.6), 2)

    # Random health degradation
    motor_health -= random.uniform(0, 0.5)
    pump_health -= random.uniform(0, 1.0)
    bulb_health -= random.uniform(0, 0.2)

    # Random failure event (5% chance)
    if random.random() < 0.05:
        pump_health = random.uniform(0, 20)

    # Clamp health between 0 and 100
    motor_health = max(0, min(100, motor_health))
    pump_health = max(0, min(100, pump_health))
    bulb_health = max(0, min(100, bulb_health))

    # Determine status
    motor_status = "Failure" if motor_health < 20 else "Active"
    pump_status = "Failure" if pump_health < 20 else "Active"
    bulb_status = "Failure" if bulb_health < 20 else "Active"

    # If failure → current becomes 0
    if motor_status == "Failure":
        motor_current = 0.0
    if pump_status == "Failure":
        pump_current = 0.0
    if bulb_status == "Failure":
        bulb_current = 0.0

    return {
        "dc_motor": {
            "status": motor_status,
            "health": int(motor_health),
            "current": motor_current,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        },
        "dc_pump": {
            "status": pump_status,
            "health": int(pump_health),
            "current": pump_current,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        },
        "bulb": {
            "status": bulb_status,
            "health": int(bulb_health),
            "current": bulb_current,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
    }


print("🚀 Appliance Simulator Started...")

while True:
    appliance_data = generate_appliance_data()

    # Use set() instead of push() to maintain fixed structure
    appliances_ref.set(appliance_data)

    print("📡 Appliances Updated:", appliance_data)

    time.sleep(2)
