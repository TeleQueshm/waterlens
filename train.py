# train_water_quality.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.impute import SimpleImputer
import pickle

# 1. Load CSV
df = pd.read_csv("water_potability.csv")

# 2. Separate features and target
X = df.drop("Potability", axis=1)
y = df["Potability"]

# 3. Handle missing values (replace NaN with column mean)
imputer = SimpleImputer(strategy="mean")
X_imputed = imputer.fit_transform(X)

# 4. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_imputed, y, test_size=0.2, random_state=42, stratify=y
)

# 5. Train Random Forest
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# 6. Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# 7. Save Model & Imputer
with open("water_quality_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("imputer.pkl", "wb") as f:
    pickle.dump(imputer, f)

print("✅ Model and imputer saved: water_quality_model.pkl, imputer.pkl")

