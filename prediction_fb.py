from pandas import DataFrame as df
from joblib import load
import time
from firebase_admin import credentials,db,initialize_app


#Firebase Login and initailisation
cred = credentials.Certificate("ai-pre-main-firebase-Service_key.json")
initialize_app(cred,{
    'databaseURL' : 'https://ai-pre-main-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

#Reference to my firebase database
sensor_data_ref = db.reference('dev_1')

#Loading the model into a object
model = load('random_forest_model_sensor_data.pkl')






