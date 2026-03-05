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


import pandas as pd
import random
from datetime import datetime, timedelta

rows = []
time = datetime.now()

motor_temp = 40
fan_temp = 30
bulb_temp = 35

for i in range(2000):

    time += timedelta(seconds=5)

    motor_temp += round(random.uniform(-0.3, 0.8))
    fan_temp += round(random.uniform(-0.2, 0.6))
    bulb_temp += round(random.uniform(-0.1, 0.5))

    motor_vib = round(random.uniform(0.5,2.0) + motor_temp/120)
    fan_vib = round(random.uniform(0.2,1.5) + fan_temp/150)

    rows.append([
        time,
        round(random.uniform(0.8,2.0)), round(random.uniform(60,120)), motor_temp, motor_vib,
        round(random.uniform(0.3,1.2)), round(random.uniform(10,24)), fan_temp, fan_vib,
        round(random.uniform(0.3,0.6)), round(random.uniform(5,12)), bulb_temp
    ])

columns = [
"timestamp",
"motor_current","motor_voltage","motor_temp","motor_vibration",
"fan_current","fan_voltage","fan_temp","fan_vibration",
"bulb_current","bulb_voltage","bulb_temp"
]

df = pd.DataFrame(rows,columns=columns)

df.to_csv("device_timeseries.csv",index=False)

print("Dataset created")