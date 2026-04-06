import random 
import time 
import json
status = ["moving", "idle", "alert"]
lat = 54.3519
lng = 18.6463
print("START")
while True: 

    lat += random.uniform(-0.0001,0.0001)
    lng += random.uniform(-0.0001,0.0001)
    truck = {
    "id": "TRUCK-00",
    "lat": round(lat, 7),
    "lng": round(lng, 7),
    "status": random.choice(status),
    "time": int(time.time())
    }
    print(json.dumps(truck, indent=2))
    time.sleep(1)
