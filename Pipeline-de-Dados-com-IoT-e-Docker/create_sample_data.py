import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

num_readings = 500
start_date = datetime(2018, 7, 28, 0, 0, 0)

ids = [f"__export__.temp_log_{i}_{np.random.randint(100000, 999999)}" for i in range(num_readings)]
room_ids = np.random.choice(["Room Admin", "Room Kitchen", "Room Office"], num_readings)
noted_dates = [start_date + timedelta(hours=np.random.randint(0, 3000)) for _ in range(num_readings)]
temps = np.random.normal(loc=30, scale=5, size=num_readings).round(1)
out_in = np.random.choice(["In", "Out"], num_readings)

df = pd.DataFrame({
    "id": ids,
    "room_id/id": room_ids,
    "noted_date": [d.strftime("%d-%m-%Y %H:%M") for d in noted_dates],
    "temp": temps,
    "out/in": out_in
})

df = df.sort_values("noted_date").reset_index(drop=True)

data_path = "data/IOT-temp.csv"
df.to_csv(data_path, index=False)

print(f"Sample dataset created successfully at {data_path}")
print(f"Total records: {len(df)}")
print("\nFirst 5 rows:")
print(df.head())
