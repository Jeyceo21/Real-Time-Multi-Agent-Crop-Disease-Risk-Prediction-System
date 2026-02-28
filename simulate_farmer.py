import requests
import random
from datetime import datetime, timedelta

# Farmer location (Tamil Nadu example)
latitude = 11.0
longitude = 78.0
import random

states_data = {
    "TamilNadu": (11.0, 78.0),
    "Punjab": (30.9, 75.8),
    "UttarPradesh": (26.8, 80.9),
    "AndhraPradesh": (15.9, 79.7),
    "Chhattisgarh": (21.3, 81.6),
    "WestBengal": (22.9, 88.4)
}

state = random.choice(list(states_data.keys()))
latitude, longitude = states_data[state]

# Automatically generate sowing date (25 days ago)
sowing_date = datetime.now() - timedelta(days=25)
sowing_days = (datetime.now() - sowing_date).days

# Simulate nitrogen application pattern
nitrogen_days = random.randint(3, 7)

payload = {
    "latitude": latitude,
    "longitude": longitude,
    "nitrogen_days": nitrogen_days,
    "sowing_days": sowing_days,
    "state": state
}

print("🌾 Farmer Data Auto-Generated")
print(payload)

response = requests.post("http://127.0.0.1:8000/predict", json=payload)

if response.status_code == 200:
    result = response.json()

    print("\n📊 AI Prediction Result")
    print("Blast Probability:", result["blast_probability"])
    print("Confidence Score:", result["confidence_score"])
    print("Projected Yield Loss %:", result["projected_yield_loss_percent"])

    if result["blast_probability"] > 0.6:
        print("\n⚠ HIGH RISK ALERT — Inspect field immediately")
    else:
        print("\n✅ Risk Under Control")

else:
    print("Error:", response.text)