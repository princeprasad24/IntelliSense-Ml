
# Actual Sensor Data generation


import pandas as pd
import random

rows = []

samples = 5000


#FAN 

for i in range(samples):

    state = random.choice(["off","normal","fault"])

    if state == "off":

        current = round(random.uniform(-14,-13),2)
        voltage = 0
        temp = round(random.uniform(30,35),2)
        vibration = 0
        label = 0

    elif state == "normal":

        current = round(random.uniform(-13.8,-13.2),2)
        voltage = round(random.uniform(9,12),2)
        temp = round(random.uniform(30,40),2)
        vibration = 0
        label = 1

    else: # fault

        current = round(random.uniform(-13.3,-12.5),2)
        voltage = round(random.uniform(13,18),2)
        temp = round(random.uniform(30,50),2)
        vibration = random.choice([0,1])
        label = 2

    rows.append([current,voltage,temp,vibration,label])


df = pd.DataFrame(rows,columns=[
    "current",
    "voltage",
    "temperature",
    "vibration",
    "label"
])

df.to_csv("./datasets/rfc_sensor_dataset.csv",index=False)

print("RFC Dataset Created")
