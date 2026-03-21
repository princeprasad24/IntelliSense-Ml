# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import classification_report
# from joblib import dump

# # Load dataset
# df = pd.read_csv("sensor_dataset_training.csv")

# # Features and label
# X = df[["current","voltage","temperature","vibration"]]
# y = df["fault"]

# # Train test split
# X_train, X_test, y_train, y_test = train_test_split(
#     X,y,test_size=0.2,random_state=42
# )

# # Train model
# model = RandomForestClassifier(
#     n_estimators=100,
#     random_state=42
# )

# model.fit(X_train,y_train)

# # Evaluate
# pred = model.predict(X_test)

# print(classification_report(y_test,pred))

# # Save model
# dump(model,"rfc_model.pkl")

# print("Random Forest model saved")


#Time series

import pandas as pd
from sklearn.linear_model import LinearRegression
from joblib import dump

# Load dataset
df = pd.read_csv("timeseries_sensor_dataset.csv")

# Create lag features
df["voltage_lag1"] = df["voltage"].shift(1)
df["voltage_lag2"] = df["voltage"].shift(2)

df = df.dropna()

# Features
X = df[["voltage_lag1","voltage_lag2","vibration"]]

# Target
y = df["voltage"]

# Train model
model = LinearRegression()
model.fit(X,y)

# Save model
dump(model,"ts_model.pkl")

print("Time Series model saved")