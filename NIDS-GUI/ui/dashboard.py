import streamlit as st
import threading
import time
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.packet_sniffer import packet_queue, start_sniffing
from core.detector import predict_packet  # Your prediction function

# Initialize session state variables to keep packets between reruns
if 'recent_packets' not in st.session_state:
    st.session_state['recent_packets'] = []

if 'threat_alerts' not in st.session_state:
    st.session_state['threat_alerts'] = []

# Start sniffing thread once
if 'sniffing_started' not in st.session_state:
    threading.Thread(target=start_sniffing, daemon=True).start()
    st.session_state['sniffing_started'] = True

# Function to process packets from queue and update session state
def update_packets():
    while not packet_queue.empty():
        features = packet_queue.get()
        prediction = predict_packet(features)
        
        pkt_with_pred = {**features, "prediction": prediction}
        st.session_state['recent_packets'].append(pkt_with_pred)

        # Save to CSV file (optional)
        CSV_FILE = "captured_packets.csv"
        df = pd.DataFrame([pkt_with_pred])
        if not os.path.exists(CSV_FILE):
            df.to_csv(CSV_FILE, index=False)
        else:
            df.to_csv(CSV_FILE, mode='a', header=False, index=False)

        if prediction == 1:
            st.session_state['threat_alerts'].append(pkt_with_pred)

# Streamlit UI rendering function
def render_ui():
    st.title("🔐 AI-Based Network Intrusion Detection System")

    update_packets()

    # Show recent packets (last 10)
    st.subheader("📡 Recent Packets")
    if st.session_state['recent_packets']:
        recent_df = pd.DataFrame(st.session_state['recent_packets'][-10:])
        st.table(recent_df)
    else:
        st.info("Waiting for packets...")

    # Show threat alerts (last 5)
    st.subheader("🚨 Threat Alerts")
    if st.session_state['threat_alerts']:
        st.error("⚠️ Intrusions Detected!")
        alert_df = pd.DataFrame(st.session_state['threat_alerts'][-5:])
        st.table(alert_df)
    else:
        st.success("✅ No threats detected.")

    # Threat distribution pie chart by protocol
    if st.session_state['threat_alerts']:
        st.subheader("📊 Threat Type Distribution by Protocol")
        protocol_counts = pd.Series([p["protocol"] for p in st.session_state['threat_alerts']]).value_counts()
        protocol_map = {6: "TCP", 17: "UDP", 1: "ICMP"}
        labels = [protocol_map.get(p, str(p)) for p in protocol_counts.index]

        fig, ax = plt.subplots()
        ax.pie(protocol_counts, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')
        st.pyplot(fig)

# Main loop to update UI every 2 seconds without freezing Streamlit
def main():
    placeholder = st.empty()

    while True:
        with placeholder.container():
            render_ui()
        time.sleep(2)  # Wait 2 seconds before refreshing UI

if __name__ == "__main__":
    main()

