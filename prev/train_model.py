# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score, classification_report
# import joblib
# import pickle


# #LOADINGF THE CSV FILE
# data = pd.read_csv("sensors_dataset_training.csv")


# #Model data for motor
# motor_X = data[["motor_current","motor_voltage","motor_temp","motor_vibration"]]
# motor_y = data["motor_fault"]

# #Model data for Fan
# fan_x = data[["fan_current", "fan_voltage", "fan_temp", "fan_vibration"]]
# fan_y = data["fan_fault"]

# #Model data for Bulb
# bulb_x = data[["bulb_current", "bulb_voltage", "bulb_temp"]]
# bulb_y = data["bulb_fault"]



# #Train and generate models
# def creating_model(x,y):

#     x_train, x_test, y_train, y_test = train_test_split(
#         x, y, test_size=0.2, random_state=42
#     )
#     model = RandomForestClassifier(
#         n_estimators=100,
#         max_depth=5,
#         random_state=42
#     )

#     model.fit(x_train, y_train)

#     y_pred = model.predict(x_test)

#     print("Accuracy:", accuracy_score(y_test, y_pred))
#     print(classification_report(y_test, y_pred))

#     return model


# #Creating Models
# motor_model = creating_model(motor_X,motor_y)
# fan_model = creating_model(fan_x,fan_y)
# bulb_model = creating_model(bulb_x,bulb_y)


# #Saving models into a file
# joblib.dump(motor_model,"rfm_motor_model.pkl")
# joblib.dump(fan_model,"rfm_fan_model.pkl")
# joblib.dump(bulb_model,"rfm_bulb_model.pkl")

#Time Series 

# train_timeseries_model.py

# import pandas as pd
# from sklearn.linear_model import LinearRegression
# from joblib import dump

# df = pd.read_csv("timeseries_device_data.csv")

# window = 5

# devices = ["motor","fan","bulb"]

# for device in devices:

#     temp_col = f"{device}_temp"
#     vib_col = f"{device}_vibration" if device != "bulb" else None

#     df[f"{temp_col}_lag1"] = df[temp_col].shift(1)
#     df[f"{temp_col}_lag2"] = df[temp_col].shift(2)

#     features = [f"{temp_col}_lag1",f"{temp_col}_lag2"]

#     if vib_col:
#         df[f"{vib_col}_lag1"] = df[vib_col].shift(1)
#         features.append(f"{vib_col}_lag1")

#     df_model = df.dropna()

#     X = df_model[features]
#     y = df_model[temp_col]

#     model = LinearRegression()
#     model.fit(X,y)

#     dump(model,f"ts_{device}_model.pkl")

#     print(f"{device} model saved")

