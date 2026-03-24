# System monitoringu parametrów w czasie rzeczywistym.
**Autorki:** Amelia Supernak, Milena Żebrowska
**Przedmiot:** Rozwój aplikacji internetowych w medycynie
**Prowadząca:** dr inż. Anna Jezierska

---
## 1. Analiza potrzeb i wymagań klinicznych
* **Identyfikacja problemu:** Opóźnienia w przesyłaniu danych EKG mogą prowadzić do błędnych diagnoz (np. przeoczenie migotania komór).
* **Użytkownicy:** Lekarze, pielęgniarki na oddziałach intensywnej terapii.
* **Analiza ryzyk:** 
    * Utrata pakietów = dziury w wykresie.
    * Wysoki jitter = skaczący, nieczytelny wykres.
    * Przeciążenie serwera = brak monitoringu wielu pacjentów jednocześnie.

## 2. Projekt architektury systemu
System składa się z trzech modułów:
1.  **Generator (Producer):** Czyta dane z pliku i wysyła je przez API (1 Hz).
2.  **Serwer (API First):** Odbiera dane, mierzy opóźnienia i przekazuje je do frontendu.
3.  **Wizualizacja (Consumer):** Wyświetla wykres w czasie rzeczywistym.

---
