import time
import random
import pandas as pd
import requests

# adres API odbierającego pomiary
API_URL = "http://127.0.0.1:5000/api/measurements"

# plik z danymi pacjenta
FILE_PATH = "data/patient_001.csv"

# identyfikator pacjenta
PATIENT_ID = "patient_001"


# wczytanie danych pomiarowych z pliku CSV
def load_data():
    df = pd.read_csv(FILE_PATH)

    # zamiana DataFrame na listę słowników
    return df.to_dict(orient="records")


# dodanie niewielkiego losowego szumu do wartości pomiaru
# dzięki temu dane nie są identyczne przy każdym odtworzeniu
def modify_value(original_value):
    noise = random.uniform(-1.5, 1.5)
    return round(original_value + noise, 2)


# główna funkcja wysyłająca dane
def stream_data():

    # wczytanie wszystkich rekordów z pliku
    rows = load_data()

    # indeks aktualnego rekordu
    index = 0

    # bufor używany do symulacji zmiany kolejności pakietów
    buffer = None

    while True:

        # pobranie aktualnego rekordu
        row = rows[index]

        # modyfikacja wartości pomiaru
        modified_value = modify_value(row["value"])

        # przygotowanie pakietu danych
        payload = {
            "patient_id": PATIENT_ID,
            "source_time": row["time"],
            "value": modified_value,
            "stream_time": time.time()
        }

        # losowanie scenariusza transmisji
        rand = random.random()

        # 20% przypadków - symulacja reordering order
        if rand < 0.2:

            print("reordering order")

            # zapisanie starszego pakietu do bufora
            buffer = payload

            # przejście do kolejnego pomiaru
            index = (index + 1) % len(rows)
            row = rows[index]

            # sztuczne opóźnienie
            time.sleep(1)

            # przygotowanie nowszego pakietu
            payload = {
                "patient_id": PATIENT_ID,
                "source_time": row["time"],
                "value": modify_value(row["value"]),
                "stream_time": time.time()
            }

            print("Wysyłanie pomieszanych danych")

            # wysłanie nowszego pakietu jako pierwszego
            try:
                response = requests.post(API_URL, json=payload)
                print("Wysłano :", payload)

            except Exception as e:
                print("Błąd podczas wysyłania:", e)

            time.sleep(0.2)

            # wysłanie starszego pakietu jako drugiego
            try:
                response = requests.post(API_URL, json=buffer)
                print("Wysłano :", buffer)

                # losowe opóźnienie sieciowe
                time.sleep(random.uniform(0.2, 1.0))

            except Exception as e:
                print("Błąd podczas wysyłania:", e)

            # wyczyszczenie bufora
            buffer = None

            time.sleep(0.8)

        else:

            # standardowa transmisja danych
            try:
                response = requests.post(API_URL, json=payload)
                print("Wysłano:", payload)

            except Exception as e:
                print("Błąd:", e)

            # wysyłanie co 1 sekundę
            time.sleep(1)

        # przejście do następnego rekordu z pliku
        index = (index + 1) % len(rows)


# uruchomienie programu
if __name__ == "__main__":
    stream_data()