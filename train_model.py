import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import matplotlib.pyplot as plt


#LOADINGF THE CSV FILE
data = pd.read_csv("sensors_dataset_training.csv")


# Example: Train model for Motor fault prediction
X = data[["motor_current","motor_voltage","motor_temp","motor_vibration"]]
y = data["motor_fault"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)



model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

#Saving the model
# joblib.dump(model, 'random_forest_model_sensor_data.pkl')

importance = model.feature_importances_

plt.bar(X.columns, importance)
plt.title("Feature Importance")
plt.show()