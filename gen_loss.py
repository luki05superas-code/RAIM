import time
import random
import pandas as pd
import requests

API_URL = "http://127.0.0.1:5000/api/measurements"
FILE_PATH = "data/patient_001.csv"
PATIENT_ID = "patient_001"
loss_probability = 0.2

# wczytanie danych z pliku
def load_data():
    df = pd.read_csv(FILE_PATH)
    return df.to_dict(orient="records")

# modyfikacja danych (żeby nie były tylko odtwarzane)
def modify_value(original_value):
    noise = random.uniform(-1.5, 1.5)
    return round(original_value + noise, 2)

# wysyłanie danych
def stream_data():
    rows = load_data()
    index = 0

    while True:
        row = rows[index]

        modified_value = modify_value(row["value"])

        # losowe usunięcie pomiaru
        if random.random() < loss_probability:
            print("Pomiar utracony:", row["time"])
            index = (index + 1) % len(rows)
            time.sleep(1)
            continue

        payload = {
            "patient_id": PATIENT_ID,
            "source_time": row["time"],
            "value": modified_value,
            "stream_time": time.time()
        }

        try:
            response = requests.post(API_URL, json=payload)
            print("Wysłano:", payload)
        except Exception as e:
            print("Błąd:", e)

        index = (index + 1) % len(rows)
        time.sleep(1)

if __name__ == "__main__":
    stream_data()