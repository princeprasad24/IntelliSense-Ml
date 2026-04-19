from pandas import DataFrame as df
from joblib import load,dump
from datetime import datetime
from firebase_admin import credentials,db,initialize_app
from time import sleep
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


# global alert_count 
alert_count = 0 
prev_timestamp = 0.0


#Histroty data for time series
device_history = {
        "pump": [],
        "fan": [],
        "bulb": []
}

#FEATRURES OF DEVICES FOR PREDICITON
devices_data_rfc = {
    "fan": ["Voltage" , "Vibration"],
    "bulb": ["Temp"],
    "pump": ["Flow", "Voltage"]
}

devices_data_ts = {
    "fan" : "Voltage",
    "bulb" : "Temp",
    "pump" : "Flow"
}



def rfc_prediction(device,data):

    #LOAD THE MODEL
    try:
        model = load(f'./models/rfc_{device}_model.pkl')
    except FileNotFoundError:
        return {'Error' : f'File not found for model {device} , {model} '}


    #Get device specific features
    column = devices_data_rfc.get(device)
    
    if not column:
        return {"Error" : f"Device not specified {device}"}
    

    #Process the data fore each device
    def process_data(features,values):

        data = []

        for x in features:
            data.append(values.get(x))

        return data

    processed_data = process_data(values=data,features=column)
    
    print(f"this is the processed data: {processed_data}") 
   
    column_data = []
    for x in column:
        column_data.append(str.lower(x))


    #make it into a dataframe
    test_data = df([processed_data],columns=column_data)
    
    # print(f"The Processed Data is : {processed_data} and \n the data frame is : {test_data}")
    # Make prediction
    prediction = model.predict(test_data)[0]

    print(f"THE prediciton for this  is {prediction}")

    
    def send_alert(device,values,prediciton,alert_type,timestamp):
        
        data = {
            "timestamp" : timestamp,
            "device" : str(device),
            **values,
            "prediction" : float(prediciton),
            "alert_type" : alert_type
        }

        print(f"Data of anamoly : {data}")
        print(f"Anamoly Detected in {device}")
        
        alerts_ref.child(device).push(data)


    if prediction == int(2):
        global alert_count
        alert_count = alert_count + 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        prev_timestamp = datetime.strptime(timestamp , "%H:%M:%S")
        alert_type = "low"
        data_dict = dict(zip(column,processed_data))
        if alert_count > 2:
            if (prev_timestamp-datetime.strptime(timestamp , "%H:%M:%S")).total_seconds() < 100:
                alert_type = "high"

        send_alert(device,data_dict,prediction,alert_type,timestamp)
                



    



def ts_prediction(device,data):

    try:
        model = load(f"./models/ts_{device}_model.pkl")
    except FileNotFoundError:
        return {"error" : f"File not found for {device}"}
    

    data_type = devices_data_ts.get(device)

    if not data_type:
        return {"Error" : f"Device feature not found {device}"}
    
    
    #GET DATA
    sensor_data = data.get(data_type)

    #PREIVOUS VERSION OF data
    prev_sensor_data = device_history[device]

    prev_sensor_data.append(sensor_data)

    
    prev_data_1 = prev_sensor_data[-2]
    prev_data_2 = prev_sensor_data[-1]
    

    print(f"cu data: {sensor_data} , pr1 data: {prev_data_1} , pr2 data: {prev_data_2}")
    #Delete previous data
    max_history_size = 10
    # device_history[device_type].append(voltage)

    if len(device_history[device]) > max_history_size:
        device_history[device].pop(0)
    
    test_data = df([[prev_data_2,prev_data_1]],
                    columns=[f'{str.lower(data_type)}_lag1',f'{str.lower(data_type)}_lag2'])


    #Calculte health of the device
    def calculate_health(deviation,device):
        base_value = {
            "fan" : 100,
            "pump" : 1000,
            "bulb" : 1000
        }
        devitation_multiplier = {
            "fan" : 1,
            "pump" : 10,
            "bulb" : 10
        }
        health = max(0 , base_value.get(device) - deviation*10)
        return health/devitation_multiplier.get(device)

    prediction = model.predict(test_data)[0]

    deviation = abs(sensor_data - prediction)

    health = calculate_health(deviation=deviation,device=device)
    anomaly = 1 if deviation > 3 else 0

    def send_health(health,device):
        data = {
            "device" : device,
            "health" : health,
            # "anamoly" : anamoly
        }
        print(f"Health data : {data}")
        health_ref.child(device).push(data)

    send_health(health=health,device=device)
    print(f"Predicted {data_type}: {prediction}")
    print(f"Actual {data_type}: {sensor_data}")
    print(f"Health of device: {health}")
    # print(f"Anamoly deteceted: {anomaly}")
    print(f"Deviation: {deviation}")
    
    

def printing(x):   

    try:
        # print(x.data)
        # print("GOT INTO PRINTING")
        device_type = x.data.get("device")
        values = x.data.get("values")

        print(f'device type: {device_type} values: {values}')
        print(ts_prediction(device=device_type,data=values))
        # print(rfc_prediction(device=device_type,data=values))
        
    except Exception as e:
        print(f"EXception is : {e}")
        tkk = 0

# sensor_data_ref.listen(printing)

sensor_data_ref.child("pump").listen(printing)
# sleep(2)
sensor_data_ref.child("fan").listen(printing)
sensor_data_ref.child("bulb").listen(printing)








