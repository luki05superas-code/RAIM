# import time
# import random
# import pandas as pd
# import requests

# API_URL = "http://127.0.0.1:5000/api/measurements"
# FILE_PATH = "data/patient_001.csv"
# PATIENT_ID = "patient_001"

# # wczytanie danych z pliku
# def load_data():
#     df = pd.read_csv(FILE_PATH)
#     return df.to_dict(orient="records")

# # modyfikacja danych (żeby nie były tylko odtwarzane)
# def modify_value(original_value):
#     noise = random.uniform(-1.5, 1.5)
#     return round(original_value + noise, 2)

# # wysyłanie danych co 1 sekundę
# def stream_data():
#     rows = load_data()
#     index = 0

#     while True:
#         row = rows[index]

#         modified_value = modify_value(row["value"])

#         payload = {
#             "patient_id": PATIENT_ID,
#             "source_time": row["time"],
#             "value": modified_value,
#             "stream_time": time.time()
#         }

#         try:
#             response = requests.post(API_URL, json=payload)
#             print("Wysłano:", payload)
#         except Exception as e:
#             print("Błąd:", e)

#         index = (index + 1) % len(rows)
#         time.sleep(1)

# if __name__ == "__main__":
#     stream_data()
import time
import random
import requests
import os
from dotenv import load_dotenv
from supabase import create_client

API_URL = "http://127.0.0.1:5000/api/measurements"

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_patients():
    result = supabase.table("patients").select("patient_id").execute()
    return result.data


def generate_heart_rate():
    return random.randint(60, 80)


def stream_data():
    patients = get_patients()

    print(f"Pobrano pacjentów z Supabase: {len(patients)}")

    while True:
        for patient in patients:
            now = time.time()

            payload = {
                "patient_id": patient["patient_id"],
                "source_time": now,
                "value": generate_heart_rate(),
                "stream_time": now
            }

            try:
                response = requests.post(API_URL, json=payload)
                print("Wysłano:", payload, "Status:", response.status_code)
            except Exception as e:
                print("Błąd:", e)

        time.sleep(1)


if __name__ == "__main__":
    stream_data()