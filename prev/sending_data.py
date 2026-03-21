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

    # Simulate current fluctuations
    motor_current = round(random.uniform(1.9, 2.0), 2)
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

    
    return [   
            #motor Values
            {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "device" : "motor",
                "values" : {
                    "Current" : motor_current,
                    "Voltage" : motor_voltage,
                    "Temp" : motor_temp,
                    "Vibration" : motor_vibration
                }
            },
            #Fan Vavlues
            {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "device" : "fan",
                "values" : {
                    "Current" : fan_current,
                    "Voltage" : fan_voltage,
                    "Temp" : fan_temp,
                    "Vibration" : fan_vibration
                }
            },
            {
                #Bulb Values
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "device" : "bulb",
                "values" : {
                    "Current" : bulb_current,
                    "Voltage" : bulb_voltage,
                    "Temp" : bulb_temp
                }
            }
        ]
    
print("Getting Sensor Data")

while True:
    s_data = generate_appliance_data()

    # Use set() instead of push() to maintain fixed structure
    # s.set((appliance_data))

    #Send Values
    # s_ref.child("motor").push(s_data[0])
    s_ref.child("fan").push(s_data[1])
    # s_ref.child("bulb").push(s_data[2])

    


    print("Sensor Data Updated:", s_data)

    time.sleep(5)
