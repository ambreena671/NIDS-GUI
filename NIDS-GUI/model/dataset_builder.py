# dataset_builder.py
import pandas as pd
from scapy.all import sniff

benign_data = []

# Callback to capture benign packets
def packet_callback(packet):
    if packet.haslayer('IP') and packet.haslayer('TCP'):
        benign_data.append({
            'src_ip': packet['IP'].src,
            'dst_ip': packet['IP'].dst,
            'length': len(packet),
            'protocol': 6,
            'src_port': packet['TCP'].sport,
            'dst_port': packet['TCP'].dport,
            'flags': str(packet['TCP'].flags),
            'label': 0
        })

print("[*] Capturing benign traffic... Press Ctrl+C to stop.")
sniff(prn=packet_callback, count=200)

# Save to CSV
pd.DataFrame(benign_data).to_csv("benign_traffic.csv", index=False)
print("[+] Saved benign_traffic.csv")

