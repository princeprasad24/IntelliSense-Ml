import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# 1. Load the generated data
df = pd.read_csv('sensor_training_data.csv')
X = df[['current', 'vibration', 'temp']]
y = df['target']

# 2. Split into Training (80%) and Testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Initialize and Train
model = RandomForestClassifier(n_estimators=100, max_depth=5)
model.fit(X_train, y_train)

# 4. Evaluate
predictions = model.predict(X_test)
print("--- Model Performance ---")
print(classification_report(y_test, predictions))

# 5. Save the model
joblib.dump(model, 'random_forest_model.pkl')
print("Model saved as random_forest_model.pkl")