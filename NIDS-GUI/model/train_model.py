import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Get base directory where this script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Load data from model directory using absolute paths
benign_path = os.path.join(base_dir, 'benign_traffic.csv')
malicious_path = os.path.join(base_dir, 'minimal_data.csv')

benign = pd.read_csv(benign_path)
malicious = pd.read_csv(malicious_path)

# Add label column
benign['label'] = 0
malicious['label'] = 1

# Combine datasets
data = pd.concat([benign, malicious], ignore_index=True)

# Select features
features = ['length', 'protocol', 'src_port', 'dst_port', 'flags']

# Encode protocol as integer (example: TCP=6, UDP=17, ICMP=1, etc.)
protocol_map = {'TCP': 6, 'UDP': 17, 'ICMP': 1}
data['protocol'] = data['protocol'].map(protocol_map).fillna(0).astype(int)

# Prepare X and y
X = data[features].copy()
y = data['label']

# Convert flags column from string to numeric safely (fixes SettingWithCopyWarning)
X.loc[:, 'flags'] = X['flags'].apply(lambda x: sum([ord(c) for c in str(x)]))

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model in model directory
model_path = os.path.join(base_dir, 'nids_model.pkl')
joblib.dump(model, model_path)
print(f"[+] Model saved as {model_path}")

