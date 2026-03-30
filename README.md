# System monitoringu parametrów w czasie rzeczywistym.
**Autorki:** Amelia Supernak, Milena Żebrowska
**Przedmiot:** Rozwój aplikacji internetowych w medycynie
**Rok studiów:** 3
**Prowadząca:** dr inż. Anna Jezierska

## Logo uczelni
![Politechnika Gdańska](assets/pg_logo.png)
## Logo katedry
![KIB](assets/kib.png)

---
## 1. Analiza potrzeb i wymagań klinicznych
* **Identyfikacja problemu:** Opóźnienia w przesyłaniu danych EKG mogą prowadzić do błędnych diagnoz (np. przeoczenie migotania komór).

### Użytkownicy systemu
- lekarze,
- pielęgniarki,
- personel oddziałów intensywnej terapii,
- personel techniczny nadzorujący systemy medyczne.

### Analiza ryzyk
- **Opóźnienia transmisji** – dane docierają za późno i nie odzwierciedlają aktualnego stanu pacjenta.
- **Jitter** – nieregularność dostarczania próbek utrudnia płynną analizę sygnału.
- **Utrata pakietów** – powoduje brak fragmentów przebiegu.
- **Przeciążenie systemu (backpressure)** – może prowadzić do spowolnienia odbioru danych i pogorszenia działania monitoringu.

---


## 3. Projekt architektury systemu

System został podzielony na trzy główne moduły:

### 1. Generator danych
Generator odczytuje dane z pliku i wysyła je do serwera z częstotliwością 1 Hz.  
Dane nie są wyłącznie odtwarzane – każda próbka może zostać lekko zmodyfikowana, np. przez dodanie zakłócenia.

### 2. Backend API
Backend odbiera próbki danych przez interfejs API, zapisuje je w pamięci oraz oblicza podstawowe parametry, np. opóźnienie transmisji.

### 3. Frontend
Frontend pobiera dane z API i przedstawia je na wykresie w czasie rzeczywistym.

### Schemat działania
`plik danych -> generator -> API -> backend -> frontend`

---

## 4. Etap 1 – działająca funkcjonalność minimalna (API-first)

W ramach etapu 1 zaimplementowano minimalną działającą wersję systemu zgodnie z podejściem API-first.

### Założenia etapu 1
- streaming danych z częstotliwością 1 Hz,
- wykorzystanie danych pochodzących z pliku,
- modyfikacja danych przed wysłaniem,
- odbiór danych przez backend za pomocą API,
- wizualizacja danych na wykresie w czasie rzeczywistym.

---

## 5. Struktura repozytorium

RAIM-main/
├── assets/
│   ├── pg_logo.png
│   └── kib.png
├── data/
│   └── patient_001.csv
├── static/
│   └── index.html
├── generator.py
├── server.py
├── requirements.txt
└── README.md