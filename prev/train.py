
#RFC

# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from joblib import dump

# df = pd.read_csv("rfc_sensor_dataset.csv")

# X = df[["current","voltage","temperature","vibration"]]
# y = df["label"]

# X_train,X_test,y_train,y_test = train_test_split(
#     X,y,test_size=0.2,random_state=42
# )

# model = RandomForestClassifier(
#     n_estimators=200,
#     max_depth=10
# )

# model.fit(X_train,y_train)

# accuracy = model.score(X_test,y_test)

# print("Model Accuracy:",accuracy)

# dump(model,"rfc_model.pkl")

# print("RFC Model Saved")

#Time series


import pandas as pd
from sklearn.linear_model import LinearRegression
from joblib import dump

df = pd.read_csv("ts_sensor_dataset.csv")

window = 5

# devices = ["motor","fan","bulb"]

# for device in devices:

vol_col = "voltage"
temp_col = "temperature"
vib_col = "vibration"

# df[f"{temp_col}_lag1"] = df[temp_col].shift(1)
# df[f"{temp_col}_lag2"] = df[temp_col].shift(2)

df[f"{vol_col}_lag1"] = df[vol_col].shift(1)
df[f"{vol_col}_lag2"] = df[vol_col].shift(2)


features = [f"{vol_col}_lag1",f"{vol_col}_lag2"]

if vib_col:
    df[f"{vib_col}_lag1"] = df[vib_col].shift(1)
    features.append(f"{vib_col}_lag1")

df_model = df.dropna()

X = df_model[features]
y = df_model[vol_col]

model = LinearRegression()
model.fit(X,y)

dump(model,f"ts_model.pkl")

print("ts model saved")
