from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt

csv_data = """Timestamp,Latency,Jitter
23:03:46,0.0045,0
23:03:46,1.2097,1.2052
23:03:48,0.0015,1.2082
23:03:49,0.0021,0.0006
23:03:50,0.0015,0.0006

"""

# wczytanie danych
df = pd.read_csv(StringIO(csv_data))

# =========================
# WYKRES LATENCJI
# =========================

plt.figure(figsize=(12, 5))

plt.plot(
    df.index,
    df["Latency"],
    marker='o',
    linewidth=2
)

plt.xlabel("Numer pomiaru")
plt.ylabel("Latencja [s]")
plt.title("Latencja transmisji – scenariusz LOSS")

plt.grid(True)

# zapis wykresu
plt.savefig("latency_loss.png", bbox_inches='tight')

plt.close()

# =========================
# WYKRES JITTERA
# =========================

plt.figure(figsize=(12, 5))

plt.plot(
    df.index,
    df["Jitter"],
    marker='o',
    linewidth=2
)

plt.xlabel("Numer pomiaru")
plt.ylabel("Jitter [s]")
plt.title("Jitter transmisji – scenariusz loss")

plt.grid(True)

# zapis wykresu
plt.savefig("jitter_loss.png", bbox_inches='tight')

plt.close()

print("Wykresy zapisane.")
print("latency_loss.png")
print("jitter_loss.png")