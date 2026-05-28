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
* **Identyfikacja problemu:** Monitorowanie tętna (BPM) w czasie rzeczywistym jest kluczowe dla wykrywania nagłych zdarzeń, takich jak tachykardia, bradykardia czy asystolia. Opóźnienia w transmisji danych (latency) mogą opóźnić reakcję personelu medycznego o krytyczne sekundy.

### Użytkownicy systemu
- lekarze,
- pielęgniarki,
- personel oddziałów intensywnej terapii,
- personel techniczny nadzorujący systemy medyczne.

### Analiza ryzyk
- **Opóźnienia transmisji** – dane docierają za późno i nie odzwierciedlają aktualnego stanu pacjenta.
- **Jitter** – nieregularność dostarczania próbek utrudnia płynną analizę sygnału.
- **Utrata pakietów** – może prowadzić do fałszywych alarmów o braku sygnału (asystolii), co wywołuje tzw. "alarm fatigue" (znieczulica na alarmy) u personelu.
- **Przeciążenie systemu (backpressure)** – może prowadzić do spowolnienia odbioru danych i pogorszenia działania monitoringu.

---


## 2. Projekt architektury systemu

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

## 3. Etap 1 – działająca funkcjonalność minimalna (API-first)

W ramach etapu 1 zaimplementowano minimalną działającą wersję systemu zgodnie z podejściem API-first.

### Założenia etapu 1
- streaming danych z częstotliwością 1 Hz,
- wykorzystanie danych pochodzących z pliku,
- modyfikacja danych przed wysłaniem,
- odbiór danych przez backend za pomocą API,
- wizualizacja danych na wykresie w czasie rzeczywistym.

---
## 4. Etap 2 – symulacja zaburzeń transmisji

Celem drugiego etapu projektu była analiza wpływu zaburzeń transmisji danych na działanie systemu monitoringu parametrów pacjenta w czasie rzeczywistym.

## Założenia etapu 2
- wysyłanie danych z symulacją opóżnienia,
- wysyłanie danych z symulacją burst,
- wysyłanie danych z symulacją reorderu danych,
- pomiar latencji i jitter, wypisanie pomiaru w terminalu oraz zapisanie do pliku,
- raport z pomiarów.

## Zaimplementowane scenariusze zaburzeń

### 1. Symulacja opóźnień transmisji (Delay)

W scenariuszu delay dane są wysyłane z losowym opóźnieniem czasowym.  
Pozwala to zasymulować problemy sieciowe oraz zwiększoną latencję transmisji.

W projekcie zastosowano losowe opóźnienia przed wysłaniem pakietu danych do backendu.
Plik:
`gen_delay.py`

## Wykres opóźnień
![Wykres Delay](assets/jitter_delay.png)
---

### 2. Symulacja burst danych

W scenariuszu burst dane są chwilowo buforowane, a następnie wysyłane jednocześnie w większej liczbie.

Pozwala to zasymulować chwilowe przeciążenie systemu oraz zjawisko backpressure.

Plik:
`gen_burst.py`

## Wykres burst danych
![Wykres Burst](assets/latency_burst.png)

---

### 3. Symulacja reorder pakietów
W scenariuszu reorder dane są wysyłane w nieprawidłowej kolejności.

Pozwala to sprawdzić wpływ błędnej kolejności pakietów na działanie systemu monitorującego.

Plik:
`gen_order.py`

## Wykres reorder pakietów
![Wykres reorder pakietów](assets/latency_order.png)

---

### 4. Symulacja utraty pakietów

W scenariuszu packet loss część pomiarów jest celowo pomijana podczas transmisji.

Pozwala to zasymulować problemy sieciowe prowadzące do utraty danych.

Plik:
`gen_loss.py`

## Wykres utraty 
![Wykres utraty pakietów](assets/jitter_loss.png)

---
## 5. Instrumentacja i pomiary

W systemie zaimplementowano mechanizmy monitorujące parametry transmisji danych.

### Mierzone parametry

- latencja transmisji,
- jitter,
- liczba odebranych pomiarów,
- maksymalne opóźnienie.

### Logowanie danych

Pomiary:
- wyświetlane są w terminalu,
- zapisywane są do pliku `measurement_report.csv`.

Backend oblicza opóźnienie transmisji na podstawie różnicy pomiędzy czasem wysłania danych przez generator a czasem odebrania danych przez serwer.

---

## 6. Raport z pomiarów

Podczas testów zaobserwowano, że:
- scenariusz burst powoduje największe chwilowe opóźnienia,
- jitter zwiększa się przy nieregularnych odstępach wysyłania danych,
- utrata pakietów prowadzi do brakujących próbek,
- reorder powoduje odbieranie danych w błędnej kolejności.

System poprawnie rejestrował zaburzenia oraz umożliwiał analizę wpływu problemów transmisyjnych na monitoring pacjenta.

---
## 7. Instrukcja uruchomienia

 ### Uruchomienie backendu komendą w terminalu: 
  python server.py

 ### Uruchomienie generatora podstawowego komendą w terminalu: 
  python generator.py

 ### Uruchomienie scenariuszy zaburzeń:
 - python gen_delay.py
 - python gen_burst.py
 - python gen_order.py
 - python gen_loss.py

 ---
## 8. Etap 3 – współbieżność i analiza błędów

Głównym celem trzeciego etapu było wprowadzenie do systemy współbieżności. Przetestowano stabilność systemu w warunkach skrajnego obciążenia bazy danych. Wdrożono mechanizmy kontroli.

## Założenia etapu 3
- obsługa 20 pacjentów (20 wątków generujących dane)
- analiza przeciążenia
- demonstracja zjawiska współbieżności (drift)
- analiza przeciążenia
- implementacja mechanizmu kontroli
- porównanie przed i po poprawce
- 2 pytesty

## Teoretyczne omówienie wybranych zagadnień współbierzności

W ramach Etapu 3 zbadano dwa kluczowe zjawiska występujące w systemach rozproszonych i systemach czasu rzeczywistego (Real-Time Systems): **dryft czasowy (drift)** w generowaniu strumieni danych oraz **zatory wydajnościowe (backpressure)** w architekturze zapisu asynchronicznego.

### 1. Dryft czasowy (Time Drift) w strumieniowaniu danych
W systemach monitorowania zdrowia pacjentów (gdzie 20 urządzeń wysyła dane co 1 sekundę) kluczowa jest powtarzalność i miarowość transmisji. W teorii współbieżności standardowa pętla oparta na zwykłym uśpieniu wątku (np. `time.sleep(1.0)`) generuje zjawisko **dryftu czasowego**.

* **Podłoże teoretyczne:** Instrukcja uśpienia blokuje wątek na określony czas, ale sam proces wybudzenia wątku, obsługa logiki, walidacja danych oraz narzut wykonania kodu przez procesor (CPU execution time) trwają ułamek milisekundy. Wykonując pętlę `while True: sleep(1); execute_logic()`, realny czas między kolejnymi pakietami wynosi zawsze $1.0s + \Delta t$. W skali minut lub godzin te ułamki sekund kumulują się, powodując rozjeżdżanie się harmonogramu i opóźnianie transmisji (wątki "dryfują" w czasie).
* **Kontekst systemu:** Nasz generator zapobiega temu zjawisku poprzez **kontrolę dryftu** (obliczanie dynamicznego czasu uśpienia). Zamiast sztywnego `sleep(1)`, system sprawdza rzeczywisty czas, jaki upłynął od startu, i skraca następne uśpienie o zaistniałe opóźnienie $\Delta t$. Dzięki temu 20 pacjentów wysyła dane idealnie w punkt, co sekundę, generując dla serwera Flask idealnie miarowe obciążenie (tzw. ruch kaskadowy), bez zniekształceń harmonicznych.

### 2. Obciążenie bazy danych i zjawisko Backpressure
Gdy serwer medyczny zostaje zasypany falą 20 zapytań na sekundę, wątek główny Flaska nie powinien być blokowany powolnymi operacjami I/O (zapisem przez internet do Supabase), ponieważ przestałby natychmiastowo odpowiadać na nowe pakiety. Rozwiązaniem jest asynchroniczność i oddelegowanie zapisu do wątków tła. W sytuacji awarii lub przeciążenia bazy (u nas symulowane opóźnienie 1.5s), ujawnia się problem zarządzania wydajnością:

* **Brak kontroli (Scenariusz Awaryjny):** Serwer bez ograniczeń (`max_workers=1000`) tworzy wątki na żądanie. Nowe wątki powstają szybciej, niż baza danych jest w stanie je zamykać. Prowadzi to do nasycenia zasobów (Resource Exhaustion) i załamania warstwy sieciowej systemu operacyjnego (`WinError 10035`), powodując bezpowrotną utratę danych pacjentów.
* **Wprowadzenie Puli i Bufora (Scenariusz Bezpieczny):** Ograniczenie współbieżności do `max_workers=5` tworzy tzw. **wąskie gardło (bottleneck)**. W tym momencie system zaczyna natywnie obsługiwać mechanizm **Backpressure**. Zamiast bezmyślnie obciążać system operacyjny i chmurę, serwer stawia barierę, a nadmiarowe pakiety medyczne są bezpiecznie kolejkowane w pamięci RAM (`_work_queue`).

Dzięki buforowaniu, w warunkach skrajnego obciążenia bazy danych, system świadomie zamienia ryzyko awarii sieciowej i utraty danych na kontrolowany wzrost opóźnienia przetwarzania (kolejka rosnąca do ponad 2000 zadań). Jest to klasyczny kompromis architektoniczny (trade-off) w systemach rozproszonych: **poświęcenie natychmiastowej aktualności danych na rzecz ich 100% integralności i bezstratności**.

### 3. Testy Automatyczne (PyTest)

W celu zweryfikowania poprawności działania punktu końcowego (endpointu) API, zaimplementowano testy automatyczne przy użyciu frameworka `pytest`. Testy skupiają się na dwóch kluczowych scenariuszach transmisji danych:

1. **Test poprawnego zapytania (Positive Test):** Weryfikuje, czy serwer poprawnie odbiera prawidłowy pakiet danych z generatora (zawierający poprawne ID pacjenta oraz prawidłową wartość tętna). Test potwierdza, że serwer zwraca oczekiwany status `HTTP 201 Created`, co oznacza, że dana pomyślnie doszła i została zarejestrowana.
2. **Test walidacji tętna (Negative Test):** Sprawdza mechanizm obronny serwera przed błędnymi danymi. Test symuluje sytuację, w której generator próbuje wysłać paczkę z nieprawidłową wartością tętna (np. tekst zamiast liczby). Test potwierdza, że serwer prawidłowo wykrywa błąd, odrzuca pakiet i zwraca status `HTTP 400 Bad Request`.

**Wniosek:** Testy potwierdzają, że endpoint Flaska działa stabilnie – bezbłędnie przyjmuje poprawne pomiary medyczne i natychmiast odrzuca pakiety uszkodzone, chroniąc system przed przetwarzaniem nieprawidłowych danych.

## 9. Struktura repozytorium

```text
RAIM/
├── .pytest_cache/
├── assets/
│   ├── jitter_delay.png
│   ├── jitter_loss.png
│   ├── kib.png
│   ├── latency_burst.png
│   ├── latency_order.png
│   ├── pg_logo.png
│   └── Widok_aplikacji.png
├── data/
│   └── patient_001.csv
├── static/
│   └── index.html
├── venv/
├── .env
├── .gitignore
├── gen_burst.py
├── gen_delay.py
├── gen_loss.py
├── gen_order.py
├── generator.py
├── measurement_report.csv
├── README.md
├── requirements.txt
├── server.py
├── test_system.py
└── wykresy.py
```