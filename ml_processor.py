# import firebase_admin
# from firebase_admin import credentials, db
# import pandas as pd
# import joblib  # To load your trained model
# from datetime import datetime

# # 1. Firebase Setup
# # Download your serviceAccountKey.json from Firebase Project Settings
# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://final-year-project-abedc-default-rtdb.asia-southeast1.firebasedatabase.app/'
# })

# # Load your pre-trained Random Forest Model
# # For now, we'll use a simple threshold-based logic placeholder 
# # until your model is fully trained.
# model = joblib.load('random_forest_model.pkl') 

# def process_and_predict(event):
#     """Callback function triggered on every Firebase update"""
#     if event.data is None:
#         print("No data received.")
#         return

#     # Extract new data
#     data = event.data
#     current = data.get('current', 0)
#     vibration = data.get('vibration', 0)
#     temp = data.get('temp', 0)

#     # 2. ML Prediction
#     # Create a features array (matching your training columns)
#     features = pd.DataFrame([[current, vibration, temp]], 
#                             columns=['current', 'vibration', 'temp'])
    
#     prediction = model.predict(features)[0] # 0 = Healthy, 1 = Anomaly

#     # 3. Handle Anomaly
#     if prediction == 1:
#         send_alert(f"Anomaly detected! Vib: {vibration}g, Temp: {temp}°C", "High")

# def send_alert(message, priority):
#     alert_ref = db.reference('alerts')
#     new_alert = {
#         "type": "AI Prediction",
#         "priority": priority,
#         "message": message,
#         "timestamp": datetime.now().strftime("%H:%M %p")
#     }
#     alert_ref.push(new_alert)
#     print(f"Alert Sent: {message}")

# # 4. Set up the Real-time Listener on the 'sensor_data' node
# print("AI Engine Started. Listening for sensor data...")
# db.reference('sensor_data').listen(process_and_predict)



import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import joblib
from datetime import datetime
import time

# -------------------------
# 1. Firebase Setup
# -------------------------
cred = credentials.Certificate("ai-pre-main-firebase-Service_key.json")
firebase_admin.initialize_app(cred, {
    # 'databaseURL': 'https://final-year-project-abedc-default-rtdb.asia-southeast1.firebasedatabase.app/' #Prasad URL
    'databaseURL' : "https://ai-pre-main-default-rtdb.asia-southeast1.firebasedatabase.app/dev_1" #MY URL
})

sensor_ref = db.reference('sensor_data')
alerts_ref = db.reference('alerts')

# -------------------------
# 2. Load Pre-trained Model
# -------------------------
model = joblib.load('random_forest_model.pkl')

# -------------------------
# 3. Callback Function
# -------------------------
def process_and_predict(event):
    """Triggered on every Firebase update"""
    if event.data is None:
        print("No data received.")
        return

    # Extract sensor values safely
    current = float(event.data.get('current', 0))
    vibration = float(event.data.get('vibration', 0))
    temp = float(event.data.get('temp', 0))

    # Prepare features for the ML model
    features = pd.DataFrame([[current, vibration, temp]],
                            columns=['current', 'vibration', 'temp'])
    
    # Make prediction
    prediction = model.predict(features)[0]  # 0 = Healthy, 1 = Anomaly

    # Handle anomaly
    if prediction == 1:
        send_alert(
            f"Anomaly detected! Vib: {vibration}g, Temp: {temp}°C, Current: {current}A",
            priority="High"
        )

# -------------------------
# 4. Send Alert
# -------------------------
def send_alert(message, priority):
    new_alert = {
        "type": "AI Prediction",
        "priority": priority,
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    alerts_ref.push(new_alert)
    print(f"Alert Sent: {message}")

# -------------------------
# 5. Run Listener with Auto-Reconnect
# -------------------------
print("AI Engine Started. Listening for sensor data...")

while True:
    try:
        sensor_ref.listen(process_and_predict)
    except Exception as e:
        print(f"Connection lost: {e}. Reconnecting in 5 seconds...")
        time.sleep(5)
