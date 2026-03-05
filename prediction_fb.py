from pandas import DataFrame as df
from joblib import load,dump
import time
import jsonify
from firebase_admin import credentials,db,initialize_app


#Firebase Login and initailisation
cred = credentials.Certificate("ai-pre-main-firebase-Service_key.json") #Ganesh key
# cred = credentials.Certificate("serviceAccountKey.json")    #PRASAD Key

initialize_app(cred,{
    # 'databaseURL': 'https://final-year-project-abedc-default-rtdb.asia-southeast1.firebasedatabase.app/' #Prasad URL
    'databaseURL' : 'https://ai-pre-main-default-rtdb.asia-southeast1.firebasedatabase.app/' #Ganesh URL
})

#Reference to my firebase database
sensor_data_ref = db.reference('dev_1')
alerts_ref = db.reference('alerts')



#Loading the model into a object
def predicttion(device_type,current,voltage,temp,vibration):


    #Loading the Model
    try:
        model = load(f'rfm_{device_type}_model.pkl')
    except FileNotFoundError:
        return {'error': f'Model for {device_type} not found'}
    
    #Creating Test data
    test_data = df([[current, voltage, temp, vibration]],
                    columns=[f'{device_type}_current', f'{device_type}_voltage', f'{device_type}_temp', f'{device_type}_vibration'])
        
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


    if prediction == int(1):
        send_alert(device_type,current,voltage,temp,prediction)

def printing(x):   

    try:
        device_type = x.data.get("device")
        values = x.data.get("values")
        current = values.get("Current")
        Voltage = values.get("Voltage")
        Temp = values.get("Temp")
        Vibr = values.get("Vibration")
        print(f'device type: {device_type} current: {current}  voltage: {Voltage} Temperature: {Temp}  Vibration: {Vibr}')
        predicttion(device_type=device_type,current=current,voltage=Voltage,temp=Temp,vibration=Vibr)

    except:
        tkk = 0


sensor_data_ref.child("Sensor data").child("motor").listen(printing)
sensor_data_ref.child("Sensor data").child("fan").listen(printing)
sensor_data_ref.child("Sensor data").child("bulb").listen(printing)








