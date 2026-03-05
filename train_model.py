import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import matplotlib.pyplot as plt


#LOADINGF THE CSV FILE
data = pd.read_csv("sensors_dataset_training.csv")


#Model data for motor
motor_X = data[["motor_current","motor_voltage","motor_temp","motor_vibration"]]
motor_y = data["motor_fault"]

#Model data for Fan
fan_x = data[["fan_current", "fan_voltage", "fan_temp", "fan_vibration"]]
fan_y = data["fan_fault"]

#Model data for Bulb
bulb_x = data[["bulb_current", "bulb_voltage", "bulb_temp"]]
bulb_y = data["bulb_fault"]



#Train and generate models
def creating_model(x,y):

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42
    )

    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    return model


#Creating Models
motor_model = creating_model(motor_X,motor_y)
fan_model = creating_model(fan_x,fan_y)
bulb_model = creating_model(bulb_x,bulb_y)


#Saving models into a file
for i in ["motor_model","fan_model","bulb_model"]:
    joblib.dump(i,f"rfm_{i}.pkl")


#Saving the model
# joblib.dump(model, 'random_forest_model_sensor_data.pkl')

# importance = model.feature_importances_

# plt.bar(X.columns, importance)
# plt.title("Feature Importance")
# plt.show()