#Random Forest algorithm data generation
# import random
# import csv

# # Number of rows you want in dataset
# num_samples = 1000

# # CSV file name
# filename = "sensors_dataset_training.csv"

# # Create CSV file
# with open(filename, mode='w', newline='') as file:
#     writer = csv.writer(file)
    
#     # Writing Header
#     writer.writerow([
#         "motor_current", "motor_voltage", "motor_temp", "motor_vibration", "motor_fault",
#         "fan_current", "fan_voltage", "fan_temp", "fan_vibration", "fan_fault",
#         "bulb_current", "bulb_voltage", "bulb_temp", "bulb_fault"
#     ])
    
#     for _ in range(num_samples):
        
#         # ---------------- Motor ----------------
#         motor_current = round(random.uniform(0.8, 2.0), 2)
#         motor_voltage = round(random.uniform(0.0, 120.0), 2)
#         motor_temp = round(random.uniform(25.0, 95.0), 2)
#         motor_vibration = round(random.uniform(0.2, 5.0), 2)
        
#         motor_fault = 1 if (
#             motor_temp > 85 or
#             motor_vibration > 4.5 or
#             motor_current > 1.8
#         ) else 0
        
#         # ---------------- Fan ----------------
#         fan_current = round(random.uniform(0.0, 1.5), 2)
#         fan_voltage = round(random.uniform(0.0, 24.0), 2)
#         fan_temp = round(random.uniform(20.0, 60.0), 2)
#         fan_vibration = round(random.uniform(0.1, 2.5), 2)
        
#         fan_fault = 1 if (
#             fan_temp > 55 or
#             fan_vibration > 2.0 or
#             fan_current > 1.3
#         ) else 0
        
#         # ---------------- Bulb ----------------
#         bulb_current = round(random.uniform(0.3, 0.6), 2)
#         bulb_voltage = round(random.uniform(0.0, 12.0), 2)
#         bulb_temp = round(random.uniform(25.0, 120.0), 2)
        
#         bulb_fault = 1 if (
#             bulb_temp > 110 or
#             bulb_current > 0.55
#         ) else 0
        
#         # Write row
#         writer.writerow([
#             motor_current, motor_voltage, motor_temp, motor_vibration, motor_fault,
#             fan_current, fan_voltage, fan_temp, fan_vibration, fan_fault,
#             bulb_current, bulb_voltage, bulb_temp, bulb_fault
#         ])

# print(f"Dataset '{filename}' generated successfully with {num_samples} samples.")


#Time series analysis data generation


# import pandas as pd
# import random
# from datetime import datetime, timedelta

# rows = []
# time = datetime.now()

# motor_temp = 40
# fan_temp = 30
# bulb_temp = 35

# for i in range(2000):

#     time += timedelta(seconds=5)

#     motor_temp += round(random.uniform(-0.3, 0.8))
#     fan_temp += round(random.uniform(-0.2, 0.6))
#     bulb_temp += round(random.uniform(-0.1, 0.5))

#     motor_vib = round(random.uniform(0.5,2.0) + motor_temp/120)
#     fan_vib = round(random.uniform(0.2,1.5) + fan_temp/150)

#     rows.append([
#         time,
#         round(random.uniform(0.8,2.0)), round(random.uniform(60,120)), motor_temp, motor_vib,
#         round(random.uniform(0.3,1.2)), round(random.uniform(10,24)), fan_temp, fan_vib,
#         round(random.uniform(0.3,0.6)), round(random.uniform(5,12)), bulb_temp
#     ])

# columns = [
# "timestamp",
# "motor_current","motor_voltage","motor_temp","motor_vibration",
# "fan_current","fan_voltage","fan_temp","fan_vibration",
# "bulb_current","bulb_voltage","bulb_temp"
# ]


#Actual Sensor Data generation

#RFC
# import pandas as pd
# import random

# rows = []

# samples = 5000

# for i in range(samples):

#     state = random.choice(["off","normal","fault"])

#     if state == "off":

#         current = round(random.uniform(-14,-13),2)
#         voltage = 0
#         temp = round(random.uniform(30,35),2)
#         vibration = 0
#         label = 0

#     elif state == "normal":

#         current = round(random.uniform(-13.8,-13.2),2)
#         voltage = round(random.uniform(9,12),2)
#         temp = round(random.uniform(30,40),2)
#         vibration = 0
#         label = 1

#     else: # fault

#         current = round(random.uniform(-13.3,-12.5),2)
#         voltage = round(random.uniform(13,18),2)
#         temp = round(random.uniform(30,50),2)
#         vibration = random.choice([0,1])
#         label = 2

#     rows.append([current,voltage,temp,vibration,label])


# df = pd.DataFrame(rows,columns=[
#     "current",
#     "voltage",
#     "temperature",
#     "vibration",
#     "label"
# ])

# df.to_csv("rfc_sensor_dataset.csv",index=False)

# print("RFC Dataset Created")

#Time serires Actual Data

import pandas as pd
import random
from datetime import datetime,timedelta

rows = []

time = datetime.now()

samples = 6000

for i in range(samples):

    state = random.choice(["off","normal","fault"])

    if state == "off":

        current = round(random.uniform(-14,-13),2)
        voltage = 0
        temp = 32
        vibration = 0
        label = 0

    elif state == "normal":

        current = round(random.uniform(-13.7,-13.3),2)
        voltage = round(random.uniform(9,12),2)
        temp = round(random.uniform(30,40),2)
        vibration = 0
        label = 1

    else:

        current = round(random.uniform(-13.3,-12.7),2)
        voltage = round(random.uniform(13,18),2)
        temp = round(random.uniform(35,55),2)
        vibration = 1
        label = 2

    rows.append([
        time,
        current,
        voltage,
        temp,
        vibration,
        label
    ])

    time = time + timedelta(seconds=5)


df = pd.DataFrame(rows,columns=[
    "timestamp",
    "current",
    "voltage",
    "temperature",
    "vibration",
    "label"
])

df.to_csv("ts_sensor_dataset.csv",index=False)

print("Time Series Dataset Created")