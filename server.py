from flask import Flask, request, jsonify, send_from_directory #flask- tworzy serwer, req - odbiera dane, json- zamienia dane na json, send- ptwiera html
from flask_cors import CORS #komunikacja back z front
import time
import csv

#tworzenie serwer
app = Flask(__name__, static_folder="static")
CORS(app)

# lista na dane
measurements = [] #zapis wszystkich pomiarow
last_delay = 0 #ostatnie opoznienie transmisji

# strona główna
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

# odbieranie danych z generatora
@app.route("/api/measurements", methods=["POST"])
def receive_measurement():
    global last_delay
    data = request.get_json()

    if not data:
        return jsonify({"error": "Brak danych JSON"}), 400

    server_time = time.time() #zapis danych kiedy serwer dostał dane 
    stream_time = data.get("stream_time", server_time) #czas kiedy generator wysłał dane, jeśli brak to czas serwera
    current_delay = round(server_time - stream_time, 4) #obliczenie opoznienia transmisji/latencji
    jitter = round(abs(current_delay - last_delay), 4) if last_delay !=0 else 0 #obliczenie jittera
    last_delay = current_delay

#tworzenie pomiaru
    item = {
        "patient_id": data.get("patient_id", "patient_001"), #id pacjenta
        "source_time": data.get("source_time"), #czas z pliku csv
        "value": data.get("value"), #wartość tętna 
        "stream_time": stream_time, #kiedy generator wysłał
        "server_time": server_time, #kiedy serwer odebrał
        "delay": current_delay, #opoznienei transmisji
        "jitter": jitter #jitter
    }

    measurements.append(item) #zapis do listy 
    #Logowanie pomiarów w konsoli
    print(f"[{item['patient_id']}] Tętno: {item['value']} | Opóźnienie: {current_delay}s | Jitter: {jitter}s")
    #Zapis pomiarów do pliku CSV
    save_to_report(current_delay, jitter)


#ograniczenie danych zeby lista nie rosła w nieskoczonosc - usuwa najstarszy pomiar
    if len(measurements) > 200:
        measurements.pop(0)

    return jsonify({
        "message": "Pomiar odebrany", #odp api
        "item": item
    }), 201

# pobieranie danych do wykresu
@app.route("/api/measurements/latest", methods=["GET"])
def get_latest_measurements():
    return jsonify(measurements[-50:])

# metryki - zwraca statystyki
@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    if not measurements:
        return jsonify({
            "count": 0,
            "avg_delay": 0,
            "max_delay": 0
        })

    delays = [m["delay"] for m in measurements]

    return jsonify({
        "count": len(measurements),
        "avg_delay": round(sum(delays) / len(delays), 4),
        "max_delay": round(max(delays), 4)
    })

def save_to_report(lat, jit):
    with open('measurement_report.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime("%H:%M:%S"), lat, jit])

        
# start serwera
if __name__ == "__main__":
    with open('measurement_report.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Latency", "Jitter"])
    print("Plik raportu został utworzony/wyczyszczony.")
    app.run(debug=True)