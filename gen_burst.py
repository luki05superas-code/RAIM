import time
import random
import pandas as pd
import requests

API_URL = "http://127.0.0.1:5000/api/measurements"
FILE_PATH = "data/patient_001.csv"
PATIENT_ID = "patient_001"

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
    buffer = []

    while True:
        row = rows[index]
        modified_value = modify_value(row["value"])

        payload = {
            "patient_id": PATIENT_ID,
            "source_time": row["time"],
            "value": modified_value,
            "stream_time": time.time()
        }
        buffer.append(payload)
        rand = random.random()
        if rand < 0.2:
            print(f"nie można teraz wysłać danych, buforowanie")
            for _ in range(random.randint(3, 6)):
                time.sleep(1)
                index = (index + 1) % len(rows)
                row = rows[index]

                buffer.append({
                    "patient_id": PATIENT_ID,
                    "source_time": row["time"],
                    "value": modify_value(row["value"]),
                    "stream_time": time.time()
                })
            print(f"Wysyłanie buforowanych danych: {len(buffer)} pomiarów")
            for p in buffer:
                try:
                    response = requests.post(API_URL, json=p)
                    print("Wysłano z bufora:", p)
                except Exception as e:
                    print("Błąd podczas wysyłania z bufora:", e)
            buffer = []
            wait_time=0
        else:
            for p in buffer:
               try:
                    response = requests.post(API_URL, json=payload)
                    print("Wysłano:", payload)
               except Exception as e:
                    print("Błąd:", e)
            buffer = []
            wait_time=1
        index = (index + 1) % len(rows)
        if wait_time:
            time.sleep(wait_time)
   

if __name__ == "__main__":
    stream_data()