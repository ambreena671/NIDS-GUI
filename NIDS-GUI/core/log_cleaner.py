import os
import time

def delete_old_logs(log_dir='logs', max_age_days=2):
    now = time.time()
    cutoff = now - (max_age_days * 86400)  # seconds in a day
    if not os.path.exists(log_dir):
        return
    for filename in os.listdir(log_dir):
        filepath = os.path.join(log_dir, filename)
        if os.path.isfile(filepath) and os.path.getmtime(filepath) < cutoff:
            os.remove(filepath)
            print(f"[LOG] Deleted old log: {filename}")

