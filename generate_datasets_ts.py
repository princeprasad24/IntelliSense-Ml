
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

        flow = 0
        current = round(random.uniform(-14,-13),2)
        voltage = 0
        temp = 32
        vibration = 0
        label = 0

    elif state == "normal":
        
        flow = round(random.uniform(60,300),2)
        current = round(random.uniform(-13.7,-13.3),2)
        voltage = round(random.uniform(5,8),2)
        temp = round(random.uniform(30,40),2)
        vibration = 0
        label = 1

    else:

        flow = round(random.uniform(0,50),2)
        current = round(random.uniform(-13.3,-12.7),2)
        voltage = round(random.uniform(8,12),2)
        temp = round(random.uniform(35,55),2)
        vibration = 1
        label = 2

    # rows.append([
    #     time,
    #     current,
    #     voltage,
    #     temp,
    #     vibration,
    #     label
    # ])

    rows.append([time,flow,voltage,label])

    time = time + timedelta(seconds=5)


#FAN
# df = pd.DataFrame(rows,columns=[
#     "timestamp",
#     "current",
#     "voltage",
#     "temperature",
#     "vibration",
#     "label"
# ])

#PUMP
df = pd.DataFrame(rows,columns=[
    'timestamp',
    'flow',
    'voltage',
    'label'
])


# df.to_csv("./datasets/ts_fan_dataset.csv",index=False)
df.to_csv("./datasets/ts_pump_dataset.csv",index=False)
print("Time Series Dataset Created")