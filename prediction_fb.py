from pandas import DataFrame as df
from joblib import load,dump
import time
from firebase_admin import credentials,db,initialize_app
import random


#Firebase Login and initailisation
# cred = credentials.Certificate("ai-pre-main-firebase-Service_key.json") #Ganesh key
cred = credentials.Certificate("serviceAccountKey.json")    #PRASAD Key

initialize_app(cred,{
    'databaseURL': 'https://final-year-project-abedc-default-rtdb.asia-southeast1.firebasedatabase.app/' #Prasad URL
    # 'databaseURL' : 'https://ai-pre-main-default-rtdb.asia-southeast1.firebasedatabase.app/' #Ganesh URL
})

#Reference to my firebase database
sensor_data_ref = db.reference('Sensor data')
alerts_ref = db.reference('alerts')
health_ref = db.reference('remaining_life')


#Histroty data for time series
device_history = {
        "motor": [],
        "fan": [],
        "bulb": []
}

def measure_current(c,v):
    
        if c <= 0 and v >= 10:
             return 1
        elif c <= 0 :
            return 0
        else: 
            return 0


#Loading the model into a object
def rfc_predicttion(device_type,current,voltage,temp,vibration):


    #Loading the Model
    try:
        model = load(f'rfc_model.pkl')
    except FileNotFoundError:
        return {'error': f'Model for {device_type} not found'}
    
    #Creating Test data
    if vibration is not None:
        test_data = df([[current, voltage, temp, vibration]],
                        columns=['current', 'voltage', 'temperature', 'vibration'])
    else:
        test_data = df([[current, voltage, temp]],
                        columns=['current', 'voltage', 'temp'])

    # Make prediction
    prediction = model.predict(test_data)[0]
    # fault_probability = model.predict_proba(test_data)[0][1]  # Probability of fault

    print(f"THE prediciton for this  is {prediction}")


    def send_alert(device,current,voltage,temp,prediciton):
        data = {
            "device" : str(device),
            "Current" : float(current),
            "Voltage" : float(voltage),
            "Temp" : float(temp),
            "prediction" : float(prediciton)
        }

        print(type(data))
        print(f"Anamoly Detected in {device}")
        
        alerts_ref.child(device_type).push(data)


    if prediction == int(2):
        send_alert(device_type,current,voltage,temp,prediction)

#Time Series analysis
def ts_prediction(device_type,current,voltage,temp,vibration):

    #Storing previous data for time series
    try:
        model = load(f"ts_model.pkl")
    except FileNotFoundError:
        return {"error": f"Model for {device_type} not found"}
    

    history = device_history[device_type]

    history.append(temp)

    if len(history) < 3:
        print("Not enough data yet")
        return 0,100

    current_lag1 = history[-2]
    current_lag2 = history[-3]

    # create input dataframe
    if current is not None:
        test_data = df(
            [[current_lag1,current_lag2,vibration]],
            columns=["current_lag1",
                    "current_lag2",
                    "vibration_lag1"]
        )
    else:
        test_data = df(
            [[current_lag1,current_lag2]],
            columns=[f"{device_type}_current_lag1",
                    f"{device_type}_current_lag2"]
        )

    #Delete previous data
    max_history_size = 10
    device_history[device_type].append(temp)

    if len(device_history[device_type]) > max_history_size:
        device_history[device_type].pop(0)
    

    def send_health(anamoly,health,device):
        data = {
            "device" : device,
            "health" : health,
            "anamoly" : anamoly
        }
        print(f"Health data : {data}")
        health_ref.child(device).push(data)

    #Calculte health of the device
    def calculate_health(deviation):
        health = max(0, 100 - deviation*1000)

        return health

    predicted_temp = model.predict(test_data)[0]

    deviation = abs(temp - predicted_temp)

    health = calculate_health(deviation=deviation)
    anomaly = 1 if deviation > 10 else 0

    send_health(anamoly=anomaly,health=health,device=device_type)
    # print(f"Predicted Temp: {predicted_temp}")
    # print(f"Actual Temp: {temp}")
    # print(f"Deviation: {deviation}")

    

def printing(x):   

    try:
        device_type = x.data.get("device")
        values = x.data.get("values")
        current = values.get("Current")
        Voltage = values.get("Voltage")
        Temp = values.get("Temp")
        Vibr = values.get("Vibration")

        # current = measure_current()
        
        print(f'device type: {device_type} current: {current}  voltage: {Voltage} Temperature: {Temp}  Vibration: {Vibr}')
        rfc_predicttion(device_type=device_type,current=current,voltage=Voltage,temp=Temp,vibration=Vibr) #prediction for random forest
        ts_prediction(device_type=device_type,current=current,voltage=Voltage,temp=Temp,vibration=Vibr) #prediciton for time series

    except:
        tkk = 0


sensor_data_ref.child("motor").listen(printing)
sensor_data_ref.child("fan").listen(printing)
sensor_data_ref.child("bulb").listen(printing)








