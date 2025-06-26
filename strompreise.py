import requests
import pandas as pd
from datetime import datetime, timedelta
import os, sys

url = "https://api.awattar.de/v1/marketdata"
now = datetime.now()
start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
end_time = start_time + timedelta(days=1)
params = { "start": int(start_time.timestamp() * 1000), "end": int(end_time.timestamp() * 1000) }

try:
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json().get("data", [])
except Exception as e:
    print(f"ERROR beim API-Abruf: {e}")
    sys.exit(1)

records = []
for item in data:
    t = datetime.fromtimestamp(item["start_timestamp"] / 1000)
    price = round(item["marketprice"] / 10, 2)
    records.append({"timestamp": t.strftime("%Y-%m-%d %H:%M:%S"), "preis_ct_kwh": price})

df_new = pd.DataFrame(records)
file = "strompreise_awattar.csv"

if os.path.exists(file):
    df_all = pd.concat([pd.read_csv(file), df_new]).drop_duplicates("timestamp")
else:
    df_all = df_new

df_all.to_csv(file, index=False)
print(f"✅ Gespeichert: {file}")
