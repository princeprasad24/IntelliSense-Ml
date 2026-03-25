# RFC

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from joblib import dump

# df = pd.read_csv("./datasets/rfc_fan_dataset.csv")

df = pd.read_csv("./datasets/ts_pump_dataset.csv")

#FAN
# X = df[["voltage","vibration"]]
# y = df["label"]

X = df[["flow","voltage"]]
y = df['label']

X_train,X_test,y_train,y_test = train_test_split(
    X,y,test_size=0.2,random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10
)

model.fit(X_train,y_train)

accuracy = model.score(X_test,y_test)

print("Model Accuracy:",accuracy)

dump(model,"./models/rfc_pump_model.pkl")

print("RFC Model Saved")
