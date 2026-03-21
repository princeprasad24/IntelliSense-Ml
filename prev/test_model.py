
from joblib import load
from pandas import DataFrame as pd
import random
import time

device = "motor"
# model = load("random_forest_model_sensor_data.pkl")
model = load(f"rfm_{device}_model.pkl")



for i in range(10):
    # Simulate current fluctuations
    motor_current = round(random.uniform(1.5, 2.0), 2)
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

    print(f"this is the data :  \n \
        motor Current: {motor_current} , Voltage : {motor_voltage} \n \
        temp : {motor_temp} vibration : {motor_vibration} ")

    test_data = pd([[motor_current,motor_voltage,motor_temp,motor_vibration]],
                            columns=['motor_current','motor_voltage','motor_temp','motor_vibration'])

    predict = model.predict(test_data)[0]

    print(f"Model Prediticon {predict}")
    if predict == 0: print("NO Failure Detected")
    else : print("Failure Detected")
    time.sleep(5)