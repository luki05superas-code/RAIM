from flask import Flask, request, jsonify, send_from_directory #flask- tworzy serwer, req - odbiera dane, json- zamienia dane na json, send- ptwiera html
from flask_cors import CORS #komunikacja back z front
import time
import csv
import os
from dotenv import load_dotenv
from supabase import create_client
from concurrent.futures import ThreadPoolExecutor

SIMULATE_OVERLOAD = False #symulacja obciążenia serwera
LIMIT_THREADS = True #ograniczenie liczby wątków

safe_pool = ThreadPoolExecutor(max_workers=5) #bezpieczna pula wątków
unsafe_pool = ThreadPoolExecutor(max_workers=1000) #niebezpieczna pula wątków

db_metrics = {
    "queue_size": 0,
    "db_write_time": 0
}

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
#tworzenie serwer
app = Flask(__name__, static_folder="static")
CORS(app)

# lista na dane
patients_data = {} #zapis wszystkich pomiarow
patients_last_delay = {} #ostatnie opoznienie transmisji

# strona główna
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

# Funkcja do zapisu danych do bazy danych
def db_write(item):
    global db_metrics
    start_time = time.time()
    if SIMULATE_OVERLOAD:
        time.sleep(1.5)  # symulacja opóźnienia zapisu do bazy
    
    try:
        supabase.table("measurements").insert(item).execute()
    except Exception as e:
        print("Błąd zapisu do Supabase:", e)
    
    db_metrics["db_write_time"] = round((time.time() - start_time)*1000, 2) #czas zapisu do bazy w ms

    


# odbieranie danych z generatora
@app.route("/api/measurements", methods=["POST"])
def receive_measurement():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Brak danych JSON"}), 400
    
    patient_id = data.get("patient_id")
    if not patient_id:
        return jsonify({"error": "Brak patient_id"}), 400
    
    if data.get("value") is None:
        return jsonify({"error": "Brak wartości"}), 400
    try:
        float(data.get("value"))
    except ValueError:
        return jsonify({"error": "Wartość musi być liczbą"}), 400
    
    

    server_time = time.time() #zapis danych kiedy serwer dostał dane 
    stream_time = data.get("stream_time", server_time) #czas kiedy generator wysłał dane, jeśli brak to czas serwera
    current_delay = round(server_time - stream_time, 4) #obliczenie opoznienia transmisji/latencji
    jitter = round(abs(current_delay - patients_last_delay.get(patient_id, 0)), 4) if patient_id in patients_last_delay else 0 #obliczenie jittera
    patients_last_delay[patient_id] = current_delay

#tworzenie pomiaru
    item = {
        "patient_id": patient_id, #id pacjenta
        "value": data.get("value"), #wartość tętna 
        "stream_time": stream_time, #kiedy generator wysłał
        "server_time": server_time, #kiedy serwer odebrał
        "latency": current_delay, #opoznienei transmisji
        "jitter": jitter #jitter
    }
    if patient_id not in patients_data:
        patients_data[patient_id] = []

    patients_data[patient_id].append(item) #zapis do listy 
    
    

    if LIMIT_THREADS:
        safe_pool.submit(db_write, item) #zapis do bazy w bezpiecznej puli wątków
        db_metrics["queue_size"] = safe_pool._work_queue.qsize() #rozmiar kolejki wątków bezpiecznych
    else:
        unsafe_pool.submit(db_write, item) #zapis do bazy w niebezpiecznej puli wątków
        db_metrics["queue_size"] = len(unsafe_pool._threads) #rozmiar kolejki wątków niebezpiecznych
        
    
    #Logowanie pomiarów w konsoli
    print(f"[{patient_id}] Tętno: {item['value']} | Opóźnienie: {current_delay}s | Jitter: {jitter}s")
    #Zapis pomiarów do pliku CSV
    # save_to_report(current_delay, jitter)


#ograniczenie danych zeby lista nie rosła w nieskoczonosc - usuwa najstarszy pomiar
    if len(patients_data[patient_id]) > 50:
        patients_data[patient_id].pop(0)

    return jsonify({
        "message": "Pomiar odebrany", #odp api
        "item": item
    }), 201

# pobieranie danych do wykresu
@app.route("/api/measurements/latest", methods=["GET"])
def get_latest_measurements():
    return jsonify(patients_data)

# metryki - zwraca statystyki
@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    all_delays = []
    total_count = 0
    for patient_id, measurements in patients_data.items():
        all_delays.extend([m["latency"] for m in measurements])
        total_count += len(measurements)

    if not all_delays:
        return jsonify({
            "count": 0,
            "avg_delay": 0,
            "max_delay": 0,
            "buffer_size": db_metrics["queue_size"],
            "db_speed_ms": db_metrics["db_write_time"]
        })

    

    return jsonify({
        "count": total_count,
        "avg_delay": round(sum(all_delays) / len(all_delays), 4),
        "max_delay": round(max(all_delays), 4),
        "buffer_size": db_metrics["queue_size"],
        "db_speed_ms": db_metrics["db_write_time"]
    })

#def save_to_report(lat, jit):
#    with open('measurement_report.csv', mode='a', newline='') as file:
 #       writer = csv.writer(file)
  #      writer.writerow([time.strftime("%H:%M:%S"), lat, jit])




# start serwera
if __name__ == "__main__":
    #with open('measurement_report.csv', mode='w', newline='') as file:
     #   writer = csv.writer(file)
      #  writer.writerow(["Timestamp", "Latency", "Jitter"])
    #print("Plik raportu został utworzony/wyczyszczony.")
    app.run(debug=True, threaded=True)