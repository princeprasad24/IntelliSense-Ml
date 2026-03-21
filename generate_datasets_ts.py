
#Actual sensor data

import pandas as pd
import random
from datetime import datetime,timedelta

rows = []

time = datetime.now()

samples = 6000

#FAN
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

df.to_csv("./datasets/ts_fan_dataset.csv",index=False)

print("Time Series Dataset Created")