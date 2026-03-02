from sklearn.ensemble import RandomForestClassifier
import joblib
import pandas as pd

# Example Training Data: [Current, Vibration, Temp] -> Status (0=Good, 1=Fail)
data = {
    'current': [2.1, 2.2, 8.5, 2.0, 9.2, 2.3],
    'vibration': [0.02, 0.03, 0.85, 0.02, 0.90, 0.04],
    'temp': [35, 36, 82, 34, 88, 37],
    'target': [0, 0, 1, 0, 1, 0] # 1 represents a simulated failure
}

df = pd.DataFrame(data)
X = df[['current', 'vibration', 'temp']]
y = df['target']

# Train Model
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X, y)

# Save the brain!
joblib.dump(clf, 'random_forest_model.pkl')