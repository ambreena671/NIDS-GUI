# save_model.py
import pickle
from sklearn.ensemble import RandomForestClassifier
import os

# Dummy training data
X = [
    [100, 6, 1],
    [200, 17, 0],
    [1500, 6, 1],
    [60, 1, 0]
]
y = [0, 1, 0, 1]

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Ensure "core" directory exists
os.makedirs("core", exist_ok=True)

# Save model to core/model.pkl
with open("core/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("[+] Model saved to core/model.pkl")

