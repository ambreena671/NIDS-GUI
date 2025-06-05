import pickle
import os
import pandas as pd

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), "..", "model", "model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

# One-hot encoded flag columns expected by the model
flag_columns = ["flags_FA", "flags_NONE", "flags_PA", "flags_S", "flags_A"]

def predict_packet(packet_features):
    try:
        # Prepare the base feature dictionary
        data = {
            "length": packet_features.get("length", 0),
            "protocol": packet_features.get("protocol", 0),
            "src_port": packet_features.get("src_port", 0),
            "dst_port": packet_features.get("dst_port", 0)
        }

        # Initialize all flag columns to 0
        for col in flag_columns:
            data[col] = 0

        # Get flag value and set corresponding one-hot column
        flag_value = f"flags_{packet_features.get('flags', 'NONE')}"
        if flag_value in flag_columns:
            data[flag_value] = 1

        # Convert to DataFrame and predict
        df = pd.DataFrame([data])
        prediction = model.predict(df)[0]
        return prediction

    except Exception as e:
        print(f"[Detector Error] {e}")
        return 0

