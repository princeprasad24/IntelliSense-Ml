#Time series


import pandas as pd
from sklearn.linear_model import LinearRegression
from joblib import dump

df = pd.read_csv("./datasets/ts_fan_dataset.csv")

window = 5

# devices = ["motor","fan","bulb"]

# for device in devices:

#FAN

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

dump(model,f"./models/ts_fan_model.pkl")

print("ts model saved")
