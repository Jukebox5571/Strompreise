import pandas as pd
import requests
from datetime import datetime, timedelta
import os
import json

# === Konfiguration ===
api_url = "https://192.168.40.130:4747/RESTApi/FXInterface/EPEX15minIntraday?date=02.07.2025"
token = os.getenv("STROM_API_TOKEN")

# === Header mit Token ===
headers = {
    "X-Token-ID": "CYpMHSpBCyMyCwQiNAKJlLGiaABEwFTTBoSTL92IYuLVurKBkuDeb8FfWU9wsIqhh6wnbdOFI57qauD08M4p3UWlpnVAy1vYTj9NZEAbxxJldZBxTvVjg4htfWiKKt3q",  # Sicher speichern, z. B. in Umgebungsvariablen
    "Accept": "application/json"
}

# === Daten abrufen ===
response = requests.get(api_url, headers=headers, verify=False)
response.raise_for_status()
raw = response.json()

datum = datetime.strptime(raw["date"], "%d.%m.%Y")
preise_roh = raw["data"]

# === Zeitpunkte im 15-Minuten-Takt generieren ===
preise = []
for i, wert in enumerate(preise_roh):
    zeitpunkt = datum + timedelta(minutes=15 * i)
    preise.append({
        "Zeitstempel": zeitpunkt.isoformat(),  # z. B. 2025-07-02T12:30:00
        "Preis (ct/kWh)": round(wert, 4)
    })

# === JSON-Datei speichern/ergänzen ===
json_datei = "strompreise_epex.json"

if os.path.exists(json_datei):
    with open(json_datei, "r", encoding="utf-8") as f:
        alt = json.load(f)
    # Zusammenführen, Duplikate vermeiden
    gesamt = {e["Zeitstempel"]: e for e in alt + preise}
    preise_gesamt = list(gesamt.values())
else:
    preise_gesamt = preise

# Nach Zeitstempel sortieren
preise_gesamt.sort(key=lambda x: x["Zeitstempel"])

# Speichern
with open(json_datei, "w", encoding="utf-8") as f:
    json.dump(preise_gesamt, f, ensure_ascii=False, indent=2)
