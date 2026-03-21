from pandas import DataFrame as df
from joblib import load,dump
from datetime import datetime
from firebase_admin import credentials,db,initialize_app


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


# #Loading the model into a object
# #OLD
# def rfc_predicttion(device_type,current,voltage,temp,vibration):


#     #Loading the Model
#     try:
#         model = load(f'rfc_model.pkl')
#     except FileNotFoundError:
#         return {'error': f'Model for {device_type} not found'}
    
#     #Creating Test data
#     if vibration is not None:
#         test_data = df([[current, voltage, temp, vibration]],
#                         columns=['current', 'voltage', 'temperature', 'vibration'])
#     else:
#         test_data = df([[current, voltage, temp]],
#                         columns=['current', 'voltage', 'temp'])

#     # Make prediction
#     prediction = model.predict(test_data)[0]
#     # fault_probability = model.predict_proba(test_data)[0][1]  # Probability of fault

#     print(f"THE prediciton for this  is {prediction}")


#     def send_alert(device,current,voltage,temp,prediciton,timestamp):
#         data = {
#             "timestamp" : timestamp,
#             "device" : str(device),
#             "Current" : float(current),
#             "Voltage" : float(voltage),
#             "Temp" : float(temp),
#             "prediction" : float(prediciton)
#         }

#         print(type(data))
#         print(f"Anamoly Detected in {device}")
        
#         alerts_ref.child(device_type).push(data)


#     if prediction == int(2):
#         timestamp = datetime.now().strftime("%H:%M:%S")
#         send_alert(device_type,current,voltage,temp,prediction,timestamp)
#         # send_health(anamoly=1,health=35,device=device_type)



def rfc_prediction(device,data):

    try:
        model = load(f'rfc_{device}_model.pkl')
    except FileNotFoundError:
        return {'Error' : f'File not found for model {device}'}

    return 0
    



def ts_prediction(device,data):

    try:
        model = load(f"ts_{device}_model.pkl")
    except FileNotFoundError:
        return {"error" : f"File not found for {device}"}
    

   #Differ each device data
    if device is 'fan':
        data_type = 'Voltage'
    elif device is 'bulb':
        data_type = 'Temp'
    elif device is 'pump':
        data_type = 'Flow'

    
    #GET DATA
    sensor_data = data.get(data_type)

    #PREIVOUS VERSION OF data
    prev_sensor_data = device_history[device]

    prev_sensor_data.append(sensor_data)


    prev_data_1 = prev_sensor_data[-2]
    prev_data_2 = prev_sensor_data[-1]
    

    
    #Delete previous data
    max_history_size = 10
    # device_history[device_type].append(voltage)

    if len(device_history[device]) > max_history_size:
        device_history[device].pop(0)


    test_data = df([prev_data_1,prev_data_2],
                    columns=[f'{data_type}_lag_1',f'{data_type}_lag_2'])


    #Calculte health of the device
    def calculate_health(deviation):
        health = max(0, 100 - deviation*10)

        return health

    prediction = model.predict(test_data)[0]

    deviation = abs(sensor_data - prediction)

    health = calculate_health(deviation=deviation)
    anomaly = 1 if deviation > 3 else 0

    def send_health(anamoly,health,device):
        data = {
            "device" : device,
            "health" : health,
            "anamoly" : anamoly
        }
        print(f"Health data : {data}")
        health_ref.child(device).push(data)

    send_health(anamoly=anomaly,health=health,device=device)
    print(f"Predicted {data_type}: {prediction}")
    print(f"Actual {data_type}: {sensor_data}")
    print(f"Health of device: {health}")
    print(f"Anamoly deteceted: {anomaly}")
    print(f"Deviation: {deviation}")
    

    
    
    

        


# #Time Series analysis 
# OLD
# def ts_prediction(device_type,current,voltage,temp,vibration):

#     #Storing previous data for time series
#     try:
#         model = load(f"ts_model.pkl")
#     except FileNotFoundError:
#         return {"error": f"Model for {device_type} not found"}
    

#     print("HELLO TS")
#     history = device_history[device_type]

#     history.append(voltage)

#     if len(history) < 3:
#         print("Not enough data yet")
#         return 0,100

#     voltage_lag1 = history[-2]
#     voltage_lag2 = history[-3]

#     # create input dataframe
#     # if current is not None:
#     test_data = df(
#         [[voltage_lag1,voltage_lag2,vibration]],
#         columns=["voltage_lag1",
#                 "voltage_lag2",
#                 "vibration_lag1"]
#     )

#     #Delete previous data
#     max_history_size = 10
#     # device_history[device_type].append(voltage)

#     if len(device_history[device_type]) > max_history_size:
#         device_history[device_type].pop(0)

#     #Calculte health of the device
#     def calculate_health(deviation):
#         health = max(0, 100 - deviation*10)

#         return health

#     predicted_voltage = model.predict(test_data)[0]

#     deviation = abs(voltage - predicted_voltage)

#     health = calculate_health(deviation=deviation)
#     anomaly = 1 if deviation > 3 else 0

#     def send_health(anamoly,health,device):
#         data = {
#             "device" : device,
#             "health" : health,
#             "anamoly" : anamoly
#         }
#         print(f"Health data : {data}")
#         health_ref.child(device).push(data)

#     send_health(anamoly=anomaly,health=health,device=device_type)
#     print(f"Predicted Voltage: {predicted_voltage}")
#     print(f"Actual Voltage: {voltage}")
#     print(f"Health of device: {health}")
#     print(f"Anamoly deteceted: {anomaly}")
#     # print(f"Deviation: {deviation}")

    

def printing(x):   

    try:
        device_type = x.data.get("device")
        values = x.data.get("values")
        # current = values.get("Current")
        # Voltage = values.get("Voltage")
        # Temp = values.get("Temp")
        # Vibr = values.get("Vibration")

        # current = measure_current()
        
        # print(f'device type: {device_type} current: {current}  voltage: {Voltage} Temperature: {Temp}  Vibration: {Vibr}')
        # rfc_predicttion(device_type=device_type,current=current,voltage=Voltage,temp=Temp,vibration=Vibr) #prediction for random forest
        ts_prediction(device_type=device_type,data=values) #prediciton for time series
        
    except Exception as e:
        print(f"EXception is : {e}")
        tkk = 0


sensor_data_ref.child("motor").listen(printing)
sensor_data_ref.child("fan").listen(printing)
sensor_data_ref.child("bulb").listen(printing)








