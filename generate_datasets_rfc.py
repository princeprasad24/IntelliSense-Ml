
# Actual Sensor Data generation


import pandas as pd
import random

rows = []

samples = 5000


#FAN 

for i in range(samples):

    state = random.choice(["off","normal","fault"])

    if state == "off":

        flow = 0
        current = round(random.uniform(-14,-13),2)
        voltage = 0
        temp = round(random.uniform(30,35),2)
        vibration = 0
        label = 0

    elif state == "normal":

        
        flow = round(random.uniform(60,300),2)
        current = round(random.uniform(-13.8,-13.2),2)
        voltage = round(random.uniform(5,8),2)
        temp = round(random.uniform(30,40),2)
        vibration = 0
        label = 1

    else: # fault

        
        flow = round(random.uniform(0,50),2)
        current = round(random.uniform(-13.3,-12.5),2)
        voltage = round(random.uniform(8,12),2)
        temp = round(random.uniform(30,50),2)
        vibration = random.choice([0,1])
        label = 2

    # rows.append([current,voltage,temp,vibration,label])

    
    rows.append([flow,voltage,label])
    


# df = pd.DataFrame(rows,columns=[
#     "current",
#     "voltage",
#     "temperature",
#     "vibration",
#     "label"
# ])

#PUMP
df = pd.DataFrame(rows,columns=[
    'flow',
    'voltage',
    'label'
])
# df.to_csv("./datasets/rfc_fan_dataset.csv",index=False)
df.to_csv("./datasets/rfc_pump_dataset.csv",index=False)

print("RFC Dataset Created")
