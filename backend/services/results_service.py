from datetime import datetime
import pytz
import os
import json

RESULTS_DIR = "results"
RESULTS_FILE = "results/results.json"


def save_results(data: dict):

    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

    # 🇮🇳 IST timezone
    ist = pytz.timezone("Asia/Kolkata")

    # current IST time
    ist_time = datetime.now(ist)

    # 12-hour format
    formatted_time = ist_time.strftime("%Y-%m-%d %I:%M:%S %p IST")

    payload = {
        "timestamp": formatted_time,
        "result": data
    }

    with open(RESULTS_FILE, "w") as f:
        json.dump(payload, f, indent=4)

    return RESULTS_FILE
