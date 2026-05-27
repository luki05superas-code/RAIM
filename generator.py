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
import asyncio
import aiohttp
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
    tentno= random.randint(60, 80)
    while True:
        tentno += random.choice([-1, 0, 1])
        tentno = max(50, min(tentno, 100))
        yield tentno


async def stream_data(session, patient_id):
    hr_generator = generate_heart_rate()
   
    last_run_time = time.time()
    

    while True:
        
        now = time.time()
        current_value = next(hr_generator)
        target_interval = 1.0
        
        # Obliczenie DRIFT 
        drift= now - last_run_time
        last_run_time = now

        payload = {
            "patient_id": patient_id,
            "source_time": now,
            "value": current_value,
            "stream_time": now            
            }
        print(f"[{patient_id}] Czas od ostatniego pomiaru {drift:.4f} s (Powinno być 1.0 s)")

        try:
             async with session.post(API_URL, json=payload) as response:
                if response.status in (200, 201):
                    print(f"[{patient_id}] Wysłano pomiar: {current_value} BPM")
                else:                    
                   print(f"[{patient_id}] Błąd serwera: {response.status}")
                          
        except Exception as e:
                print(f"[{patient_id}] Błąd połączenia z API: {e}")

        execution_time = time.time() - now
        sleep_time = target_interval - execution_time
        if sleep_time < 0:
            sleep_time = 0

        await asyncio.sleep(sleep_time)

async def main():
  patients  = get_patients()
  print(f"Pobrano pacjentów z Supabase: {len(patients)}")
  async with aiohttp.ClientSession() as session:
    tasks = []
    for patient in patients:
        patient_id = patient["patient_id"]
        tasks.append(stream_data(session, patient_id))
    await asyncio.gather(*tasks)
        


if __name__ == "__main__":
    asyncio.run(main())