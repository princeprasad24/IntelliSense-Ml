import firebase_admin
from firebase_admin import credentials, db
import random
import time
from datetime import datetime

cred = credentials.Certificate("ai-pre-main-firebase-Service_key.json") #GANESH DB
# cred = credentials.Certificate("serviceAccountKey.json")    #PRASAD DB

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://ai-pre-main-default-rtdb.asia-southeast1.firebasedatabase.app/"  #GANESH DB
    # "databaseURL" : "https://final-year-project-abedc-default-rtdb.asia-southeast1.firebasedatabase.app//" #PRASAD DB
})

# Reference to appliances node
s_ref = db.reference("Sensor data")
alerts_red = db.reference("alerts")

# Base values
motor_health = 95
fan_health = 90
bulb_health = 100

def generate_appliance_data():
    global motor_health, fan_health, bulb_health

import random

# Base values
motor_health = 95
fan_health = 90
bulb_health = 100
import random
import datetime

# Base values
motor_health = 95
fan_health = 90
bulb_health = 100

def generate_appliance_data():
    global motor_health, fan_health, bulb_health

    def get_state_values(device):
        state = random.choice(["off", "normal", "fault"])

        if state == "off":
            current = round(random.uniform(-14, -13), 2)
            voltage = 0
            temp = round(random.uniform(30, 35), 2)
            vibration = 0
            label = 0

        elif state == "normal":
            current = round(random.uniform(-13.8, -13.2), 2)
            voltage = round(random.uniform(7, 12), 2)
            temp = round(random.uniform(30, 40), 2)
            vibration = 0
            label = 1

        else:  # fault
            current = round(random.uniform(-13.3, -12.5), 2)
            voltage = round(random.uniform(13, 18), 2)
            temp = round(random.uniform(30, 50), 2)
            vibration = random.choice([0, 1])
            label = 2

        # Force off‑like if health < 20
        health = {
            "motor": motor_health,
            "fan": fan_health,
            "bulb": bulb_health
        }[device]

        if health < 20:
            current = 0.0
            voltage = 0
            vibration = 0
            temp = round(random.uniform(30, 35), 2)

        return current, voltage, temp, vibration

    # Generate values for each device using the above ranges
    motor_current, motor_voltage, motor_temp, motor_vibration = get_state_values("motor")
    fan_current,   fan_voltage,   fan_temp,   fan_vibration   = get_state_values("fan")
    bulb_current,  bulb_voltage,  bulb_temp,  _               = get_state_values("bulb")

    # # Random health degradation
    # motor_health -= random.uniform(0, 0.5)
    # fan_health   -= random.uniform(0, 1.0)
    # bulb_health  -= random.uniform(0, 0.2)

    # # Random fan failure (5% chance)
    # if random.random() < 0.05:
    #     fan_health = random.uniform(0, 20)

    # # Clamp health between 0 and 100
    # motor_health = max(0, min(100, motor_health))
    # fan_health   = max(0, min(100, fan_health))
    # bulb_health  = max(0, min(100, bulb_health))

    # Return in your exact format
    return [
        # Motor values
        {
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "device": "motor",
            "values": {
                "Current": motor_current,
                "Voltage": motor_voltage,
                "Temp": motor_temp,
                "Vibration": motor_vibration
            }
        },
        # Fan values
        {
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "device": "fan",
            "values": {
                "Current": fan_current,
                "Voltage": fan_voltage,
                "temperature": fan_temp,
                "Vibration": fan_vibration
            }
        },
        # Bulb values
        {
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "device": "bulb",
            "values": {
                "Current": bulb_current,
                "Voltage": bulb_voltage,
                "Temp": bulb_temp
            }
        }
    ]

# Example usage:
# data = generate_appliance_data()
# print(data['motor']['current'], data['motor']['voltage'], etc.)

    
print("Getting Sensor Data")

while True:
    s_data = generate_appliance_data()
    # print(s_data)
    # Use set() instead of push() to maintain fixed structure
    # s.set((appliance_data))

    #Send Values
    # s_ref.child("motor").push(s_data[0])
    s_ref.child("fan").push(s_data[1])
    # s_ref.child("bulb").push(s_data[2])

    


    print("Sensor Data Updated:", s_data[1])

    time.sleep(5)
