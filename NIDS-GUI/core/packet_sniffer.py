from scapy.all import sniff, IP, TCP, UDP, ICMP
from queue import Queue

packet_queue = Queue()

def packet_callback(packet):
    try:
        features = {
            "src_ip": None,
            "dst_ip": None,
            "length": len(packet),
            "protocol": 0,
            "src_port": 0,
            "dst_port": 0,
            "flags": "NONE"
        }

        if IP in packet:
            features["src_ip"] = packet[IP].src
            features["dst_ip"] = packet[IP].dst
            features["protocol"] = packet[IP].proto

            if TCP in packet:
                features["src_port"] = packet[TCP].sport
                features["dst_port"] = packet[TCP].dport
                flags = packet[TCP].flags

                # Map TCP flags to your flag strings
                if flags == 0x02:
                    features["flags"] = "S"   # SYN
                elif flags == 0x10:
                    features["flags"] = "A"   # ACK
                elif flags == 0x18:
                    features["flags"] = "PA"  # PSH+ACK
                elif flags == 0x11:
                    features["flags"] = "FA"  # FIN+ACK
                else:
                    features["flags"] = "NONE"

            elif UDP in packet:
                features["src_port"] = packet[UDP].sport
                features["dst_port"] = packet[UDP].dport
                features["flags"] = "NONE"

            elif ICMP in packet:
                features["flags"] = "NONE"

        packet_queue.put(features)
        print(f"[+] Packet captured: {features}")

    except Exception as e:
        print(f"[-] Failed to parse packet: {e}")

def start_sniffing():
    sniff(prn=packet_callback, store=False, iface="eth0")  # change iface as needed

