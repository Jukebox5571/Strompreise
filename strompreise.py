import pandas as pd
import requests
from datetime import datetime
import os
import json

# === Konfiguration ===
api_url = "https://192.168.40.130:4747/RESTApi/FXInterface/EPEX15minIntraday?date=06.11.2024" # ← Deine API-URL
token = os.getenv("STROM_API_TOKEN")             # ← aus GitHub Secret oder Umgebungsvariable

# === Header mit Token ===
headers = {
    "X-Token-ID": "CYpMHSpBCyMyCwQiNAKJlLGiaABEwFTTBoSTL92IYuLVurKBkuDeb8FfWU9wsIqhh6wnbdOFI57qauD08M4p3UWlpnVAy1vYTj9NZEAbxxJldZBxTvVjg4htfWiKKt3q"# oder z. B. "X-API-Token"
    "Accept": "application/json"
}

# === Daten abrufen ===
response = requests.get(api_url, headers=headers, verify=False)
response.raise_for_status()
data = response.json()["data"]  # evtl. anpassen, je nach API
print(data)
# === Daten vorbereiten ===
preise = []
for eintrag in data:
    start = datetime.fromisoformat(eintrag["start_timestamp"][:-1])
    preis = eintrag["marketprice"] / 10  # z. B. Umrechnung in ct/kWh
    preise.append({
        "Datum": start.strftime("%Y-%m-%d"),
        "Uhrzeit": start.strftime("%H:%M"),
        "Preis (ct/kWh)": preis
    })

# === JSON-Datei speichern/ergänzen ===
json_datei = "strompreise_awattar.json"

if os.path.exists(json_datei):
    # Alte Daten laden
    with open(json_datei, "r", encoding="utf-8") as f:
        alt = json.load(f)
    # Kombinieren & Duplikate vermeiden
    gesamt = {f'{e["Datum"]} {e["Uhrzeit"]}': e for e in alt + preise}
    preise_gesamt = list(gesamt.values())
else:
    preise_gesamt = preise

# Sortieren nach Datum & Uhrzeit
preise_gesamt.sort(key=lambda x: (x["Datum"], x["Uhrzeit"]))

# Speichern als JSON
with open(json_datei, "w", encoding="utf-8") as f:
    json.dump(preise_gesamt, f, ensure_ascii=False, indent=2)
