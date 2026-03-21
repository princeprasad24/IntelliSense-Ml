import firebase_admin
from firebase_admin import credentials, db
import joblib
from datetime import datetime

# 1. Firebase Initialization
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://final-year-project-abedc-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# 2. Load separate models if available, or use one robust model
# Tip: A pump failure looks different from a bulb failure.
try:
    models = {
        'dc_motor': joblib.load('motor_model.pkl'),
        'dc_pump': joblib.load('pump_model.pkl'),
        'bulb': joblib.load('bulb_model.pkl')
    }
except:
    print("Models not found. Using threshold fallback logic for demo.")
    models = None

def analyze_appliance(event):
    """
    event.path will look like '/dc_motor/data' or '/bulb/data'
    event.data will be the sensor object
    """
    if event.data is None or event.path == '/': return

    # Extract appliance name from path
    path_parts = event.path.split('/')
    appliance_id = path_parts[1] 
    
    # Get sensor values
    sensors = event.data
    current = sensors.get('current', 0)
    vibration = sensors.get('vibration', 0)
    temp = sensors.get('temp', 0)

    prediction = 0 # 0 = Healthy, 1 = Fail

    # 3. Apply Prediction Logic
    if models:
        # Use ML Model
        features = [[current, vibration, temp]]
        prediction = models[appliance_id].predict(features)[0]
    else:
        # Fallback Threshold Logic (Great for initial testing)
        if appliance_id == 'dc_motor' and (vibration > 0.7 or temp > 70):
            prediction = 1
        elif appliance_id == 'dc_pump' and (current > 5.0 or vibration > 0.9):
            prediction = 1
        elif appliance_id == 'bulb' and current > 1.5: # Overcurrent in bulb
            prediction = 1

    # 4. If Anomaly detected, update Status and Push Alert
    status = "Critical" if prediction == 1 else "Healthy"
    
    # Update the status field in Firebase for the specific appliance
    db.reference(f'appliances/{appliance_id}').update({'status': status})

    if prediction == 1:
        send_ai_alert(appliance_id, f"Predicted failure in {appliance_id} based on anomalous { 'vibration' if vibration > 0.5 else 'electrical' } patterns.")

def send_ai_alert(device, msg):
    alert_ref = db.reference('alerts')
    alert_ref.push({
        "type": device.replace('_', ' ').upper(),
        "priority": "High",
        "message": msg,
        "timestamp": datetime.now().strftime("%I:%M %p")
    })
    print(f"!!! ALERT: {device} failure predicted !!!")

# 5. Listen specifically to the 'appliances' root
print("Monitoring all appliances for failures...")
db.reference('appliances').listen(analyze_appliance)