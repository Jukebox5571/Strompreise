import pandas as pd
import requests
from datetime import datetime, timedelta
import os

# Aktuelles Datum
heute = datetime.now().date()

# AwaTtar API-Endpunkt (AT oder DE)
response = requests.get("https://api.awattar.de/v1/marketdata")
data = response.json()["data"]

# Daten extrahieren
preise = []
for eintrag in data:
    start = datetime.fromisoformat(eintrag["start_timestamp"][:-1])
    preis = eintrag["marketprice"] / 10  # Umrechnung in ct/kWh
    preise.append({"Datum": start.strftime("%Y-%m-%d"), "Uhrzeit": start.strftime("%H:%M"), "Preis (ct/kWh)": preis})

df_neu = pd.DataFrame(preise)

# Pfad zur CSV
csv_datei = "strompreise_awattar.csv"

# Prüfen, ob Datei existiert → Daten anhängen oder neu schreiben
if os.path.exists(csv_datei):
    df_alt = pd.read_csv(csv_datei)
    # Duplikate vermeiden (z. B. falls schon einmal gespeichert)
    df_gesamt = pd.concat([df_alt, df_neu]).drop_duplicates(subset=["Datum", "Uhrzeit"]).sort_values(by=["Datum", "Uhrzeit"])
else:
    df_gesamt = df_neu

# Speichern
df_gesamt.to_csv(csv_datei, index=False)
