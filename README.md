NIDS-GUI
🔧 Installation Instructions

✅ Required Packages
Install using pip or inside a virtual environment:

pip install -r requirements.txt
Or install individually:
pip install streamlit scikit-learn pandas matplotlib scapy
On Kali Linux, ensure you run the tool with root privileges due to raw packet capture.

▶️ How to Run
1. Clone or unzip the project:

cd ~/Downloads/NIDS-GUI

3. Train the ML Model (optional if nids_model.pkl exists):
   
python3 model/train_model.py

5. Run the Application
sudo streamlit run ui/dashboard.py

6. Open browser at:
http://localhost:8501
