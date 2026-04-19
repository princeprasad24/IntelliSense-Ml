
#Actual sensor data

import pandas as pd
import random
from datetime import datetime,timedelta

rows = []

time = datetime.now()

samples = 6000

limit = False
prev_state = ""
prev_flow = 0


#FAN
for i in range(samples):

    #FOR PUMP
    if limit:
        state = random.choice(["off","normal","fault"])
        prev_state = state
    else:
        state = prev_state

    #FOR FAN
    # state = random.choice(["off","normal","fault"])

    if state == "off":

        flow = 0
        current = round(random.uniform(-14,-13),2)
        voltage = 0
        temp = 0
        vibration = 0
        label = 0
        limit = True

    elif state == "normal":
        
        if not limit:
            flow = round(prev_flow+random.uniform(0,15),2)
            prev_flow = flow
        else:
            flow = round(random.uniform(60,300),2)
            prev_flow = flow
            limit = False
        current = round(random.uniform(-13.7,-13.3),2)
        voltage = round(random.uniform(2,3),2)
        temp = round(random.uniform(25,26),2)
        vibration = 0
        label = 1
        flow = float(flow)
        if flow>300:
            limit = True

    else:

        if not limit:
            flow = round(prev_flow+random.uniform(0,15),2)
            prev_flow = flow
        else:
            flow = round(random.uniform(0,50),2)
            prev_flow = flow
            limit = False
        current = round(random.uniform(-13.3,-12.7),2)
        voltage = round(random.uniform(4,4),2)
        temp = round(random.uniform(27,27),2)
        vibration = 1
        label = 2
        flow = float(flow)
        if flow>50:
            limit = True

    # rows.append([
    #     time,
    #     current,
    #     voltage,
    #     temp,
    #     vibration,
    #     label
    # ])

    # rows.append([time,flow,voltage,label])

    rows.append([time,temp,voltage,label])

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
    'temp',
    'voltage',
    'label'
])

# df.to_csv("./datasets/ts_fan_dataset.csv",index=False)
# df.to_csv("./datasets/ts_pump_dataset.csv",index=False)
df.to_csv("./datasets/ts_bulb_dataset.csv",index=False)

print("Time Series Dataset Created")