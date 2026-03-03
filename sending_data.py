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
fan_health = 90
bulb_health = 100

def generate_appliance_data():
    global motor_health, fan_health, bulb_health

    # Simulate current fluctuations
    motor_current = round(random.uniform(0.8, 2.0), 2)
    fan_current = round(random.uniform(0.0, 1.5), 2)
    bulb_current = round(random.uniform(0.3, 0.6), 2)


    #Simulating Voltage fluctuations
    motor_voltage = round(random.uniform(0.0,120.0),2)
    fan_voltage = round(random.uniform(0.0,24.0),2)
    bulb_voltage = round(random.uniform(0.0,12.0),2)

    #Simulating Tempearture Fluctuations
    motor_temp = round(random.uniform(25.0,95.0),2)
    fan_temp = round(random.uniform(20.0,60.0),2)
    bulb_temp = round(random.uniform(25.0,120.0),2)


    #Simulating Vibration Fluctuations
    motor_vibration = round(random.uniform(0.2,5.0),2)
    fan_vibration = round(random.uniform(0.1,2.5),2)

    # Random health degradation
    motor_health -= random.uniform(0, 0.5)
    fan_health -= random.uniform(0, 1.0)
    bulb_health -= random.uniform(0, 0.2)

    # Random failure event (5% chance)
    if random.random() < 0.05:
        fan_health = random.uniform(0, 20)

    # Clamp health between 0 and 100
    motor_health = max(0, min(100, motor_health))
    fan_health = max(0, min(100, fan_health))
    bulb_health = max(0, min(100, bulb_health))

    # Determine status
    motor_status = "Failure" if motor_health < 20 else "Active"
    fan_status = "Failure" if fan_health < 20 else "Active"
    bulb_status = "Failure" if bulb_health < 20 else "Active"

    # If failure → current becomes 0
    if motor_status == "Failure":
        motor_current = 0.0
    if fan_status == "Failure":
        fan_current = 0.0
    if bulb_status == "Failure":
        bulb_current = 0.0

    return {
        "motor": {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "Current" : motor_current,
            "voltage" : motor_voltage,
            "Temp" : motor_temp,
            "Vibration" : motor_vibration
        },
        "fan": {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "Current" : fan_current,
            "Voltage" : fan_voltage,
            "Temp" : fan_temp,
            "Vibration" : fan_vibration
        },
        "bulb": {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "Current" : bulb_current,
            "voltage" : bulb_voltage,
            "Temp" : bulb_temp
        }
    }


print("🚀 Appliance Simulator Started...")

while True:
    appliance_data = generate_appliance_data()

    # Use set() instead of push() to maintain fixed structure
    appliances_ref.set(appliance_data)

    print("📡 Appliances Updated:", appliance_data)

    time.sleep(2)
